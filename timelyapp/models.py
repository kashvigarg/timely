from django.db import models
from django.utils import timezone
# from django_mysql.models import ListCharField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.is_staff = False 
        user.is_active = True
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    
class Task(models.Model):
    difficulty_choices = (
        (1, "Hard"),
        (2, "Medium"), 
        (3, "Easy"), 
    )
    priority_choices = (
        (1, "High"), 
        (2, "Medium"),
        (3, "Low"),
    )

    name = models.CharField(max_length=255, default = "")
    difficulty = models.IntegerField(choices=difficulty_choices, default = 3)
    priority = models.IntegerField(choices=priority_choices, default = 3)
    no_of_revisions = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    

class Schedule(models.Model):
    class Behaviour(models.IntegerChoices):
        LAZY = 1, 'Lazy'
        MODERATELY_LAZY = 2, 'Moderately Lazy'
        MODERATELY_HARDWORKING = 3, 'Moderately Hardworking'
        HARDWORKING = 4, 'Hardworking'
    # curr = get_user_model().objects.first()
    user_id = models.ForeignKey(CustomUser, on_delete = models.CASCADE, default=0)
    name = models.CharField(max_length=255, default="", unique=True)
    duration = models.IntegerField(default=0)
    starts_on = models.DateTimeField(default=timezone.now)
    no_of_tasks = models.IntegerField(default=0)
    longest_sitting_time = models.DurationField(default=timezone.timedelta(hours=2))
    behaviour = models.IntegerField(choices=Behaviour.choices, default=Behaviour.MODERATELY_HARDWORKING)
    tasks = models.ManyToManyField(Task, blank=True, null=True)

    def __str__(self):
        return self.name
    

class TimeTable(models.Model):
    day_choices = (
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    )

    task = models.ForeignKey(Task, on_delete=models.CASCADE, default = "", null=True)
    day = models.IntegerField(choices=day_choices, default = 1)
    start_time = models.TimeField(default = timezone.now)
    end_time = models.TimeField(default = timezone.now)

    def __str__(self):
        return f"{self.task.name} - {self.get_day_display()} - {self.start_time} to {self.end_time}"
    



    # Schedule (POST)
# - name of sched
# - duration (in days) 
# - starts on (date, day)
# - no of tasks 
# - longest sitting time 
# - behaviour  {lazy, moderately lazy, moderately hardworking, hardworking} 
# - tasks []

# Schedule ID -> No of tasks (GET)

# Task (POST)
# - name of subject 
# - priority (high, medium, low)
# - difficulty (high, medium, low)
# - no of revisions 

# Timetable (GET) <- Schedule ID
# - date, day - time - task

# {
#     days 
#     [
#         [
#             2-4 : Kaam, 
#             4-5 : Kaam2
#         ]
#     ]
# }

# users 
# user id 
    # auth

    # POST (user data)


# id/schedule
    # schedule id

# schedule id -> tasks add
    # tasks -> len


    # POST(user data) 
    # POST(userid/schedule) 
    # POST(userid/scheduleid/task) 
    # GET(userid/scheduleid/len of tasks)
    # GET(userid/scheduleid/tasks)
    # GET(userid/scheduleid/getTimetable)
