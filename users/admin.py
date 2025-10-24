from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TeacherProfile, StudentProfile, UserNotification, UserPreference


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_verified', 'date_joined']
    list_filter = ['user_type', 'is_verified', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Physics Learning Profile', {
            'fields': ('user_type', 'phone_number', 'date_of_birth', 'school', 
                      'grade_level', 'profile_picture', 'bio', 'is_verified')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Physics Learning Profile', {
            'fields': ('user_type', 'phone_number', 'date_of_birth', 'school', 
                      'grade_level', 'profile_picture', 'bio', 'is_verified')
        }),
    )


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject_specialization', 'teaching_experience', 'is_approved']
    list_filter = ['is_approved', 'teaching_experience']
    search_fields = ['user__username', 'subject_specialization', 'school_affiliation']
    list_editable = ['is_approved']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent_email', 'learning_goals', 'physics_interest_level']
    list_filter = ['physics_interest_level', 'preferred_learning_time']
    search_fields = ['user__username', 'parent_email', 'learning_goals']


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications', 'dark_mode', 'language']
    list_filter = ['email_notifications', 'push_notifications', 'dark_mode', 'language']
    search_fields = ['user__username']