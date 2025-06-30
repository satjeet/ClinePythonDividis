# -*- coding: utf-8 -*-
"""
Views for the Dividis API.
"""
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.utils import timezone
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from uuid import UUID

from .models import (
    Profile, Module, ModuleProgress, Mission, MissionProgress,
    Achievement, UserAchievement, Streak, Declaration, UnlockedPillar
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, ProfileSerializer,
    ModuleSerializer, ModuleProgressSerializer, MissionSerializer,
    MissionProgressSerializer, AchievementSerializer, UserAchievementSerializer,
    StreakSerializer, UserProfileDetailSerializer, ProgressOverviewSerializer,
    DeclarationSerializer, UnlockedPillarSerializer,
    HabitSerializer, ComfortWallSerializer,
    UserProfileUpdateSerializer
)

def sync_module_unlocks(user):
    """
    Sincroniza el estado de desbloqueo de módulos según XP y requisitos.
    Desbloquea automáticamente los módulos para los que el usuario cumple los requisitos.
    """
    profile = user.profile
    modules = Module.objects.all()
    for module in modules:
        progress, _ = ModuleProgress.objects.get_or_create(user=user, module=module)
        if progress.state == 'locked':
            # Lógica de requisitos personalizados
            can_unlock = False
            if module.id == "salud":
                if profile.experience_points >= module.xp_required:
                    can_unlock = True
            elif module.id == "personalidad":
                has_xp = profile.experience_points >= 200
                try:
                    mission = Mission.objects.get(id="46e39fc7-8a77-4e39-9559-283a73655d12")
                    mp = MissionProgress.objects.filter(user=user, mission=mission, state="completed").exists()
                except Exception:
                    mp = False
                if has_xp and mp:
                    can_unlock = True
            else:
                if profile.experience_points >= module.xp_required:
                    can_unlock = True
            if can_unlock:
                progress.unlock()
                progress.save()

