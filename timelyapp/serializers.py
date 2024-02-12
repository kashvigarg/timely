from rest_framework import serializers

from .models import Schedule, Task, TimeTable, CustomUser

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['task_id'] = instance.id
        
        return representation

class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['user_id', 'name' ,'duration','starts_on', 'longest_sitting_time', 'behaviour', 'schedule_color']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user_id', None)
        representation['schedule_id'] = instance.id
        representation['has_timetable'] = instance.has_timetable
        
        return representation


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

    