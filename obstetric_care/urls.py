"""
URLs principales del proyecto
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # Página principal (Dashboard)
    path('', TemplateView.as_view(template_name='Obtetric_care.html'), name='home'),
    
    # Apps del sistema
    path('gestion/', include('gestionApp.urls', namespace='gestion')),
    path('matrona/', include('matronaApp.urls', namespace='matrona')),
    path('medico/', include('medicoApp.urls', namespace='medico')),
    path('inicio/', include('inicioApp.urls', namespace='inicio')),
    path('tens/', include('tensApp.urls', namespace='tens')),
    
    # API Global (para búsquedas AJAX)
    path('api/persona/buscar/', include('gestionApp.urls')),  # ← AGREGAR ESTA LÍNEA
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)