@extend_schema(tags=['users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

@extend_schema(tags=['auth'])
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(tags=['users'])
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        print("PATCH /auth/me/ request.data:", request.data)
        profile = self.get_object()
        user = profile.user
        updated = False

        email = request.data.get('email')
        if email:
            user.email = email
            updated = True
        first_name = request.data.get('first_name')
        if first_name is not None:
            user.first_name = first_name
            updated = True
        last_name = request.data.get('last_name')
        if last_name is not None:
            user.last_name = last_name
            updated = True
        if updated:
            user.save()
            profile = self.get_object()
            user.refresh_from_db()
            print("Usuario actualizado:", user.email, user.first_name, user.last_name)
        else:
            print("No se actualizaron campos de usuario.")

        # Devuelve el perfil actualizado con los datos del usuario
        serializer = self.get_serializer(profile)
        # Para máxima compatibilidad, devuelve la misma estructura que el GET
        data = serializer.data
        return Response(data)

# NUEVA VISTA PARA UPDATE DE PERFIL (SOLO EMAIL, NOMBRE, APELLIDO)
@extend_schema(tags=['users'])
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

@extend_schema(tags=['modules'])
class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Devuelve todos los módulos para el usuario autenticado
        return Module.objects.all()

@extend_schema(
    tags=['modules'],
    parameters=[
        OpenApiParameter(
            name='module_id',
            type=str,
            location=OpenApiParameter.PATH,
            description='ID of the module to unlock',
            required=True
        )
    ]
)
class ModuleUnlockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModuleProgressSerializer
    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        user = request.user
        profile = user.profile

        # Lógica de requisitos personalizados
        can_unlock = False
        error_msg = ""
        if module.id == "salud":
            if profile.experience_points >= module.xp_required:
                can_unlock = True
            else:
                error_msg = f"Necesitas al menos {module.xp_required} XP para desbloquear Salud."
        elif module.id == "personalidad":
            # XP y misión global
            has_xp = profile.experience_points >= 200
            try:
                from .models import Mission, MissionProgress
                mission = Mission.objects.get(id="46e39fc7-8a77-4e39-9559-283a73655d12")
                mp = MissionProgress.objects.filter(user=user, mission=mission, state="completed").exists()
            except Exception:
                mp = False
            if has_xp and mp:
                can_unlock = True
            elif not has_xp:
                error_msg = "Necesitas al menos 200 XP para desbloquear Personalidad."
            elif not mp:
                error_msg = "Debes completar la misión global de racha de 1 día para desbloquear Personalidad."
        else:
            # Otros módulos: solo XP
            if profile.experience_points >= module.xp_required:
                can_unlock = True
            else:
                error_msg = f"Necesitas al menos {module.xp_required} XP para desbloquear este módulo."

        if not can_unlock:
            return Response(
                {"error": error_msg or "No cumples los requisitos para desbloquear este módulo."},
                status=status.HTTP_403_FORBIDDEN
            )

        progress, created = ModuleProgress.objects.get_or_create(
            user=user,
            module=module
        )
        if progress.state == 'locked':
            progress.unlock()
            progress.save()
        return Response(
            ModuleProgressSerializer(progress).data,
            status=status.HTTP_200_OK
        )

@extend_schema(tags=['missions'])
class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        unlocked_modules = ModuleProgress.objects.filter(
            user=user,
            state='unlocked'
        ).values_list('module_id', flat=True)
        return Mission.objects.filter(module_id__in=unlocked_modules)

@extend_schema(
    tags=['missions'],
    parameters=[
        OpenApiParameter(
            name='mission_id',
            type=str,
            location=OpenApiParameter.PATH,
            description='UUID of the mission to complete',
            required=True,
            pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        )
    ]
)
class MissionCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MissionProgressSerializer
    def post(self, request, mission_id):
        try:
            if not isinstance(mission_id, UUID):
                mission_id = UUID(str(mission_id))
        except ValueError:
            return Response(
                {"error": "Invalid mission ID format"},
                status=status.HTTP_400_BAD_REQUEST
            )
        mission = get_object_or_404(Mission, id=mission_id)
        user = request.user
        module_progress = get_object_or_404(
            ModuleProgress,
            user=user,
            module=mission.module
        )
        if module_progress.state == 'locked':
            return Response(
                {"error": "Module is locked"},
                status=status.HTTP_403_FORBIDDEN
            )
        progress, created = MissionProgress.objects.get_or_create(
            user=user,
            mission=mission
        )
        if progress.state != 'completed':
            progress.complete()
            progress.save()
            profile = user.profile
            profile.experience_points += mission.xp_reward
            profile.calculate_level()
            profile.save()
            streak, _ = Streak.objects.get_or_create(
                user=user,
                module=mission.module
            )
            streak.update_streak()
        return Response(
            MissionProgressSerializer(progress).data,
            status=status.HTTP_200_OK
        )

@extend_schema(tags=['progress'])
class ProgressOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProgressOverviewSerializer
    def get(self, request):
        user = request.user
        # --- Sincroniza desbloqueo de módulos antes de devolver el progreso ---
        sync_module_unlocks(user)
        profile = user.profile
        modules_unlocked = ModuleProgress.objects.filter(
            user=user,
            state='unlocked'
        ).count()
        missions_completed = MissionProgress.objects.filter(
            user=user,
            state='completed'
        ).count()
        achievements_earned = UserAchievement.objects.filter(
            user=user
        ).count()
        streaks = Streak.objects.filter(user=user)
        current_streaks = {
            streak.module.id: streak.current_streak
            for streak in streaks
        }
        data = {
            'total_xp': profile.experience_points,
            'level': profile.current_level,
            'modules_unlocked': modules_unlocked,
            'missions_completed': missions_completed,
            'achievements_earned': achievements_earned,
            'current_streaks': current_streaks,
            'title': profile.get_level_title()
        }
        return Response(
            ProgressOverviewSerializer(data).data,
            status=status.HTTP_200_OK
        )

@extend_schema(
    tags=['progress'],
    parameters=[
        OpenApiParameter(
            name='module_id',
            type=str,
            location=OpenApiParameter.PATH,
            description='ID of the module to get progress for',
            required=True
        )
    ]
)
class ModuleProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ModuleProgressSerializer
    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        user = request.user
        # --- Sincroniza desbloqueo de módulos antes de devolver el progreso de uno ---
        sync_module_unlocks(user)
        progress, _ = ModuleProgress.objects.get_or_create(
            user=user,
            module=module
        )
        missions = MissionProgress.objects.filter(
            user=user,
            mission__module=module
        )
        streak, _ = Streak.objects.get_or_create(
            user=user,
            module=module
        )
        data = {
            'progress': ModuleProgressSerializer(progress).data,
            'missions': MissionProgressSerializer(missions, many=True).data,
            'streak': StreakSerializer(streak).data
        }
        return Response(data, status=status.HTTP_200_OK)

# --- Pilares desbloqueados ---
@extend_schema(tags=['pillars'])
class UnlockedPillarViewSet(viewsets.ModelViewSet):
    """ViewSet for unlocked pillars."""
    queryset = UnlockedPillar.objects.all()
    serializer_class = UnlockedPillarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = UnlockedPillar.objects.filter(user=user)
        module_id = self.request.query_params.get('module')
        if module_id:
            queryset = queryset.filter(module__id=module_id)
        return queryset

    def perform_create(self, serializer):
        try:
            dificultad = serializer.validated_data.get('dificultad')
            ataque = 1
            if dificultad == 'media':
                ataque = 3
            elif dificultad == 'difícil':
                ataque = 9
            serializer.save(user=self.request.user)
        except Exception as e:
            from django.db import IntegrityError
            if isinstance(e, IntegrityError):
                from rest_framework.exceptions import ValidationError
                raise ValidationError({'detail': 'Este pilar ya está desbloqueado para este usuario y módulo.'})
            raise

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        hp_actual = request.data.get('hp_actual')
        updated = False
        if hp_actual is not None:
            try:
                hp_actual = float(hp_actual)
            except Exception:
                pass
            if hp_actual <= 0:
                # Subir de nivel el muro
                instance.nivel_muro += 1
                instance.hp_max += 100
                instance.hp_actual = instance.hp_max
                updated = True
        if not updated:
            return super().partial_update(request, *args, **kwargs)
        instance.fecha_ultimo_ataque = request.data.get('fecha_ultimo_ataque', instance.fecha_ultimo_ataque)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# --- Declaraciones ---
@extend_schema(tags=['declarations'])
class DeclarationViewSet(viewsets.ModelViewSet):
    """ViewSet for user declarations."""
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        queryset = Declaration.objects.filter(user=user)
        module_id = self.request.query_params.get('module')
        pillar = self.request.query_params.get('pillar')
        if module_id:
            queryset = queryset.filter(module__id=module_id)
        if pillar:
            queryset = queryset.filter(pillar=pillar)
        return queryset
    def perform_create(self, serializer):
        # Guardar la declaración con el usuario actual
        declaration = serializer.save(user=self.request.user)
        user = self.request.user
        module = declaration.module
        pillar = declaration.pillar

        # Verificar si ya existe una declaración previa en este pilar/módulo para este usuario
        exists = Declaration.objects.filter(
            user=user,
            module=module,
            pillar=pillar
        ).exclude(id=declaration.id).exists()

        if not exists:
            # Calcular experiencia: base 20 + 10 * (orden-1)
            base_xp = 20
            xp = base_xp + 10 * (module.order - 1)
            profile = user.profile
            profile.experience_points += xp
            profile.calculate_level()
            profile.save()
        # Actualizar streak diario al crear declaración
        streak, _ = Streak.objects.get_or_create(user=user, module=module)
        streak.update_streak()

        # --- Lógica de misiones delegada a utils ---
        from api.utils.mission_logic import check_and_complete_missions
        check_and_complete_missions(user, module, pillar)

# --- Hábitos (serpiente) ---
@extend_schema(tags=['habits'])
class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet for user habits (serpientes)."""
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = __import__('api.models').models.Habit.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# --- Muro de confort (zona de confort) ---
@extend_schema(tags=['comfortwall'])
class ComfortWallViewSet(viewsets.ModelViewSet):
    """ViewSet for user's comfort wall (zona de confort)."""
    serializer_class = ComfortWallSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = __import__('api.models').models.ComfortWall.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        hp_actual = request.data.get('hp_actual')
        updated = False
        if hp_actual is not None:
            try:
                hp_actual = float(hp_actual)
            except Exception:
                pass
            if hp_actual <= 0:
                # Subir de nivel el muro
                instance.nivel_muro += 1
                instance.hp_max += 100
                instance.hp_actual = instance.hp_max
                updated = True
        if not updated:
            return super().partial_update(request, *args, **kwargs)
        instance.fecha_ultimo_ataque = request.data.get('fecha_ultimo_ataque', instance.fecha_ultimo_ataque)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# --- Achievements (logros) ---
class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- User Missions APIView ---
class UserMissionsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        from .models import Mission, MissionProgress, Declaration, ModuleProgress
        from datetime import timedelta

        now = timezone.now()
        today = now.date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        # Misiones globales
        global_missions = Mission.objects.filter(module__isnull=True)
        # Todas las misiones de módulos (desbloqueados o no)
        module_missions = Mission.objects.filter(module__isnull=False)
        # Módulos desbloqueados por el usuario
        unlocked_modules = set(ModuleProgress.objects.filter(
            user=user,
            state='unlocked'
        ).values_list('module_id', flat=True))

        # Progreso de usuario
        declarations_today = Declaration.objects.filter(user=user, created_at__date=today).count()
        declarations_this_week = Declaration.objects.filter(user=user, created_at__date__gte=week_start, created_at__date__lte=week_end)
        days_with_declaration = declarations_this_week.values_list('created_at__date', flat=True).distinct()
        modules_unlocked_this_week = ModuleProgress.objects.filter(
            user=user,
            state='unlocked',
            last_activity__date__gte=week_start,
            last_activity__date__lte=week_end,
            auto_unlocked=False
        ).count()

        result = []

        # Global missions
        for mission in global_missions:
            mp = MissionProgress.objects.filter(user=user, mission=mission).first()
            state = mp.state if mp else "active"
            progress = None
            frequency = getattr(mission, "frequency", None)
            if hasattr(mission, "frequency"):
                frequency = mission.frequency
            elif hasattr(mission, "fields") and "frequency" in mission.fields:
                frequency = mission.fields["frequency"]
            # Daily
            if frequency == "daily":
                progress = {
                    "current": declarations_today,
                    "target": 1,
                    "label": f"{declarations_today}/1 declaraciones hoy"
                }
                if declarations_today >= 1:
                    state = "completed"
            # Weekly streak
            elif frequency == "weekly" and "racha" in mission.title.lower():
                # Usar la racha real del usuario (Streak)
                from .models import Streak
                streak = Streak.objects.filter(user=user, module__isnull=True).first()
                current_streak = streak.current_streak if streak else 0
                progress = {
                    "current": current_streak,
                    "target": 5,
                    "label": f"{current_streak}/5 días de racha consecutiva"
                }
                if current_streak >= 5:
                    state = "completed"
            # Weekly unlock
            elif frequency == "weekly" and "desbloquea" in mission.title.lower():
                progress = {
                    "current": modules_unlocked_this_week,
                    "target": 1,
                    "label": f"{modules_unlocked_this_week}/1 módulos desbloqueados esta semana"
                }
                if modules_unlocked_this_week >= 1:
                    state = "completed"
            result.append({
                "id": str(mission.id),
                "title": mission.title,
                "description": mission.description,
                "xp_reward": mission.xp_reward,
                "frequency": frequency,
                "requirements": getattr(mission, "requirements", []),
                "type": "global",
                "state": state,
                "progress": progress,
                "started_at": mp.started_at if mp else None,
                "completed_at": mp.completed_at if mp else None,
            })

        # Module missions
        for mission in module_missions:
            mp = MissionProgress.objects.filter(user=user, mission=mission).first()
            # Si el módulo está desbloqueado, usar el estado real; si no, marcar como "blocked"
            if mission.module and str(mission.module.id) in unlocked_modules:
                state = mp.state if mp else "active"
            else:
                state = "blocked"
            result.append({
                "id": str(mission.id),
                "title": mission.title,
                "description": mission.description,
                "xp_reward": mission.xp_reward,
                "frequency": getattr(mission, "frequency", None),
                "requirements": getattr(mission, "requirements", []),
                "type": "module",
                "module_id": str(mission.module.id) if mission.module else None,
                "state": state,
                "progress": None,
                "started_at": mp.started_at if mp else None,
                "completed_at": mp.completed_at if mp else None,
            })

        return Response(result)
