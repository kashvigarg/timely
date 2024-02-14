from django.http import HttpResponse
from .google_palm import get_response
from django.views import View
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import json
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import utils

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Schedule, TimeTable, CustomUser
from .serializers import TaskSerializer, ScheduleSerializer, TimeTableSerializer
from rest_framework.decorators import api_view, renderer_classes

class TestHitView(APIView):
    def get(self, request, format= None):
        return Response(
            status=status.HTTP_200_OK,
            data={
                "error": False,
                "error_message": "",
                "success_message": "API test successful.",
                "data": {
                    
                }
            }
           )
    

class GetIdView(APIView):
    def get(self, request, format=None):
       email = request.data['email']
       user = CustomUser.objects.filter(email=email)
       
       if not user:
           return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                "error": True,
                "error_message": f"User with email {email} doesn't exist.",
                "success_message": "",
                "data": {
                    
                }
            }
           )
       else:
           return Response(
            status=status.HTTP_200_OK,
            data={
                "error": False,
                "error_message": "",
                "success_message": f"User with email {email} fetched successfully.",
                "data": {
                    "user_id": user.values_list('id', flat=True)[0],
                    "email" : user.values_list( 'email' , flat=True)[0],
                    "username" : user.values_list( 'username', flat=True)[0]
                }
            }
           )


class TimetableView (APIView):
    def get(self, request, schedule_id, format = None):
        
        schedule = Schedule.objects.filter(user_id = request.user.id , id = schedule_id).first()
        schedule_serializer = ScheduleSerializer(schedule)
        schedule.has_timetable = True
        schedule.save()
        schedule_duration_days = schedule_serializer.data['duration']
        starts_on = schedule_serializer.data['starts_on']
        longest_sitting_time_minutes = schedule_serializer.data['longest_sitting_time']
        user_behaviour = schedule_serializer.data['behaviour']

        all_tasks = Task.objects.filter(schedule_id=schedule_id)
        
        task_serializer = TaskSerializer(all_tasks, many=True)
        tasks = task_serializer.data

        palm_data = get_response (schedule_duration_days, starts_on,  longest_sitting_time_minutes,user_behaviour, tasks)
        # serializer = TimeTableSerializer(palm_data)

        if (palm_data!=None):
            return Response(
            status=status.HTTP_200_OK,
            data={
                "error": False,
                "error_message": "",
                "success_message": f"Timetable fetched successfully.",
                "data": {
                    "timetable" : palm_data['timetable'],
                    "timetable_color" : schedule.schedule_color
                }
            }
        )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
            "error": True,
            "error_message": "Time table couldn't be generated for given schedule id",
            "success_message": "",
            "data": {}
        }
    )
        
         

class TaskListCreateView(APIView):
    def get(self, request, schedule_id, format=None):
        tasks = Task.objects.filter(schedule_id=schedule_id)
        serializer = TaskSerializer(tasks, many=True)
        tasks_count = tasks.count()
        
        if serializer.data:
            return Response(
            status=status.HTTP_200_OK,
            data={
                "error": False,
                "error_message": "",
                "success_message": f"Tasks count for schedule {schedule_id} retrieved successfully.",
                "data": {
                    "schedule_id": schedule_id,
                    "tasks_count": tasks_count, 
                    "tasks" : serializer.data
                }
            }
        )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
            "error": True,
            "error_message": serializer.errors,
            "success_message": "",
            "data": {}
        }
    )
    
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(
            status=status.HTTP_201_CREATED,
            data={
                "error": False,
                "error_message": "",
                "success_message": "Task created successfully",
                "data": serializer.data
            }
        )

        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
            "error": True,
            "error_message": serializer.errors,
            "success_message": "",
            "data": {}
        }
    )


class ScheduleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        schedules = Schedule.objects.filter(user_id=user_id)
        serializer = ScheduleSerializer(schedules, many=True)
        if not serializer.data:
            return Response(
                status= status.HTTP_404_NOT_FOUND,
                data = {
                    "error" : True, 
                    "error_message" : "No schedules exist for user.", 
                    "success_message" : "", 
                    "data" : {}
                }
        )
        return Response(
                status= status.HTTP_200_OK,
                data = {
                    "error" : False, 
                    "error_message" : "", 
                    "success_message" : "", 
                    "data" : serializer.data
                }
        )

    def post(self, request, format=None):
        try:
            
            serializer = ScheduleSerializer(data=request.data)
            if serializer.is_valid():
                user_id = request.user.id
                
                user = get_user_model().objects.get(id=user_id)
                if not user:
                    raise PermissionDenied("User doesn't exist")

                serializer.save()

                
                return Response(
                status=status.HTTP_201_CREATED,
                data={
                "error": False,
                "error_message": "",
                "success_message": "Schedule created successfully",
                "data": serializer.data
                }
            )

        except get_user_model().DoesNotExist:
            raise PermissionDenied("User not found.")

        except PermissionDenied as e:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={
                    "error": True,
                    "error_message": str(e),
                    "success_message": "",
                    "data": {}
                }
            )
        
        
        
        return Response(
        status=status.HTTP_400_BAD_REQUEST,
        data={
            "error": True,
            "error_message": serializer.errors,
            "success_message": "",
            "data": {}
        }
    )


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            user = serializer.save()

            success_message = f"Account created for {username}"
            error_message = ""
            error = False
            data = {
                "user_id" : user.id
            }

            return Response(
                status= status.HTTP_200_OK,
                data = {
                    "error" : error, 
                    "error_message" : error_message, 
                    "success_message" : success_message, 
                    "data" : data
                }
        )
        
        error_message = serializer.errors
        error = True
        success_message = ""
        data = { }
        return Response(
            status= status.HTTP_400_BAD_REQUEST,
                data = {
                    "error" : error, 
                    "error_message" : error_message, 
                    "success_message" : success_message, 
                    "data" : data
                }
        )


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
   
            authenticate(request, username=email, password=password)
            user = get_user_model().objects.get(email=email)
            if user is not None and user.is_active:
                
                auth.login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                print(token)
                

                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "error": False,
                        "error_message": "",
                        "success_message": "Logged in successfully",
                        "data": {
                            "token": token.key
                        }
                    }
                )

            elif user is not None and not user.is_active:
                error_message = "User account is not active. Please contact support."

            else:
                error_message = "Invalid credentials."

        else:
            error_message = serializer.errors

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={
                "error": True,
                "error_message": error_message,
                "success_message": "",
                "data": {}
            }
        )
    

# timetable time alter tasks, 