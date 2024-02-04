from enum import Enum

class Behaviour(Enum):
    LAZY = 1, 'Lazy'
    MODERATELY_LAZY = 2, 'Moderately Lazy'
    MODERATELY_HARDWORKING = 3, 'Moderately Hardworking'
    HARDWORKING = 4, 'Hardworking'

class Difficulty(Enum):
    HARD = 1, 'Hard'
    MEDIUM = 2, 'Medium'
    EASY = 3, 'Easy'

class Priority(Enum):
    HIGH = 1, 'High'
    MEDIUM = 2, 'Medium'
    LOW = 3, 'Low'

class Day(Enum):
    MONDAY = 1, 'Monday'
    TUESDAY = 2, 'Tuesday'
    WEDNESDAY = 3, 'Wednesday'
    THURSDAY = 4, 'Thursday'
    FRIDAY = 5, 'Friday'
    SATURDAY = 6, 'Saturday'
    SUNDAY = 7, 'Sunday'