"""
Serializers relacionados con el modelo Achievement y UserAchievement.
"""

from rest_framework import serializers
from ..models import Achievement, UserAchievement

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
