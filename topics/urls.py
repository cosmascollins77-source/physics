from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.home, name='home'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/grade/<int:grade_id>/', views.topic_list, name='topic_list_by_grade'),
    path('topic/<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
    # Remove authenticated views
    # path('topic/<int:topic_id>/start/', views.start_topic, name='start_topic'),
    # path('topic/<int:topic_id>/complete/', views.complete_topic, name='complete_topic'),
    path('search/', views.search_topics, name='search_topics'),
]