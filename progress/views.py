from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Sum, Avg, Q
from .models import (
    TopicProgress, LearningPath, Achievement, UserAchievement, 
    StudySession, LearningAnalytics, UserProfile
)
from topics.models import PhysicsTopic, CBCGrade
# Remove login_required decorator
# from django.contrib.auth.decorators import login_required

# Remove dashboard view since it requires authentication
# @login_required
# def dashboard(request):
#     """User's learning dashboard"""
#     user = request.user
#     
#     # Get user progress
#     topic_progress = TopicProgress.objects.filter(user=user)
#     completed_topics = topic_progress.filter(status='completed').count()
#     in_progress_topics = topic_progress.filter(status='in_progress').count()
#     
#     # Get recent study sessions
#     recent_sessions = StudySession.objects.filter(user=user).order_by('-started_at')[:5]
#     
#     # Get achievements
#     user_achievements = UserAchievement.objects.filter(user=user).order_by('-earned_at')[:5]
#     
#     # Get learning analytics
#     analytics, created = LearningAnalytics.objects.get_or_create(user=user)
#     
#     context = {
#         'completed_topics': completed_topics,
#         'in_progress_topics': in_progress_topics,
#         'recent_sessions': recent_sessions,
#         'user_achievements': user_achievements,
#         'analytics': analytics,
#     }
#     return render(request, 'progress/dashboard.html', context)


# Remove analytics view since it requires authentication
# @login_required
# def analytics(request):
#     """Detailed learning analytics"""
#     user = request.user
#     
#     # Get analytics
#     analytics, created = LearningAnalytics.objects.get_or_create(user=user)
#     
#     # Get topic progress breakdown
#     progress_by_grade = topic_progress.values('topic__grade__name').annotate(
#         total=Count('id'),
#         completed=Count('id', filter=Q(status='completed'))
#     )
#     
#     # Get study time by session type
#     study_time_by_type = StudySession.objects.filter(user=user).values(
#         'session_type'
#     ).annotate(
#         total_time=Sum('duration')
#     )
#     
#     context = {
#         'analytics': analytics,
#         'progress_by_grade': progress_by_grade,
#         'study_time_by_type': study_time_by_type,
#     }
#     return render(request, 'progress/analytics.html', context)


# Remove achievements view since it requires authentication
# @login_required
# def achievements(request):
#     """User achievements page"""
#     user = request.user
#     
#     # Get all achievements
#     all_achievements = Achievement.objects.filter(is_active=True)
#     
#     # Get user achievements
#     user_achievements = UserAchievement.objects.filter(user=user)
#     earned_achievement_ids = user_achievements.values_list('achievement_id', flat=True)
#     
#     # Separate earned and unearned achievements
#     earned_achievements = all_achievements.filter(id__in=earned_achievement_ids)
#     unearned_achievements = all_achievements.exclude(id__in=earned_achievement_ids)
#     
#     context = {
#         'earned_achievements': earned_achievements,
#         'unearned_achievements': unearned_achievements,
#         'user_achievements': user_achievements,
#     }
#     return render(request, 'progress/achievements.html', context)


# Remove learning_path view since it requires authentication
# @login_required
# def learning_path(request):
#     """User's learning path"""
#     user = request.user
#     
#     # Get user's learning paths
#     learning_paths = LearningPath.objects.filter(user=user, is_active=True)
#     
#     # Get recommended topics based on progress
#     completed_topics = TopicProgress.objects.filter(
#         user=user, 
#         status='completed'
#     ).values_list('topic_id', flat=True)
#     
#     recommended_topics = PhysicsTopic.objects.filter(
#         is_active=True
#     ).exclude(id__in=completed_topics)[:10]
#     
#     context = {
#         'learning_paths': learning_paths,
#         'recommended_topics': recommended_topics,
#     }
#     return render(request, 'progress/learning_path.html', context)


# Remove study_sessions view since it requires authentication
# @login_required
# def study_sessions(request):
#     """User's study sessions"""
#     user = request.user
#     
#     # Get study sessions
#     sessions = StudySession.objects.filter(user=user).order_by('-started_at')
#     
#     # Get session statistics
#     total_sessions = sessions.count()
#     total_time = sessions.aggregate(Sum('duration'))['duration__sum'] or 0
#     avg_satisfaction = sessions.aggregate(Avg('satisfaction_rating'))['satisfaction_rating__avg'] or 0
#     
#     context = {
#         'sessions': sessions,
#         'total_sessions': total_sessions,
#         'total_time': total_time,
#         'avg_satisfaction': avg_satisfaction,
#     }
#     return render(request, 'progress/study_sessions.html', context)