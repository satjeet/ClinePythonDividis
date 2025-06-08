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
    DeclarationSerializer, UnlockedPillarSerializer
)

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
        if profile.experience_points < module.xp_required:
            return Response(
                {"error": "Insufficient XP to unlock this module"},
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
            'current_streaks': current_streaks
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
        serializer.save(user=self.request.user)

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
