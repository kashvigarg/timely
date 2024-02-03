from django.http import HttpResponse
from .google_palm import get_response
from django.views import View
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import json
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import utils

def index(request):
    return HttpResponse("Hello, world. You're at app index.")

def palm_response(request):
    response = get_response(prompt='Hello, who are you?')
    return HttpResponse(json.dumps(response), content_type = 'application/json')

# views.py
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Schedule, TimeTable
from .serializers import TaskSerializer, ScheduleSerializer, TimeTableSerializer
from rest_framework.decorators import api_view, renderer_classes

# class TaskListCreateView(APIView):
#     def get(self, request, format=None):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleListCreateView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        schedules = Schedule.objects.filter(user=request.user)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        mutable_data = request.data.copy()
        mutable_data['user'] = request.user.id
        print(mutable_data)
        serializer = ScheduleSerializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ScheduleDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Schedule.objects.get(pk=pk)
#         except Schedule.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         schedule = self.get_object(pk)
#         serializer = ScheduleSerializer(schedule)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         schedule = self.get_object(pk)
#         serializer = ScheduleSerializer(schedule, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         schedule = self.get_object(pk)
#         schedule.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class TimeTableListCreateView(APIView):
#     def get(self, request, format=None):
#         timetables = TimeTable.objects.all()
#         serializer = TimeTableSerializer(timetables, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = TimeTableSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TimeTableDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return TimeTable.objects.get(pk=pk)
#         except TimeTable.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         timetable = self.get_object(pk)
#         serializer = TimeTableSerializer(timetable)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         timetable = self.get_object(pk)
#         serializer = TimeTableSerializer(timetable, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         timetable = self.get_object(pk)
#         timetable.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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