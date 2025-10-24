from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import Simulation, SimulationSession, SimulationFeedback
from topics.models import PhysicsTopic
# Remove login_required decorator
# from django.contrib.auth.decorators import login_required

def simulation_list(request, topic_id=None):
    """List all simulations, optionally filtered by topic"""
    simulations = Simulation.objects.filter(is_active=True)
    
    if topic_id:
        simulations = simulations.filter(topic_id=topic_id)
        topic = get_object_or_404(PhysicsTopic, id=topic_id)
    else:
        topic = None
    
    # Get user sessions if logged in
    user_sessions = {}
    
    context = {
        'simulations': simulations,
        'topic': topic,
        'user_sessions': user_sessions,
    }
    return render(request, 'simulations/simulation_list.html', context)


def simulation_detail(request, simulation_id):
    """Detailed view of a simulation"""
    simulation = get_object_or_404(Simulation, id=simulation_id, is_active=True)
    
    # Get user session if logged in
    user_session = None
    
    context = {
        'simulation': simulation,
        'user_session': user_session,
    }
    return render(request, 'simulations/simulation_detail.html', context)


# Remove start_simulation view since it requires authentication
# @login_required
# def start_simulation(request, simulation_id):
#     """Start a simulation session"""
#     simulation = get_object_or_404(Simulation, id=simulation_id)
#     
#     session, created = SimulationSession.objects.get_or_create(
#         user=request.user,
#         simulation=simulation
#     )
#     
#     if created:
#         session.started_at = timezone.now()
#         session.save()
#     
#     return JsonResponse({
#         'success': True,
#         'session_id': session.id,
#         'message': f'Started simulation: {simulation.title}'
#     })


# Remove complete_simulation view since it requires authentication
# @login_required
# def complete_simulation(request, simulation_id):
#     """Complete a simulation session"""
#     simulation = get_object_or_404(Simulation, id=simulation_id)
#     
#     try:
#         session = SimulationSession.objects.get(
#             user=request.user,
#             simulation=simulation
#         )
#         session.is_completed = True
#         session.completed_at = timezone.now()
#         session.save()
#         
#         return JsonResponse({
#             'success': True,
#             'message': f'Completed simulation: {simulation.title}'
#         })
#     except SimulationSession.DoesNotExist:
#         return JsonResponse({
#             'success': False,
#             'message': 'Simulation session not found'
#         })


# Remove save_simulation_parameters view since it requires authentication
# @login_required
# def save_simulation_parameters(request, simulation_id):
#     """Save simulation parameters used by user"""
#     simulation = get_object_or_404(Simulation, id=simulation_id)
#     parameters = request.POST.get('parameters', {})
#     
#     try:
#         session = SimulationSession.objects.get(
#             user=request.user,
#             simulation=simulation
#         )
#         session.parameters_used = parameters
#         session.interactions_count += 1
#         session.save()
#         
#         return JsonResponse({
#             'success': True,
#             'message': 'Parameters saved'
#         })
#     except SimulationSession.DoesNotExist:
#         return JsonResponse({
#             'success': False,
#             'message': 'Simulation session not found'
#         })


# Remove submit_simulation_feedback view since it requires authentication
# @login_required
# def submit_simulation_feedback(request, simulation_id):
#     """Submit feedback for a simulation"""
#     simulation = get_object_or_404(Simulation, id=simulation_id)
#     
#     try:
#         session = SimulationSession.objects.get(
#             user=request.user,
#             simulation=simulation
#         )
#         
#         feedback, created = SimulationFeedback.objects.get_or_create(
#             session=session
#         )
#         
#         feedback.understanding_rating = request.POST.get('understanding_rating')
#         feedback.difficulty_rating = request.POST.get('difficulty_rating')
#         feedback.helpful_rating = request.POST.get('helpful_rating')
#         feedback.comments = request.POST.get('comments', '')
#         feedback.concepts_learned = request.POST.get('concepts_learned', '')
#         feedback.questions_arose = request.POST.get('questions_arose', '')
#         feedback.save()
#         
#         return JsonResponse({
#             'success': True,
#             'message': 'Feedback submitted successfully'
#         })
#     except SimulationSession.DoesNotExist:
#         return JsonResponse({
#             'success': False,
#             'message': 'Simulation session not found'
#         })


def interactive_simulation(request, simulation_id):
    """Render interactive simulation page"""
    simulation = get_object_or_404(Simulation, id=simulation_id, is_active=True)
    
    context = {
        'simulation': simulation,
    }
    return render(request, 'simulations/interactive.html', context)