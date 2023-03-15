"""dms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from rest_framework.authtoken import views
from django.conf.urls.static import static

from api.views import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('login.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('permissions/', include('userpermissions.urls')),
    path('masters/', include('masters.urls')),
    path('users/', include('users.urls')),
    path('api/token-auth/', auth.obtain_auth_token),
    path('api/', include('api.urls')),
    path('drone/', include('drone_management.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
