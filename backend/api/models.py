# -*- coding: utf-8 -*-
"""
Data models for the Dividis application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_fsm import FSMField, transition
from django.conf import settings
import uuid

import json
import os

class LevelTitle(models.Model):
    level = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Nivel {self.level}: {self.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experience_points = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)

    # Cargar títulos de nivel una sola vez
    _level_titles = None

    @classmethod
    def get_titles_dict(cls):
        if cls._level_titles is None:
            fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "level_titles.json")
            with open(fixture_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                cls._level_titles = {item["level"]: item["title"] for item in data}
        return cls._level_titles

    def get_level_title(self):
        titles = self.get_titles_dict()
        return titles.get(self.current_level, "Aventurero")

    def __str__(self):
        return f"{self.user.username}'s profile"
    def calculate_level(self):
        self.current_level = (self.experience_points // 100) + 1
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        # Desbloquear automáticamente el primer módulo (orden 1)
        from .models import Module, ModuleProgress
        first_module = Module.objects.order_by('order').first()
        if first_module:
            progress, _ = ModuleProgress.objects.get_or_create(user=instance, module=first_module)
            if progress.state == 'locked':
                progress.unlock()
                progress.auto_unlocked = True
                progress.save()

class Module(models.Model):
    STATES = (
        ('locked', 'Locked'),
        ('unlocked', 'Unlocked'),
        ('completed', 'Completed'),
    )
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    order = models.IntegerField()
    xp_required = models.IntegerField(default=0)
    state = FSMField(default='locked', choices=STATES)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.name
    @transition(field=state, source='locked', target='unlocked')
    def unlock(self):
        self.state = 'unlocked'
        self.save(update_fields=['state'])
    @transition(field=state, source='unlocked', target='completed')
    def complete(self):
        pass

class ModuleProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    state = FSMField(default='locked', choices=Module.STATES)
    experience_points = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    auto_unlocked = models.BooleanField(default=False)  # Nuevo campo

    class Meta:
        unique_together = ['user', 'module']
    def __str__(self):
        return f"{self.user.username}'s progress in {self.module.name}"
    @transition(field=state, source='locked', target='unlocked')
    def unlock(self):
        self.state = 'unlocked'
        self.save(update_fields=['state'])
    @transition(field=state, source='unlocked', target='completed')
    def complete(self):
        pass

from django.db.models import JSONField

class Mission(models.Model):
    STATES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    FREQUENCY_CHOICES = [
        ('global', 'Global'),
        ('daily', 'Diaria'),
        ('weekly', 'Semanal'),
        (None, 'Sin frecuencia'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    xp_reward = models.IntegerField(default=settings.DEFAULT_MISSION_POINTS)
    required_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, null=True, blank=True, default=None)
    requirements = JSONField(default=list, blank=True)  # Nuevo campo para requisitos
    def __str__(self):
        return self.title

class MissionProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    state = FSMField(default='active', choices=Mission.STATES)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        unique_together = ['user', 'mission']
    def __str__(self):
        return f"{self.user.username}'s progress on {self.mission.title}"
    @transition(field=state, source='active', target='completed')
    def complete(self):
        from django.utils import timezone
        self.completed_at = timezone.now()
    @transition(field=state, source='active', target='failed')
    def fail(self):
        pass

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    xp_reward = models.IntegerField(default=100)
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'achievement']
    def __str__(self):
        return f"{self.user.username} unlocked {self.achievement.name}"

class Streak(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ['user', 'module']
    def __str__(self):
        return f"{self.user.username}'s streak in {self.module.name}"
    def update_streak(self):
        from django.utils import timezone
        now = timezone.now()
        if (now - self.last_activity).days <= 1:
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            self.current_streak = 1
        self.last_activity = now
        self.save()

        # --- Lógica para misión global de racha de 1 día ---
        if self.current_streak >= 1:
            try:
                from .models import Mission, MissionProgress
                mission = Mission.objects.get(id="46e39fc7-8a77-4e39-9559-283a73655d12")
                mp, created = MissionProgress.objects.get_or_create(user=self.user, mission=mission)
                if mp.state != "completed":
                    mp.complete()
                    mp.save()
            except Mission.DoesNotExist:
                pass

class Declaration(models.Model):
    PILLAR_CHOICES = [
        ('Vision', 'Visión'),
        ('Proposito', 'Propósito'),
        ('Creencias', 'Creencias'),
        ('Estrategias', 'Estrategias'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    pillar = models.CharField(max_length=20, choices=PILLAR_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    synced = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'module', 'pillar', 'text']
    def __str__(self):
        return f"{self.user.username} - {self.module.name} - {self.pillar}: {self.text[:30]}"

class UnlockedPillar(models.Model):
    """Pilares desbloqueados por usuario en un módulo/área."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    pillar = models.CharField(max_length=20)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'module', 'pillar']
    def __str__(self):
        return f"{self.user.username} - {self.module.name} - {self.pillar}"

