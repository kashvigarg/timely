from django.db import models

class Behaviour(models.IntegerChoices):
    LAZY = 1, 'Lazy'
    MODERATELY_LAZY = 2, 'Moderately Lazy'
    MODERATELY_HARDWORKING = 3, 'Moderately Hardworking'
    HARDWORKING = 4, 'Hardworking'

class Difficulty(models.IntegerChoices):
    HARD = 1, 'Hard'
    MEDIUM = 2, 'Medium'
    EASY = 3, 'Easy'

class Priority(models.IntegerChoices):
    HIGH = 1, 'High'
    MEDIUM = 2, 'Medium'
    LOW = 3, 'Low'

class Day(models.IntegerChoices):
    MONDAY = 1, 'Monday'
    TUESDAY = 2, 'Tuesday'
    WEDNESDAY = 3, 'Wednesday'
    THURSDAY = 4, 'Thursday'
    FRIDAY = 5, 'Friday'
    SATURDAY = 6, 'Saturday'
    SUNDAY = 7, 'Sunday'