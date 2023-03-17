from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health, name='health'),    
    path('accounts/', include('allauth.urls')),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback')
]