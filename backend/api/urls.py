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

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Auth endpoints
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/me/', views.UserProfileView.as_view(), name='me'),
    
    # Module specific endpoints
    path('modules/<str:module_id>/unlock/', views.ModuleUnlockView.as_view(), name='module-unlock'),
    path('missions/<uuid:mission_id>/complete/', views.MissionCompleteView.as_view(), name='mission-complete'),
    
    # Progress endpoints
    path('progress/overview/', views.ProgressOverviewView.as_view(), name='progress-overview'),
    path('progress/module/<str:module_id>/', views.ModuleProgressView.as_view(), name='module-progress'),
]
