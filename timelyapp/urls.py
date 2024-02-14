from django.urls import path
from .views import (
    TaskListCreateView, 
    # TaskDetailView,
    GetIdView,
    RegisterView, LoginView,
    ScheduleListCreateView, 
    TimetableView,
    TestHitView,
    # ScheduleDetailView,
    # TimeTableListCreateView, TimeTableDetailView
)
from . import views

urlpatterns = [
    # Hit Test URLS 
    path('testhit', TestHitView.as_view(), name='test-hit'),
    
    # Task URLs
    path('tasks', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:schedule_id>', TaskListCreateView.as_view(), name='task-get'),

    # auth 
    path('register', RegisterView.as_view(), name = 'register'),
    path('login', LoginView.as_view(), name = 'login'),
    path('getuserbyemail', GetIdView.as_view(), name='id-by-username'),
    
    # # Schedule URLs
    path('schedules', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:user_id>', ScheduleListCreateView.as_view(), name='schedule-detail'),

    # # TimeTable URLs
    # path('timetables/<int:schedule_id>', TimetableView.as_view(), name='timetable-list-create'),
    # path('timetables/<int:pk>/', TimeTableDetailView.as_view(), name='timetable-detail'),

]