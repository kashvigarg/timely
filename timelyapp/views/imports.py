from django.http import HttpResponse
from ..google_palm import get_response
from django.views import View
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import json
from datetime import datetime
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from ..serializers import RegisterSerializer, LoginSerializer, EmailSerializer, TimeSlabSerializer, TimeTableSerializer
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .. import utils

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Task, Schedule, TimeTable, CustomUser, TimeSlab, Day
from ..serializers import TaskSerializer, ScheduleSerializer, TimeTableSerializer
from rest_framework.decorators import api_view, renderer_classes