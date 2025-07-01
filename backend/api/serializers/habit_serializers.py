"""
Serializers relacionados con el modelo Habit.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class HabitSerializer(serializers.ModelSerializer):
    """Serializer for Habit (serpiente/hábito)."""
    user = UserSerializer(read_only=True)
    class Meta:
        model = __import__('api.models').models.Habit
        fields = (
            'id', 'user', 'nombre', 'dificultad', 'horario_sugerido',
            'fecha_creacion', 'dias_activos', 'estrellas', 'nivel', 'estado', 'ataque'
        )
        read_only_fields = ('id', 'user', 'fecha_creacion', 'dias_activos', 'estrellas', 'nivel', 'estado')
