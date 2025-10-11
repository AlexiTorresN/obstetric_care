from django.shortcuts import render
from django.utils import timezone
from gestionApp.models import Tens, Persona
from matronaApp.models import Paciente, IngresoPaciente


def index(request):
    """Vista principal del módulo TENS"""
    return render(request, 'tens/index.html', {
        'titulo': 'Módulo TENS',
        'fecha_actual': timezone.now()
    })


def dashboard_tens(request):
    """Dashboard con estadísticas para TENS"""
    
    context = {
        'fecha_actual': timezone.now(),
        'total_tens': Tens.objects.filter(Activo=True).count(),
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_ingresos': IngresoPaciente.objects.count(),
        'ingresos_recientes': IngresoPaciente.objects.select_related('paciente').order_by('-fecha_ingreso')[:10],
    }
    
    return render(request, 'tens/dashboard.html', context)