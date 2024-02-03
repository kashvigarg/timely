from rest_framework import serializers
from django.contrib.auth import authenticate, login
from .models import Schedule, Task, TimeTable, CustomUser
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    # tasks = TaskSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ['name' ,'duration','starts_on','no_of_tasks', 'longest_sitting_time', 'behaviour']
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']  
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        
        fields = ['email','password']

    