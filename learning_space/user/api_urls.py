from django.urls import path
from . import api_views

user_urls = [
    path('api/register', api_views.register, name='register')
]
