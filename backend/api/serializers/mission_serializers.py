"""
Serializers relacionados con el modelo Mission y MissionProgress.
"""

from rest_framework import serializers
from ..models import Mission, MissionProgress
from .module_serializers import ModuleSerializer

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
