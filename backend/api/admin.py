"""
Admin configuration for the API app.
"""
from django.contrib import admin
from .models import (
    Profile, Module, ModuleProgress, Mission,
    MissionProgress, Achievement, UserAchievement, Streak, LevelTitle
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_level', 'experience_points']
    search_fields = ['user__username']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'order', 'xp_required']
    search_fields = ['name']
    ordering = ['order']

@admin.register(ModuleProgress)
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'state']
    list_filter = ['state']
    search_fields = ['user__username', 'module__name']

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'module', 'xp_reward', 'required_level', 'frequency']
    list_filter = ['module', 'frequency']
    search_fields = ['title', 'description']
    readonly_fields = ['id']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'module', 'xp_reward', 'required_level', 'frequency', 'requirements', 'id')
        }),
    )

@admin.register(MissionProgress)
class MissionProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'mission', 'state']
    list_filter = ['state']
    search_fields = ['user__username', 'mission__title']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'xp_reward']
    search_fields = ['name']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'unlocked_at']
    search_fields = ['user__username', 'achievement__name']

@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'current_streak', 'longest_streak', 'last_activity']
    search_fields = ['user__username', 'module__name']

@admin.register(LevelTitle)
class LevelTitleAdmin(admin.ModelAdmin):
    list_display = ['level', 'title']
    search_fields = ['title']
