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
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, default="")
    duration = models.IntegerField(default=0)
    starts_on = models.DateTimeField(default=timezone.now)
    no_of_tasks = models.IntegerField(default=0)
    longest_sitting_time = models.DurationField(default=timezone.timedelta(hours=2))
    behaviour = models.IntegerField(choices=[(choice.value, choice.name) for choice in Behaviour], default=Behaviour.MODERATELY_HARDWORKING.value)
    has_timetable = models.BooleanField(default=False)
    schedule_color = models.CharField(max_length=255, default="#9292F0")

    def __str__(self):
        return f"{self.name} , has_timetable = {self.has_timetable}"
    
    class Meta:
        unique_together = ('user', 'name')
    
class Task(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete = models.CASCADE)
    name = models.CharField(max_length=255, default = "")
    difficulty = models.IntegerField(choices=[(choice.value, choice.name) for choice in Difficulty], default=Difficulty.EASY.value)
    priority = models.IntegerField(choices=[(choice.value, choice.name) for choice in Priority], default=Priority.MEDIUM.value)
    no_of_revisions = models.IntegerField(default=0)
    estimated_length = models.DurationField(default=timezone.timedelta)

    def __str__(self):
        return self.name
    
class TimeTable(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete = models.CASCADE)
    timetable_color = models.CharField(max_length=255, default="#9292F0")

class TimeSlab(models.Model):
    timetable = models.ForeignKey(TimeTable, on_delete = models.CASCADE)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    timeslab_color = models.CharField(max_length = 255, default= "#9292F0")
    task = models.ForeignKey(Task, on_delete = models.CASCADE) 
    date = models.DateTimeField(default=timezone.now)
    day = models.CharField(max_length=255, default = "") 



