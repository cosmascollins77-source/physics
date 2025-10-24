from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Extended user model for physics learning platform"""
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Administrator'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=200, blank=True)
    grade_level = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True, max_length=500)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class TeacherProfile(models.Model):
    """Extended profile for teachers"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    subject_specialization = models.CharField(max_length=200, help_text="Physics specializations")
    teaching_experience = models.PositiveIntegerField(default=0, help_text="Years of teaching experience")
    qualifications = models.TextField(blank=True)
    school_affiliation = models.CharField(max_length=200, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Teacher Profile"


class StudentProfile(models.Model):
    """Extended profile for students"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    parent_email = models.EmailField(blank=True, help_text="Parent/Guardian email for notifications")
    learning_goals = models.TextField(blank=True)
    preferred_learning_time = models.CharField(max_length=50, choices=[
        ('morning', 'Morning (6AM-12PM)'),
        ('afternoon', 'Afternoon (12PM-6PM)'),
        ('evening', 'Evening (6PM-12AM)'),
        ('flexible', 'Flexible'),
    ], default='flexible')
    physics_interest_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Student Profile"


class UserNotification(models.Model):
    """User notifications system"""
    NOTIFICATION_TYPES = [
        ('achievement', 'Achievement Unlocked'),
        ('reminder', 'Study Reminder'),
        ('quiz_due', 'Quiz Due'),
        ('new_content', 'New Content Available'),
        ('progress_milestone', 'Progress Milestone'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True, help_text="URL to navigate when notification is clicked")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class UserPreference(models.Model):
    """User preferences and settings"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    study_reminders = models.BooleanField(default=True)
    achievement_notifications = models.BooleanField(default=True)
    weekly_progress_reports = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Preferences"