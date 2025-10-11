"""
URLs para el módulo de inicio (dashboard)
"""
from django.urls import path
from . import views

app_name = 'inicio'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
]