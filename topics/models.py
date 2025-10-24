from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CBCGrade(models.Model):
    """Represents different grades in the CBC system"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name


class PhysicsTopic(models.Model):
    """Main physics topics aligned with CBC curriculum"""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    grade = models.ForeignKey(CBCGrade, on_delete=models.CASCADE, related_name='topics')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    learning_outcomes = models.TextField(help_text="CBC learning outcomes for this topic")
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='prerequisite_for')
    estimated_duration = models.PositiveIntegerField(help_text="Estimated time in minutes")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['grade__order', 'order']
    
    def __str__(self):
        return f"{self.grade.name} - {self.title}"


class TopicContent(models.Model):
    """Detailed content for each physics topic"""
    CONTENT_TYPES = [
        ('theory', 'Theory'),
        ('formula', 'Formula'),
        ('example', 'Example'),
        ('experiment', 'Experiment'),
        ('application', 'Real-world Application'),
    ]
    
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_essential = models.BooleanField(default=True, help_text="Essential for understanding the topic")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class TopicMedia(models.Model):
    """Multimedia content for topics"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('animation', 'Animation'),
        ('diagram', 'Diagram'),
        ('audio', 'Audio'),
    ]
    
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, related_name='media')
    content = models.ForeignKey(TopicContent, on_delete=models.CASCADE, related_name='media', null=True, blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='topic_media/')
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class TopicFormula(models.Model):
    """Physics formulas for each topic"""
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, related_name='formulas')
    name = models.CharField(max_length=200)
    formula = models.CharField(max_length=500, help_text="LaTeX format formula")
    description = models.TextField()
    variables = models.JSONField(help_text="Dictionary of variables and their descriptions")
    units = models.CharField(max_length=100, help_text="Result units")
    example_calculation = models.TextField(blank=True)
    is_essential = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.topic.title} - {self.name}"


class TopicExperiment(models.Model):
    """Virtual experiments for physics topics"""
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, related_name='experiments')
    title = models.CharField(max_length=200)
    objective = models.TextField()
    materials_needed = models.TextField()
    procedure = models.TextField()
    expected_results = models.TextField()
    safety_notes = models.TextField(blank=True)
    is_virtual = models.BooleanField(default=True)
    simulation_url = models.URLField(blank=True, help_text="Link to interactive simulation")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.topic.title} - {self.title}"