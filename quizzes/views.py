from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import Quiz, Question, Answer, QuizAttempt, QuizResponse, QuizFeedback
from topics.models import PhysicsTopic
# Remove login_required decorator
# from django.contrib.auth.decorators import login_required

def quiz_list(request, topic_id=None):
    """List all quizzes, optionally filtered by topic"""
    quizzes = Quiz.objects.filter(is_active=True)
    
    if topic_id:
        quizzes = quizzes.filter(topic_id=topic_id)
        topic = get_object_or_404(PhysicsTopic, id=topic_id)
    else:
        topic = None
    
    # Get user attempts if logged in
    user_attempts = {}
    
    context = {
        'quizzes': quizzes,
        'topic': topic,
        'user_attempts': user_attempts,
    }
    return render(request, 'quizzes/quiz_list.html', context)


def quiz_detail(request, quiz_id):
    """Detailed view of a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    
    # Get user attempts if logged in
    user_attempts = []
    
    context = {
        'quiz': quiz,
        'user_attempts': user_attempts,
    }
    return render(request, 'quizzes/quiz_detail.html', context)


# Remove start_quiz view since it requires authentication
# @login_required
# def start_quiz(request, quiz_id):
#     """Start a quiz attempt"""
#     quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
#     
#     # Check if user has exceeded max attempts
#     existing_attempts = QuizAttempt.objects.filter(
#         user=request.user,
#         quiz=quiz
#     ).count()
#     
#     if existing_attempts >= quiz.max_attempts:
#         return JsonResponse({
#             'success': False,
#             'message': f'Maximum attempts ({quiz.max_attempts}) exceeded'
#         })
#     
#     # Create new attempt
#     attempt = QuizAttempt.objects.create(
#         user=request.user,
#         quiz=quiz,
#         attempt_number=existing_attempts + 1
#     )
#     
#     return JsonResponse({
#         'success': True,
#         'attempt_id': attempt.id,
#         'message': f'Started quiz: {quiz.title}'
#     })


# Remove take_quiz view since it requires authentication
# @login_required
# def take_quiz(request, attempt_id):
#     """Take a quiz attempt"""
#     attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
#     
#     if attempt.completed_at:
#         return redirect('quiz_result', attempt_id=attempt.id)
#     
#     # Get questions for the quiz
#     questions = attempt.quiz.questions.filter(is_active=True)
#     if attempt.quiz.is_randomized:
#         questions = questions.order_by('?')
#     
#     # Get existing responses
#     responses = QuizResponse.objects.filter(attempt=attempt)
#     response_dict = {r.question_id: r for r in responses}
#     
#     context = {
#         'attempt': attempt,
#         'questions': questions,
#         'responses': response_dict,
#     }
#     return render(request, 'quizzes/take_quiz.html', context)


# Remove submit_quiz_response view since it requires authentication
# @login_required
# def submit_quiz_response(request, attempt_id, question_id):
#     """Submit response for a quiz question"""
#     attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
#     question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)
#     
#     # Get or create response
#     response, created = QuizResponse.objects.get_or_create(
#         attempt=attempt,
#         question=question
#     )
#     
#     # Handle different question types
#     if question.question_type == 'multiple_choice':
#         answer_ids = request.POST.getlist('answers')
#         selected_answers = Answer.objects.filter(id__in=answer_ids)
#         response.selected_answers.set(selected_answers)
#         
#         # Check if correct
#         correct_answers = question.answers.filter(is_correct=True)
#         user_answers = set(selected_answers)
#         correct_set = set(correct_answers)
#         
#         response.is_correct = user_answers == correct_set
#         response.points_earned = question.points if response.is_correct else 0
#         
#     elif question.question_type == 'true_false':
#         answer_id = request.POST.get('answer')
#         if answer_id:
#             selected_answer = Answer.objects.get(id=answer_id)
#             response.selected_answers.set([selected_answer])
#             response.is_correct = selected_answer.is_correct
#             response.points_earned = question.points if response.is_correct else 0
#     
#     elif question.question_type in ['fill_blank', 'short_answer', 'calculation']:
#         text_response = request.POST.get('text_response', '')
#         response.text_response = text_response
#         # For now, mark as correct if text is provided (can be enhanced with AI checking)
#         response.is_correct = bool(text_response.strip())
#         response.points_earned = question.points if response.is_correct else 0
#     
#     response.save()
#     
#     return JsonResponse({
#         'success': True,
#         'is_correct': response.is_correct,
#         'points_earned': response.points_earned,
#         'explanation': question.explanation if response.is_correct else ''
#     })


# Remove complete_quiz view since it requires authentication
# @login_required
# def complete_quiz(request, attempt_id):
#     """Complete a quiz attempt"""
#     attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
#     
#     if attempt.completed_at:
#         return JsonResponse({
#             'success': False,
#             'message': 'Quiz already completed'
#         })
#     
#     # Calculate score
#     total_points = sum(q.points for q in attempt.quiz.questions.filter(is_active=True))
#     earned_points = sum(r.points_earned for r in attempt.responses.all())
#     score = (earned_points / total_points * 100) if total_points > 0 else 0
#     
#     # Complete the attempt
#     attempt.completed_at = timezone.now()
#     attempt.score = score
#     attempt.is_passed = score >= attempt.quiz.passing_score
#     attempt.save()
#     
#     return JsonResponse({
#         'success': True,
#         'score': score,
#         'is_passed': attempt.is_passed,
#         'message': f'Quiz completed with {score:.1f}% score'
#     })


# Remove quiz_result view since it requires authentication
# @login_required
# def quiz_result(request, attempt_id):
#     """View quiz results"""
#     attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
#     
#     if not attempt.completed_at:
#         return redirect('take_quiz', attempt_id=attempt.id)
#     
#     # Get responses with correct answers
#     responses = attempt.responses.all()
#     
#     context = {
#         'attempt': attempt,
#         'responses': responses,
#     }
#     return render(request, 'quizzes/quiz_result.html', context)


# Remove submit_quiz_feedback view since it requires authentication
# @login_required
# def submit_quiz_feedback(request, attempt_id):
#     """Submit feedback for a quiz"""
#     attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
#     
#     feedback, created = QuizFeedback.objects.get_or_create(attempt=attempt)
#     
#     feedback.difficulty_rating = request.POST.get('difficulty_rating')
#     feedback.helpful_rating = request.POST.get('helpful_rating')
#     feedback.concepts_understood = request.POST.get('concepts_understood', '')
#     feedback.concepts_confusing = request.POST.get('concepts_confusing', '')
#     feedback.suggestions = request.POST.get('suggestions', '')
#     feedback.save()
#     
#     return JsonResponse({
#         'success': True,
#         'message': 'Feedback submitted successfully'
#     })


def search_quizzes(request):
    """Search quizzes"""
    query = request.GET.get('q', '')
    quizzes = Quiz.objects.filter(is_active=True)
    
    if query:
        quizzes = quizzes.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(topic__title__icontains=query)
        )
    
    context = {
        'quizzes': quizzes,
        'query': query,
    }
    return render(request, 'quizzes/search_results.html', context)