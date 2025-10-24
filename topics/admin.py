from django.contrib import admin
from .models import (
    CBCGrade, PhysicsTopic, TopicContent, TopicMedia, 
    TopicFormula, TopicExperiment
)


@admin.register(CBCGrade)
class CBCGradeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'order']
    list_editable = ['order']
    ordering = ['order']


@admin.register(PhysicsTopic)
class PhysicsTopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'grade', 'difficulty_level', 'estimated_duration', 'is_active']
    list_filter = ['grade', 'difficulty_level', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['prerequisites']


@admin.register(TopicContent)
class TopicContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'content_type', 'order', 'is_essential']
    list_filter = ['content_type', 'is_essential', 'topic__grade']
    search_fields = ['title', 'content']
    list_editable = ['order', 'is_essential']


@admin.register(TopicMedia)
class TopicMediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'media_type', 'order']
    list_filter = ['media_type', 'topic__grade']
    search_fields = ['title', 'description']
    list_editable = ['order']


@admin.register(TopicFormula)
class TopicFormulaAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'is_essential', 'order']
    list_filter = ['is_essential', 'topic__grade']
    search_fields = ['name', 'formula', 'description']
    list_editable = ['order', 'is_essential']


@admin.register(TopicExperiment)
class TopicExperimentAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'is_virtual', 'order']
    list_filter = ['is_virtual', 'topic__grade']
    search_fields = ['title', 'objective']
    list_editable = ['order']