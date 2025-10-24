from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('topic/<int:topic_id>/', views.quiz_list, name='quiz_list_by_topic'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    # Remove authenticated views
    # path('quiz/<int:quiz_id>/start/', views.start_quiz, name='start_quiz'),
    # path('attempt/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
    # path('attempt/<int:attempt_id>/question/<int:question_id>/submit/', views.submit_quiz_response, name='submit_quiz_response'),
    # path('attempt/<int:attempt_id>/complete/', views.complete_quiz, name='complete_quiz'),
    # path('attempt/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
    # path('attempt/<int:attempt_id>/feedback/', views.submit_quiz_feedback, name='submit_quiz_feedback'),
    path('search/', views.search_quizzes, name='search_quizzes'),
]