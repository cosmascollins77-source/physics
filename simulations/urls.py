from django.urls import path
from . import views

app_name = 'simulations'

urlpatterns = [
    path('', views.simulation_list, name='simulation_list'),
    path('topic/<int:topic_id>/', views.simulation_list, name='simulation_list_by_topic'),
    path('simulation/<int:simulation_id>/', views.simulation_detail, name='simulation_detail'),
    # Remove authenticated views
    # path('simulation/<int:simulation_id>/start/', views.start_simulation, name='start_simulation'),
    # path('simulation/<int:simulation_id>/complete/', views.complete_simulation, name='complete_simulation'),
    # path('simulation/<int:simulation_id>/save-parameters/', views.save_simulation_parameters, name='save_simulation_parameters'),
    # path('simulation/<int:simulation_id>/feedback/', views.submit_simulation_feedback, name='submit_simulation_feedback'),
    path('interactive/<int:simulation_id>/', views.interactive_simulation, name='interactive_simulation'),
]