from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
from topics.models import PhysicsTopic


class Simulation(models.Model):
    """Interactive physics simulations"""
    SIMULATION_TYPES = [
        ('motion', 'Motion & Mechanics'),
        ('electricity', 'Electricity & Magnetism'),
        ('optics', 'Optics & Light'),
        ('waves', 'Waves & Sound'),
        ('thermodynamics', 'Thermodynamics'),
        ('quantum', 'Quantum Physics'),
        ('relativity', 'Relativity'),
    ]
    
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, related_name='simulations')
    title = models.CharField(max_length=200)
    description = models.TextField()
    simulation_type = models.CharField(max_length=20, choices=SIMULATION_TYPES)
    html_content = models.TextField(help_text="HTML/JavaScript simulation code")
    css_content = models.TextField(blank=True, help_text="Custom CSS for simulation")
    js_content = models.TextField(blank=True, help_text="JavaScript code for simulation")
    parameters = models.JSONField(default=dict, help_text="Simulation parameters and default values")
    learning_objectives = models.TextField(help_text="What students will learn from this simulation")
    instructions = models.TextField(help_text="How to use the simulation")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='beginner')
    is_interactive = models.BooleanField(default=True)
    estimated_duration = models.PositiveIntegerField(help_text="Estimated time in minutes", default=10)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['topic__grade__order', 'topic__order', 'order']
    
    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class SimulationParameter(models.Model):
    """Configurable parameters for simulations"""
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='parameters_list')
    name = models.CharField(max_length=100)
    parameter_type = models.CharField(max_length=20, choices=[
        ('slider', 'Slider'),
        ('input', 'Text Input'),
        ('dropdown', 'Dropdown'),
        ('checkbox', 'Checkbox'),
        ('color', 'Color Picker'),
    ])
    default_value = models.CharField(max_length=200)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    step = models.FloatField(null=True, blank=True)
    options = models.JSONField(blank=True, null=True, help_text="Options for dropdown parameters")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.simulation.title} - {self.name}"


class SimulationSession(models.Model):
    """Track user interactions with simulations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulation_sessions')
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in seconds")
    parameters_used = models.JSONField(default=dict, help_text="Parameters user experimented with")
    interactions_count = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.simulation.title}"


class SimulationFeedback(models.Model):
    """User feedback and learning outcomes from simulations"""
    session = models.OneToOneField(SimulationSession, on_delete=models.CASCADE, related_name='feedback')
    understanding_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], 
                                                     help_text="Rate your understanding (1-5)")
    difficulty_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], 
                                                   help_text="Rate difficulty (1-5)")
    helpful_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], 
                                                help_text="Rate helpfulness (1-5)")
    comments = models.TextField(blank=True)
    concepts_learned = models.TextField(blank=True, help_text="What concepts did you learn?")
    questions_arose = models.TextField(blank=True, help_text="What questions do you have?")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.session.simulation.title} by {self.session.user.username}"