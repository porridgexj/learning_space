"""
URL configuration for learning_space project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from learning_space.user import api_views
from learning_space.user.api_urls import urlpatterns as user_urls  
from learning_space.space.api_urls import urlpatterns as space_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    # path('api/user', include('learning_space.user.api_urls')),
    # path('api/space', include('learning_space.space.api_urls')),
    path('api/', include(user_urls)),
    path('api/', include(space_urls)),
    # path('api/register/', api_views.register, name='register'),
    # path('api/login/', api_views.login, name='login'),
    # path('api/', include('learning_space.user.api_urls')),
    path('login', views.login),
    path('reserve/<int:id>/', views.reserve),
    path('comments/<int:id>/', views.comments),
    path('favours', views.favours),
]

# urlpatterns.extend(user_urls)
# urlpatterns.extend(space_urls)
