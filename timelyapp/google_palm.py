import google.generativeai as palm
from django.conf import settings
import os

palm.configure(api_key=settings.PALM_API_KEY)

def get_response(prompt):
    
    response = palm.chat(messages='Generate a time table for studying maths for 2 hours')
    print(response)
    return response.last