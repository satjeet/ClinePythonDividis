"""
Serializers relacionados con el modelo Profile.
"""

from rest_framework import serializers
from .user_serializers import UserSerializer, UserWriteSerializer
from ..models import Profile
from ..utils.serializers_helpers import (
    get_title, get_first_name, get_last_name, update_user_fields, get_active_missions
)

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profiles."""
    user = UserSerializer(read_only=True)
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return get_title(obj)
    
    class Meta:
        model = Profile
        fields = ('user', 'experience_points', 'current_level', 'created_at', 'updated_at', 'title')
        read_only_fields = ('created_at', 'updated_at')

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer específico para actualizar datos del perfil de usuario."""
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        update_user_fields(user, user_data)
        return instance

    def to_representation(self, instance):
        return {
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name
        }

class UserProfileDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for user profile with related data."""
    user = UserSerializer(read_only=True)
    user_write = UserWriteSerializer(write_only=True, required=False)
    module_progress = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    streaks = serializers.SerializerMethodField()
    active_missions = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return get_title(obj)

    def get_module_progress(self, obj):
        from .module_serializers import ModuleProgressSerializer
        from ..models import ModuleProgress
        return ModuleProgressSerializer(ModuleProgress.objects.filter(user=obj.user), many=True).data

    def get_achievements(self, obj):
        from .achievement_serializers import UserAchievementSerializer
        from ..models import UserAchievement
        return UserAchievementSerializer(UserAchievement.objects.filter(user=obj.user), many=True).data

    def get_streaks(self, obj):
        from .streak_serializers import StreakSerializer
        from ..models import Streak
        return StreakSerializer(Streak.objects.filter(user=obj.user), many=True).data

    def get_active_missions(self, obj):
        from drf_spectacular.utils import extend_schema_field
        from .mission_serializers import MissionProgressSerializer
        active_missions = get_active_missions(obj.user)
        return MissionProgressSerializer(active_missions, many=True).data

    def get_first_name(self, obj):
        return get_first_name(obj)

    def get_last_name(self, obj):
        return get_last_name(obj)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user_write', None)
        if user_data:
            user = instance.user
            update_user_fields(user, user_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Profile
        fields = (
            'user', 'user_write', 'experience_points', 'current_level', 'created_at',
            'updated_at', 'module_progress', 'achievements', 'streaks',
            'active_missions', 'first_name', 'last_name', 'title'
        )
        read_only_fields = ('created_at', 'updated_at')
