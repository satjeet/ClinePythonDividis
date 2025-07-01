"""
Helpers para serializers de la API Dividis.
Extrae lógica auxiliar y repetida para mantener serializers limpios y profesionales.
"""

from typing import Any, Optional
from django.contrib.auth.models import User

def get_title(profile) -> str:
    """Devuelve el título de nivel del perfil."""
    return profile.get_level_title() if hasattr(profile, "get_level_title") else ""

def get_first_name(profile) -> str:
    """Devuelve el primer nombre del usuario asociado al perfil."""
    return profile.user.first_name if hasattr(profile, "user") else ""

def get_last_name(profile) -> str:
    """Devuelve el apellido del usuario asociado al perfil."""
    return profile.user.last_name if hasattr(profile, "user") else ""

def update_user_fields(user: User, user_data: dict) -> None:
    """
    Actualiza los campos básicos del usuario.
    """
    for attr, value in user_data.items():
        setattr(user, attr, value)
    user.save()

def get_state(module, context: dict) -> Any:
    """
    Devuelve el estado del módulo para el usuario autenticado en el contexto.
    """
    user = context.get('request').user if context.get('request') else None
    if user and user.is_authenticated:
        from api.models import ModuleProgress
        try:
            progress = ModuleProgress.objects.get(user=user, module=module)
            return progress.state
        except ModuleProgress.DoesNotExist:
            pass
    return getattr(module, "state", None)

def get_active_missions(user: User):
    """
    Devuelve los MissionProgress activos para un usuario.
    """
    from api.models import MissionProgress
    return MissionProgress.objects.filter(user=user, state='active').select_related('mission')
