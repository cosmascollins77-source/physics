from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import PhysicsTopic, TopicContent, TopicMedia, TopicFormula, TopicExperiment, CBCGrade
# Remove UserProfile import since it requires authentication
# from progress.models import TopicProgress, UserProfile

# Remove login_required decorator
# from django.contrib.auth.decorators import login_required

def home(request):
    """Home page with overview of physics topics"""
    grades = CBCGrade.objects.all().order_by('order')
    featured_topics = PhysicsTopic.objects.filter(is_active=True)[:6]
    
    context = {
        'grades': grades,
        'featured_topics': featured_topics,
    }
    return render(request, 'topics/home.html', context)


def topic_list(request, grade_id=None):
    """List all physics topics, optionally filtered by grade"""
    topics = PhysicsTopic.objects.filter(is_active=True)
    
    if grade_id:
        topics = topics.filter(grade_id=grade_id)
        grade = get_object_or_404(CBCGrade, id=grade_id)
    else:
        grade = None
    
    context = {
        'topics': topics,
        'grade': grade,
    }
    return render(request, 'topics/topic_list.html', context)


def topic_detail(request, topic_slug):
    """Detailed view of a physics topic"""
    topic = get_object_or_404(PhysicsTopic, slug=topic_slug, is_active=True)
    
    # Get topic content
    contents = topic.contents.all().order_by('order')
    media = topic.media.all().order_by('order')
    formulas = topic.formulas.all().order_by('order')
    experiments = topic.experiments.all().order_by('order')
    
    context = {
        'topic': topic,
        'contents': contents,
        'media': media,
        'formulas': formulas,
        'experiments': experiments,
    }
    return render(request, 'topics/topic_detail.html', context)


# Remove start_topic view since it requires authentication
# @login_required
# def start_topic(request, topic_id):
#     """Start studying a topic"""
#     topic = get_object_or_404(PhysicsTopic, id=topic_id)
#     
#     progress, created = TopicProgress.objects.get_or_create(
#         user=request.user,
#         topic=topic
#     )
#     
#     if progress.status == 'not_started':
#         progress.status = 'in_progress'
#         progress.started_at = timezone.now()
#         progress.save()
#     
#     return JsonResponse({
#         'success': True,
#         'status': progress.status,
#         'message': f'Started studying {topic.title}'
#     })


# Remove complete_topic view since it requires authentication
# @login_required
# def complete_topic(request, topic_id):
#     """Mark a topic as completed"""
#     topic = get_object_or_404(PhysicsTopic, id=topic_id)
#     
#     try:
#         progress = TopicProgress.objects.get(user=request.user, topic=topic)
#         progress.status = 'completed'
#         progress.completed_at = timezone.now()
#         progress.save()
#         
#         return JsonResponse({
#             'success': True,
#             'message': f'Completed {topic.title}'
#         })
#     except TopicProgress.DoesNotExist:
#         return JsonResponse({
#             'success': False,
#             'message': 'Topic progress not found'
#         })


def search_topics(request):
    """Search physics topics"""
    query = request.GET.get('q', '')
    topics = PhysicsTopic.objects.filter(is_active=True)
    
    if query:
        topics = topics.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(learning_outcomes__icontains=query)
        )
    
    context = {
        'topics': topics,
        'query': query,
    }
    return render(request, 'topics/search_results.html', context)