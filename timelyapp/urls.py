from django.urls import path

from .views import exports as ex
from . import views

urlpatterns = [
    # Hit Test URLS 
    path('testhit', ex.test_hit_view.TestHitView.as_view(), name='test-hit'),

    # Task URLs
    path('tasks', ex.task_view.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:schedule_id>', ex.task_view.TaskListCreateView.as_view(), name='task-get'),
    path('tasks/delete/<int:task_id>', ex.task_view.TaskListCreateView.as_view(), name='task-delete'),

    # auth 
    path('register', ex.auth_view.RegisterView.as_view(), name = 'register'),
    path('login', ex.auth_view.LoginView.as_view(), name = 'login'),
    path('getuserbyemail', ex.auth_view.GetIdView.as_view(), name='id-by-username'),
    
    # # Schedule URLs
    path('schedules', ex.schedule_view.ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('schedules/<int:user_id>', ex.schedule_view.ScheduleListCreateView.as_view(), name='schedule-detail'),

    # # TimeTable URLs
    path('timetables/', ex.timetable_view.TimetableView.as_view(), name='timetable-list-create'),
    # path('timetables/<int:pk>/', TimeTableDetailView.as_view(), name='timetable-detail'),

]