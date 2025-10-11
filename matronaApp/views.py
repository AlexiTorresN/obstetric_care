from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from matronaApp.models import Paciente, IngresoPaciente
from gestionApp.models import Persona
from gestionApp.forms.Gestion_form import PacienteForm


# ============================================
# VISTAS DE PACIENTE
# ============================================

class PacienteListView(ListView):
    """Listado de todos los pacientes"""
    model = Paciente
    template_name = 'Matrona/Data/paciente_list.html'
    context_object_name = 'pacientes'


class PacienteDetailView(DetailView):
    """Detalle de un paciente específico"""
    model = Paciente
    template_name = 'Matrona/Data/paciente_detail.html'
    context_object_name = 'paciente'


def registrar_paciente(request):
    """Registrar un nuevo paciente"""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente registrado correctamente.")
            return redirect('matrona:lista_pacientes')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PacienteForm()
    
    return render(request, 'Matrona/Formularios/registrar_paciente.html', {'form': form})


def buscar_paciente(request):
    """Buscar paciente por RUT o nombre"""
    query = request.GET.get('q', '').strip()
    
    if query:
        pacientes = Paciente.objects.filter(
            activo=True,
            persona__Rut__icontains=query
        ) | Paciente.objects.filter(
            activo=True,
            persona__Nombre__icontains=query
        )
    else:
        pacientes = Paciente.objects.filter(activo=True)[:10]
    
    return render(request, 'Matrona/Data/buscar_paciente.html', {
        'pacientes': pacientes,
        'query': query
    })


# ============================================
# VISTAS DE INGRESO (Placeholder)
# ============================================

def registrar_ingreso(request):
    """Registrar ingreso de un paciente"""
    return render(request, 'Matrona/Formularios/registrar_ingreso.html')


class IngresoDetailView(DetailView):
    """Vista de detalle de un ingreso"""
    model = IngresoPaciente
    template_name = 'Matrona/Data/ingreso_detail.html'
    context_object_name = 'ingreso'


# ============================================
# GESTIÓN DE PATOLOGÍAS (Placeholder)
# ============================================

def asignar_patologia(request, paciente_pk):
    """Asignar una patología a un paciente"""
    paciente = get_object_or_404(Paciente, pk=paciente_pk)
    messages.info(request, "Función en desarrollo")
    return redirect('matrona:detalle_paciente', pk=paciente_pk)


def eliminar_patologia(request, paciente_pk, patologia_pk):
    """Eliminar una patología de un paciente"""
    messages.info(request, "Función en desarrollo")
    return redirect('matrona:detalle_paciente', pk=paciente_pk)


# ============================================
# API REST (AJAX)
# ============================================

def buscar_paciente_api(request):
    """Buscar paciente vía AJAX (retorna JSON)"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'pacientes': []})
    
    pacientes = Paciente.objects.filter(
        activo=True,
        persona__Rut__icontains=query
    ) | Paciente.objects.filter(
        activo=True,
        persona__Nombre__icontains=query
    )
    
    data = {
        'pacientes': [
            {
                'id': p.id,
                'nombre': f"{p.persona.Nombre} {p.persona.Apellido}",
                'rut': p.persona.Rut,
            }
            for p in pacientes[:10]
        ]
    }
    
    return JsonResponse(data)


def buscar_persona_api(request):
    """Buscar persona por RUT vía AJAX (retorna JSON)"""
    rut = request.GET.get('rut', '').strip()
    
    if not rut:
        return JsonResponse({'encontrado': False, 'mensaje': 'RUT no proporcionado'})
    
    try:
        from utilidad.rut_validator import normalizar_rut
        rut_normalizado = normalizar_rut(rut)
        
        persona = Persona.objects.filter(Rut=rut_normalizado, Activo=True).first()
        
        if persona:
            return JsonResponse({
                'encontrado': True,
                'persona': {
                    'id': persona.id,
                    'rut': persona.Rut,
                    'nombre': persona.Nombre,
                    'apellido': persona.Apellido,
                    'nombre_completo': f"{persona.Nombre} {persona.Apellido}",
                    'sexo': persona.Sexo,
                    'fecha_nacimiento': persona.Fecha_nacimiento.strftime('%Y-%m-%d'),
                    'telefono': persona.Telefono or '',
                    'email': persona.Email or '',
                    'direccion': persona.Direccion or '',
                }
            })
        else:
            return JsonResponse({
                'encontrado': False,
                'mensaje': 'No se encontró una persona con ese RUT'
            })
    
    except Exception as e:
        return JsonResponse({
            'encontrado': False,
            'mensaje': f'Error al buscar: {str(e)}'
        }, status=400)