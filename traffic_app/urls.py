from django.urls import path
from . import views

urlpatterns = [
    path('api/sensor-events/', views.sensor_event_receiver, name='sensor-events'),
    path('api/junctions/<str:junction_id>/commands/', views.manual_command, name='manual-command'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]