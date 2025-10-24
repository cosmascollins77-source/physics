from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
from topics.models import PhysicsTopic, CBCGrade
from quizzes.models import Quiz
from simulations.models import Simulation


class UserProfile(models.Model):
    """Extended user profile for physics learning"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_grade = models.ForeignKey(CBCGrade, on_delete=models.SET_NULL, null=True, blank=True)
    learning_goals = models.TextField(blank=True, help_text="Student's learning goals")
    preferred_learning_style = models.CharField(max_length=50, choices=[
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('kinesthetic', 'Kinesthetic'),
        ('reading', 'Reading/Writing'),
    ], default='visual')
    physics_background = models.CharField(max_length=50, choices=[
        ('beginner', 'Complete Beginner'),
        ('some_knowledge', 'Some Knowledge'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='beginner')
    time_available = models.PositiveIntegerField(default=30, help_text="Available study time per week in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"


class TopicProgress(models.Model):
    """Track user progress through physics topics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('mastered', 'Mastered'),
    ], default='not_started')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.PositiveIntegerField(default=0, help_text="Time spent in minutes")
    understanding_level = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], 
                                                     null=True, blank=True, help_text="Self-rated understanding (1-5)")
    notes = models.TextField(blank=True, help_text="Personal notes about the topic")
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'topic']
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.title} ({self.status})"


class LearningPath(models.Model):
    """Personalized learning paths for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topics = models.ManyToManyField(PhysicsTopic, related_name='learning_paths')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"


class Achievement(models.Model):
    """Learning achievements and badges"""
    ACHIEVEMENT_TYPES = [
        ('topic_completion', 'Topic Completion'),
        ('quiz_mastery', 'Quiz Mastery'),
        ('simulation_explorer', 'Simulation Explorer'),
        ('streak', 'Learning Streak'),
        ('speed_learner', 'Speed Learner'),
        ('perfectionist', 'Perfectionist'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    achievement_type = models.CharField(max_length=30, choices=ACHIEVEMENT_TYPES)
    icon = models.CharField(max_length=100, help_text="Icon class or name")
    criteria = models.JSONField(help_text="Criteria for earning this achievement")
    points = models.PositiveIntegerField(default=10, help_text="Points awarded")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """User earned achievements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='users')
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class StudySession(models.Model):
    """Track study sessions and learning analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    session_type = models.CharField(max_length=30, choices=[
        ('topic_study', 'Topic Study'),
        ('quiz_practice', 'Quiz Practice'),
        ('simulation_exploration', 'Simulation Exploration'),
        ('review', 'Review Session'),
    ])
    topic = models.ForeignKey(PhysicsTopic, on_delete=models.CASCADE, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duration in minutes")
    activities_completed = models.JSONField(default=list, help_text="List of completed activities")
    concepts_learned = models.TextField(blank=True)
    questions_asked = models.TextField(blank=True)
    satisfaction_rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], 
                                                           null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.session_type} ({self.started_at.date()})"


class LearningAnalytics(models.Model):
    """Aggregated learning analytics for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analytics')
    total_study_time = models.PositiveIntegerField(default=0, help_text="Total study time in minutes")
    topics_completed = models.PositiveIntegerField(default=0)
    quizzes_taken = models.PositiveIntegerField(default=0)
    simulations_explored = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0, help_text="Current learning streak in days")
    longest_streak = models.PositiveIntegerField(default=0, help_text="Longest learning streak in days")
    average_quiz_score = models.FloatField(null=True, blank=True)
    favorite_topics = models.JSONField(default=list, help_text="Most studied topics")
    learning_velocity = models.FloatField(default=0, help_text="Topics completed per week")
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Analytics"