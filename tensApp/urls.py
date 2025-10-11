"""
URLs para el módulo TENS
"""
from django.urls import path
from . import views

app_name = 'tens'

urlpatterns = [
    # Dashboard TENS
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_tens, name='dashboard'),
]