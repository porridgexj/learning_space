from django.urls import path
from . import api_views

urlpatterns = [
    path('api/register', api_views.register, name='register')
]
