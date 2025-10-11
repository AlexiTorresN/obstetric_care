from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('personas/', views.PersonaListView.as_view(), name='lista_personas'),
    path('persona/<int:pk>/', views.PersonaDetailView.as_view(), name='detalle_persona'),
    path('persona/registrar/', views.agregar_persona, name='registrar_persona'),
    path('paciente/registrar/', views.agregar_paciente, name='registrar_paciente'),
    path('medico/registrar/', views.agregar_medico, name='registrar_medico'),
    path('matrona/registrar/', views.agregar_matrona, name='registrar_matrona'),
    path('tens/registrar/', views.agregar_tens, name='registrar_tens'),
    
    # ============================================
    # API REST (AJAX) - Sin namespace para acceso directo
    # ============================================
    path('', views.buscar_persona_api, name='buscar_persona_api'),  # Para /api/persona/buscar/
]