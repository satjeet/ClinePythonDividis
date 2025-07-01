"""
Serializers misceláneos: Declaration, UnlockedPillar, ProgressOverview.
"""

from rest_framework import serializers
from ..models import Declaration, UnlockedPillar

class DeclarationSerializer(serializers.ModelSerializer):
    """Serializer for user declarations."""
    class Meta:
        model = Declaration
        fields = ('id', 'user', 'module', 'pillar', 'text', 'created_at', 'updated_at', 'synced')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

class UnlockedPillarSerializer(serializers.ModelSerializer):
    """Serializer for unlocked pillars."""
    class Meta:
        model = UnlockedPillar
        fields = ('id', 'user', 'module', 'pillar', 'unlocked_at')
        read_only_fields = ('id', 'user', 'unlocked_at')

class ProgressOverviewSerializer(serializers.Serializer):
    """Serializer for user's overall progress."""
    total_xp = serializers.IntegerField()
    level = serializers.IntegerField()
    modules_unlocked = serializers.IntegerField()
    missions_completed = serializers.IntegerField()
    achievements_earned = serializers.IntegerField()
    current_streaks = serializers.DictField()