class Habit(models.Model):
    DIFFICULTY_CHOICES = [
        ('fácil', 'Fácil'),
        ('media', 'Media'),
        ('difícil', 'Difícil'),
    ]
    STATE_CHOICES = [
        ('activo', 'Activo'),
        ('incubando', 'Incubando'),
        ('inactivo', 'Inactivo'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=64)
    dificultad = models.CharField(max_length=16, choices=DIFFICULTY_CHOICES)
    horario_sugerido = models.TimeField(null=True, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    dias_activos = models.PositiveIntegerField(default=0)
    estrellas = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    nivel = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=16, choices=STATE_CHOICES, default='incubando')
    ataque = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    def __str__(self):
        return f"{self.nombre} ({self.user.username})"

class ComfortWall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hp_actual = models.FloatField(default=100)
    hp_max = models.FloatField(default=100)
    nivel_muro = models.PositiveIntegerField(default=1)
    fecha_ultimo_ataque = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"Muro de {self.user.username} (Nivel {self.nivel_muro})"

# --- DESBLOQUEO SECUENCIAL DE CONSTELACIONES ---
from django.db.models.signals import post_save
from django.dispatch import receiver

import logging

@receiver(post_save, sender=Declaration)
def check_and_unlock_next_module(sender, instance, created, **kwargs):
    """
    Cuando el usuario tiene al menos una declaración en cada pilar de un módulo,
    desbloquea el siguiente módulo (constelación) en orden.
    """
    logger = logging.getLogger("api.models")
    if not created:
        return

    user = instance.user
    module = instance.module

    # Obtener todos los pilares requeridos para el módulo actual
    required_pillars = [choice[0] for choice in Declaration.PILLAR_CHOICES]

    # Verificar si el usuario tiene al menos una declaración en cada pilar de este módulo
    user_pillars = Declaration.objects.filter(
        user=user,
        module=module
    ).values_list('pillar', flat=True).distinct()

    logger.info(f"[DEBUG] Declaraciones para usuario {user.username} en módulo {module.id}: {list(user_pillars)}")
    logger.info(f"[DEBUG] Pilares requeridos: {required_pillars}")

    if set(required_pillars).issubset(set(user_pillars)):
        logger.info(f"[DEBUG] Usuario {user.username} completó todos los pilares de {module.id}. Intentando desbloquear siguiente módulo...")
        # Buscar el siguiente módulo por orden
        next_module = Module.objects.filter(order__gt=module.order).order_by('order').first()
        if next_module:
            logger.info(f"[DEBUG] Siguiente módulo a desbloquear: {next_module.id}")
            # Desbloquear el siguiente módulo para el usuario
            progress, created = ModuleProgress.objects.get_or_create(user=user, module=next_module)
            logger.info(f"[DEBUG] Estado actual de ModuleProgress: {progress.state}")
            if progress.state == 'locked':
                progress.unlock()
                progress.save()
                logger.info(f"[DEBUG] Módulo {next_module.id} desbloqueado para {user.username}")
            else:
                logger.info(f"[DEBUG] Módulo {next_module.id} ya estaba desbloqueado para {user.username}")
        else:
            logger.info(f"[DEBUG] No hay siguiente módulo para desbloquear.")
    else:
        logger.info(f"[DEBUG] Usuario {user.username} aún no tiene declaraciones en todos los pilares de {module.id}")
