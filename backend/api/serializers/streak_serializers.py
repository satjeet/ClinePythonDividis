"""
Serializers relacionados con el modelo Streak.
"""

from rest_framework import serializers
from ..models import Streak
from .module_serializers import ModuleSerializer

class StreakSerializer(serializers.ModelSerializer):
    """Serializer for activity streaks."""
    module = ModuleSerializer(read_only=True)
    
    class Meta:
        model = Streak
        fields = ('module', 'current_streak', 'longest_streak', 'last_activity')
        read_only_fields = ('last_activity',)
