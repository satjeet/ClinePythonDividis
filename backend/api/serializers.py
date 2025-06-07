"""
Serializers for the Dividis API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import (
    Profile, Module, ModuleProgress, Mission, MissionProgress,
    Achievement, UserAchievement, Streak
)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ('user', 'experience_points', 'current_level', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for modules."""
    state = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ('id', 'name', 'description', 'icon', 'order', 'xp_required', 'state')

    def get_state(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            from .models import ModuleProgress
            try:
                progress = ModuleProgress.objects.get(user=user, module=obj)
                return progress.state
            except ModuleProgress.DoesNotExist:
                pass
        return obj.state

class ModuleProgressSerializer(serializers.ModelSerializer):
    """Serializer for module progress."""
    module = ModuleSerializer(read_only=True)
    
    class Meta:
        model = ModuleProgress
        fields = ('module', 'state', 'experience_points', 'last_activity')
        read_only_fields = ('last_activity',)

class MissionSerializer(serializers.ModelSerializer):
    """Serializer for missions."""
    module = ModuleSerializer(read_only=True)
    
    class Meta:
        model = Mission
        fields = ('id', 'module', 'title', 'description', 'xp_reward', 'required_level', 'created_at')
        read_only_fields = ('id', 'created_at')

class MissionProgressSerializer(serializers.ModelSerializer):
    """Serializer for mission progress."""
    mission = MissionSerializer(read_only=True)
    
    class Meta:
        model = MissionProgress
        fields = ('mission', 'state', 'started_at', 'completed_at')
        read_only_fields = ('started_at', 'completed_at')

class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for achievements."""
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'icon', 'xp_reward')

class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for user achievements."""
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ('achievement', 'unlocked_at')
        read_only_fields = ('unlocked_at',)

class StreakSerializer(serializers.ModelSerializer):
    """Serializer for activity streaks."""
    module = ModuleSerializer(read_only=True)
    
    class Meta:
        model = Streak
        fields = ('module', 'current_streak', 'longest_streak', 'last_activity')
        read_only_fields = ('last_activity',)

class UserProfileDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for user profile with related data."""
    user = UserSerializer(read_only=True)
    module_progress = ModuleProgressSerializer(many=True, read_only=True, source='moduleprogressset')
    achievements = UserAchievementSerializer(many=True, read_only=True, source='userachievement_set')
    streaks = StreakSerializer(many=True, read_only=True, source='streak_set')
    active_missions = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'user', 'experience_points', 'current_level', 'created_at',
            'updated_at', 'module_progress', 'achievements', 'streaks',
            'active_missions'
        )
        read_only_fields = ('created_at', 'updated_at')

    from drf_spectacular.utils import extend_schema_field
    from typing import Any

    @extend_schema_field(MissionProgressSerializer(many=True))
    def get_active_missions(self, obj) -> Any:
        active_missions = MissionProgress.objects.filter(
            user=obj.user,
            state='active'
        ).select_related('mission')
        return MissionProgressSerializer(active_missions, many=True).data

class ProgressOverviewSerializer(serializers.Serializer):
    """Serializer for user's overall progress."""
    total_xp = serializers.IntegerField()
    level = serializers.IntegerField()
    modules_unlocked = serializers.IntegerField()
    missions_completed = serializers.IntegerField()
    achievements_earned = serializers.IntegerField()
    current_streaks = serializers.DictField()

class DeclarationSerializer(serializers.ModelSerializer):
    """Serializer for user declarations."""
    class Meta:
        model = __import__('api.models').models.Declaration
        fields = ('id', 'user', 'module', 'pillar', 'text', 'created_at', 'updated_at', 'synced')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

class UnlockedPillarSerializer(serializers.ModelSerializer):
    """Serializer for unlocked pillars."""
    class Meta:
        model = __import__('api.models').models.UnlockedPillar
        fields = ('id', 'user', 'module', 'pillar', 'unlocked_at')
        read_only_fields = ('id', 'user', 'unlocked_at')
