from django.contrib import admin

# Register your models here.
from .models import TimeTable, Task, Schedule, CustomUser

# admin.site.register(Subject)
admin.site.register(TimeTable)
admin.site.register(Task)
admin.site.register(Schedule)
admin.site.register(CustomUser)
