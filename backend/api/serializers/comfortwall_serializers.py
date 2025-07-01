"""
Serializers relacionados con el modelo ComfortWall.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ComfortWallSerializer(serializers.ModelSerializer):
    """Serializer for ComfortWall (zona de confort/muro)."""
    user = UserSerializer(read_only=True)
    class Meta:
        model = __import__('api.models').models.ComfortWall
        fields = (
            'id', 'user', 'hp_actual', 'hp_max', 'nivel_muro', 'fecha_ultimo_ataque'
        )
        read_only_fields = ('id', 'user', 'nivel_muro', 'fecha_ultimo_ataque')
