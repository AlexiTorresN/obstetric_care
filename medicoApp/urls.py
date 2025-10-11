"""
URLs para la gestión del catálogo de patologías
"""
from django.urls import path
from . import views

app_name = 'medico'

urlpatterns = [
    # ============================================
    # RUTAS DE PATOLOGÍAS
    # ============================================
    path('patologias/', views.PatologiaListView.as_view(), name='lista_patologias'),
    path('patologia/<int:pk>/', views.PatologiaDetailView.as_view(), name='detalle_patologia'),
    path('patologia/registrar/', views.registrar_patologia, name='registrar_patologia'),
    path('patologia/<int:pk>/editar/', views.editar_patologia, name='editar_patologia'),
    
    # ============================================
    # API REST (AJAX)
    # ============================================
    path('api/patologia/<int:pk>/cambiar-estado/', 
        views.cambiar_estado_patologia, 
        name='api_cambiar_estado_patologia'),
]