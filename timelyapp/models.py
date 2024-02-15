from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .enums import *
from .model_managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    

class Schedule(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, default="", unique=True)
    duration = models.IntegerField(default=0)
    starts_on = models.DateTimeField(default=timezone.now)
    no_of_tasks = models.IntegerField(default=0)
    longest_sitting_time = models.DurationField(default=timezone.timedelta(hours=2))
    behaviour = models.IntegerField(choices=[(choice.value, choice.name) for choice in Behaviour], default=Behaviour.MODERATELY_HARDWORKING.value)
    has_timetable = models.BooleanField(default=False)
    schedule_color = models.CharField(max_length=255, default="#9292F0")

    def __str__(self):
        return f"{self.name} , has_timetable = {self.has_timetable}"
    
class Task(models.Model):
    schedule_id = models.ForeignKey(Schedule, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, default = "")
    difficulty = models.IntegerField(choices=[(choice.value, choice.name) for choice in Difficulty], default=Difficulty.EASY.value)
    priority = models.IntegerField(choices=[(choice.value, choice.name) for choice in Priority], default=Priority.MEDIUM.value)
    no_of_revisions = models.IntegerField(default=0)
    estimated_length = models.DurationField(default=timezone.timedelta)

    def __str__(self):
        return self.name
    
class TimeSlab(models.Model):
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    tasks = models.ManyToManyField(Task)

class Day(models.Model):
    date = models.DateField(default=timezone.now)
    time_slabs = models.ManyToManyField(TimeSlab)

class TimeTable(models.Model):
    schedule_id = models.ForeignKey(Schedule, on_delete = models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    days = models.ManyToManyField(Day)

# class TimeTable(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE, default = "", null=True)
#     day = models.IntegerField(choices=[(choice.value, choice.name) for choice in Day], default=Day.MONDAY.value)
#     start_time = models.TimeField(default = timezone.now)
#     end_time = models.TimeField(default = timezone.now)
#     timetable_color = models.CharField(max_length=255, default="")
    
#     def __str__(self):
#         return f"{self.task.name} - {self.get_day_display()} - {self.start_time} to {self.end_time}"
    

# {
#     "error": false,
#     "error_message": "",
#     "success_message": "Timetable fetched successfully.",
#     "data": {
#         "timetable": {
#             "days": {
#                 "day_1": {
#                     "date": "10/02/2024",
#                     "time_slabs": [
#                         {
#                             "start_time": "08:00 AM",
#                             "end_time": "10:00 AM",
#                             "tasks": [
#                                 {
#                                     "id": 1,
#                                     "name": "Task1",
#                                     "difficulty": 2,
#                                     "priority": 1,
#                                     "no_of_revisions": 2,
#                                     "schedule_id": 1,
#                                     "task_id": 1
#                                 }
#                             ]
#                         },
#                         {
#                             "start_time": "10:30 AM",
#                             "end_time": "12:30 PM",
#                             "tasks": [
#                                 {
#                                     "id": 2,
#                                     "name": "Task2",
#                                     "difficulty": 2,
#                                     "priority": 1,
#                                     "no_of_revisions": 2,
#                                     "schedule_id": 1,
#                                     "task_id": 2
#                                 }
#                             ]
#                         },
#                         {
#                             "start_time": "01:30 PM",
#                             "end_time": "03:30 PM",
#                             "tasks": [
#                                 {
#                                     "id": 3,
#                                     "name": "Task3",
#                                     "difficulty": 1,
#                                     "priority": 2,
#                                     "no_of_revisions": 1,
#                                     "schedule_id": 1,
#                                     "task_id": 3
#                                 }
#                             ]
#                         },
#                         {
#                             "start_time": "04:00 PM",
#                             "end_time": "06:00 PM",
#                             "tasks": [
#                                 {
#                                     "id": 4,
#                                     "name": "Task4",
#                                     "difficulty": 1,
#                                     "priority": 2,
#                                     "no_of_revisions": 1,
#                                     "schedule_id": 1,
#                                     "task_id": 4
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             }
#         },
#         "timetable_color": "#9292F0"
#     }
# }