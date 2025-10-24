from django.contrib import admin
from .models import Simulation, SimulationParameter, SimulationSession, SimulationFeedback


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'simulation_type', 'difficulty_level', 'is_active']
    list_filter = ['simulation_type', 'difficulty_level', 'is_active', 'topic__grade']
    search_fields = ['title', 'description', 'learning_objectives']
    list_editable = ['is_active']


@admin.register(SimulationParameter)
class SimulationParameterAdmin(admin.ModelAdmin):
    list_display = ['name', 'simulation', 'parameter_type', 'default_value', 'order']
    list_filter = ['parameter_type', 'simulation__topic__grade']
    search_fields = ['name', 'description']
    list_editable = ['order']


@admin.register(SimulationSession)
class SimulationSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'simulation', 'started_at', 'completed_at', 'is_completed']
    list_filter = ['is_completed', 'simulation__topic__grade']
    search_fields = ['user__username', 'simulation__title']
    readonly_fields = ['started_at']


@admin.register(SimulationFeedback)
class SimulationFeedbackAdmin(admin.ModelAdmin):
    list_display = ['session', 'understanding_rating', 'difficulty_rating', 'helpful_rating', 'created_at']
    list_filter = ['understanding_rating', 'difficulty_rating', 'helpful_rating']
    search_fields = ['session__user__username', 'session__simulation__title']
    readonly_fields = ['created_at']