from django.urls import path
from .views import (
    # TaskListCreateView, 
    # TaskDetailView,
    RegisterView, LoginView,
    ScheduleListCreateView, 
    # ScheduleDetailView,
    # TimeTableListCreateView, TimeTableDetailView
)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_res", views.palm_response, name="palm_response"), 
     # Task URLs
    # path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    # path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # auth 
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
    
    # # Schedule URLs
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    # path('schedules/<int:pk>/', ScheduleDetailView.as_view(), name='schedule-detail'),

    # # TimeTable URLs
    # path('timetables/', TimeTableListCreateView.as_view(), name='timetable-list-create'),
    # path('timetables/<int:pk>/', TimeTableDetailView.as_view(), name='timetable-detail'),

]