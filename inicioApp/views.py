"""
Vistas para el dashboard principal
"""
from django.shortcuts import render
from django.utils import timezone
from gestionApp.models import Persona, Medico, Matrona, Tens
from matronaApp.models import Paciente, IngresoPaciente
from medicoApp.models import Patologias


def dashboard(request):
    """Vista principal del dashboard"""
    
    # Obtener estadísticas
    context = {
        'fecha_actual': timezone.now(),
        
        # Estadísticas generales
        'total_personas': Persona.objects.count(),
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_ingresos': IngresoPaciente.objects.count(),
        'total_patologias': Patologias.objects.filter(estado='Activo').count(),
        
        # Personal del hospital
        'total_medicos': Medico.objects.filter(activo=True).count(),
        'total_matronas': Matrona.objects.filter(activo=True).count(),
        'total_tens': Tens.objects.filter(activo=True).count(),
        'total_personal': (
            Medico.objects.filter(activo=True).count() +
            Matrona.objects.filter(activo=True).count() +
            Tens.objects.filter(activo=True).count()
        ),
        
        # Estadísticas de patologías
        'patologias_alto_riesgo': Patologias.objects.filter(
            estado='Activo',
            nivel_de_riesgo__contains='Alto'
        ).count(),
        'patologias_bajo_riesgo': Patologias.objects.filter(
            estado='Activo',
            nivel_de_riesgo__contains='Bajo'
        ).count(),
        
        # Actividades recientes (opcional - por implementar)
        'actividades_recientes': [],
    }
    
    return render(request, 'Obtetric_care.html', context)