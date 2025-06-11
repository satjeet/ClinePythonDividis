# -*- coding: utf-8 -*-
"""
URL patterns for the API app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'modules', views.ModuleViewSet)
router.register(r'missions', views.MissionViewSet)
router.register(r'declarations', views.DeclarationViewSet)
router.register(r'unlocked-pillars', views.UnlockedPillarViewSet)
router.register(r'habits', views.HabitViewSet)
router.register(r'comfortwall', views.ComfortWallViewSet)
router.register(r'achievements', views.AchievementViewSet)  # <-- NUEVO

# Rutas personalizadas primero para evitar conflictos con el router DRF
urlpatterns = [
    # Auth endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/me/', views.UserProfileView.as_view(), name='me'),
    path('auth/me/update/', views.UserProfileUpdateView.as_view(), name='profile-update'),

    # Module specific endpoints
    path('modules/<str:module_id>/unlock/', views.ModuleUnlockView.as_view(), name='module-unlock'),
    path('missions/<uuid:mission_id>/complete/', views.MissionCompleteView.as_view(), name='mission-complete'),

    # Global missions endpoint
    path('missions/global/', views.GlobalMissionListView.as_view(), name='global-missions'),

    # Progress endpoints
    path('progress/overview/', views.ProgressOverviewView.as_view(), name='progress-overview'),
    path('progress/module/<str:module_id>/', views.ModuleProgressView.as_view(), name='module-progress'),

    # Router URLs (dejar al final)
    path('', include(router.urls)),
]
