"""
URLs para la gestión del catálogo de patologías
"""
from django.urls import path
from . import views

app_name = 'medico'  # ✅ ESTO ES CRÍTICO

urlpatterns = [
    # ============================================
    # MENÚ PRINCIPAL
    # ============================================
    path('', views.menu_medico, name='menu_medico'),  # ✅ ESTA ES LA RUTA PRINCIPAL
    
    # ============================================
    # RUTAS DE PATOLOGÍAS
    # ============================================
    path('patologias/', views.listar_patologias, name='listar_patologias'),
    path('patologia/registrar/', views.registrar_patologia, name='registrar_patologia'),
    path('patologia/editar/<int:pk>/', views.editar_patologia, name='editar_patologia'),
    path('patologia/toggle/<int:pk>/', views.toggle_patologia, name='toggle_patologia'),
    path('patologias/<int:pk>/', views.detalle_patologia, name='detalle_patologia')
]