"""
URLs para la gestión de pacientes e ingresos hospitalarios
"""
from django.urls import path
from . import views

app_name = 'matrona'

urlpatterns = [
    # ============================================
    # RUTAS DE PACIENTE
    # ============================================
    path('pacientes/', views.PacienteListView.as_view(), name='lista_pacientes'),
    path('paciente/<int:pk>/', views.PacienteDetailView.as_view(), name='detalle_paciente'),
    path('paciente/registrar/', views.registrar_paciente, name='registrar_paciente'),
    path('paciente/buscar/', views.buscar_paciente, name='buscar_paciente'),
    
    # ============================================
    # RUTAS DE INGRESO
    # ============================================
    path('ingreso/registrar/', views.registrar_ingreso, name='registrar_ingreso'),
    path('ingreso/<int:pk>/', views.IngresoDetailView.as_view(), name='detalle_ingreso'),
    
    # ============================================
    # RUTAS DE PATOLOGÍAS DEL PACIENTE
    # ============================================
    path('paciente/<int:paciente_pk>/patologia/asignar/', 
        views.asignar_patologia, 
        name='asignar_patologia'),
    path('paciente/<int:paciente_pk>/patologia/<int:patologia_pk>/eliminar/', 
        views.eliminar_patologia, 
        name='eliminar_patologia'),
    
    # ============================================
    # API REST (AJAX)
    # ============================================
    path('api/paciente/buscar/', views.buscar_paciente_api, name='api_buscar_paciente'),
    path('api/persona/buscar/', views.buscar_persona_api, name='api_buscar_persona'),

]