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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experience_points = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.user.username}'s profile"
    def calculate_level(self):
        self.current_level = (self.experience_points // 100) + 1
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

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
        pass
    @transition(field=state, source='unlocked', target='completed')
    def complete(self):
        pass

class ModuleProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    state = FSMField(default='locked', choices=Module.STATES)
    experience_points = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ['user', 'module']
    def __str__(self):
        return f"{self.user.username}'s progress in {self.module.name}"
    @transition(field=state, source='locked', target='unlocked')
    def unlock(self):
        pass
    @transition(field=state, source='unlocked', target='completed')
    def complete(self):
        pass

class Mission(models.Model):
    STATES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    xp_reward = models.IntegerField(default=settings.DEFAULT_MISSION_POINTS)
    required_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
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
