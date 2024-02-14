from django.urls import path
from .views import (
    TaskListCreateView, 
    # TaskDetailView,
    GetIdView,
    RegisterView, LoginView,
    ScheduleListCreateView, 
    TimetableView,
    # ScheduleDetailView,
    # TimeTableListCreateView, TimeTableDetailView
)
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("get_res", views.palm_response, name="palm_response"), 
    
    # Task URLs
    path('tasks', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:schedule_id>', TaskListCreateView.as_view(), name='task-get'),

    # auth 
    path('register', RegisterView.as_view(), name = 'register'),
    path('login', LoginView.as_view(), name = 'login'),
    path('getidbyusername', GetIdView.as_view(), name='id-by-username'),
    
    # # Schedule URLs
    path('schedules', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:user_id>', ScheduleListCreateView.as_view(), name='schedule-detail'),

    # # TimeTable URLs
    # path('timetables/<int:schedule_id>', TimetableView.as_view(), name='timetable-list-create'),
    # path('timetables/<int:pk>/', TimeTableDetailView.as_view(), name='timetable-detail'),

]