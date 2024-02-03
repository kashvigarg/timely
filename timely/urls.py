
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('api_schema', get_schema_view(title= 'API Schema', description = 'Guide for the REST API'), name='v6apispec'),
    path('docs/', TemplateView.as_view(
        template_name='docs.html',
        extra_context={'schema_url':'v6apispec'}
        ), name='swagger-ui'),
    path("admin/", admin.site.urls),
    path("api/", include("timelyapp.urls")),
]

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

