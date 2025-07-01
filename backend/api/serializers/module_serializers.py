"""
Serializers relacionados con el modelo Module y ModuleProgress.
"""

from rest_framework import serializers
from ..models import Module, ModuleProgress
from ..utils.serializers_helpers import get_state

class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for modules."""
    state = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ('id', 'name', 'description', 'icon', 'order', 'xp_required', 'state')

    def get_state(self, obj):
        return get_state(obj, self.context)

class ModuleProgressSerializer(serializers.ModelSerializer):
    """Serializer for module progress."""
    module = ModuleSerializer(read_only=True)
    
    class Meta:
        model = ModuleProgress
        fields = ('module', 'state', 'experience_points', 'last_activity')
        read_only_fields = ('last_activity',)
