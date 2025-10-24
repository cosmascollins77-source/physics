from django.contrib import admin
from .models import (
    UserProfile, TopicProgress, LearningPath, Achievement, 
    UserAchievement, StudySession, LearningAnalytics
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_grade', 'preferred_learning_style', 'physics_background']
    list_filter = ['current_grade', 'preferred_learning_style', 'physics_background']
    search_fields = ['user__username', 'user__email']


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'status', 'understanding_level', 'last_accessed']
    list_filter = ['status', 'understanding_level', 'topic__grade']
    search_fields = ['user__username', 'topic__title']
    readonly_fields = ['last_accessed']


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'is_active', 'created_at']
    list_filter = ['is_active', 'user']
    search_fields = ['name', 'description', 'user__username']
    filter_horizontal = ['topics']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'achievement_type', 'points', 'is_active']
    list_filter = ['achievement_type', 'is_active']
    search_fields = ['name', 'description']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'earned_at']
    list_filter = ['achievement__achievement_type', 'earned_at']
    search_fields = ['user__username', 'achievement__name']
    readonly_fields = ['earned_at']


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'topic', 'started_at', 'duration', 'satisfaction_rating']
    list_filter = ['session_type', 'satisfaction_rating', 'topic__grade']
    search_fields = ['user__username', 'topic__title']
    readonly_fields = ['started_at']


@admin.register(LearningAnalytics)
class LearningAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_study_time', 'topics_completed', 'current_streak', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['user__username']
    readonly_fields = ['last_updated']