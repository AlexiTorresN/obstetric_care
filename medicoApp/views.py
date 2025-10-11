from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Patologias


# ============================================
# VISTAS DE PATOLOGÍAS
# ============================================

class PatologiaListView(ListView):
    """Listado de todas las patologías del catálogo"""
    model = Patologias
    template_name = 'medico/patologia_list.html'
    context_object_name = 'patologias'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Patologias.objects.all()
        
        # Filtrar por estado si se proporciona
        estado = self.request.GET.get('estado', '')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtrar por nivel de riesgo
        nivel_riesgo = self.request.GET.get('nivel_riesgo', '')
        if nivel_riesgo:
            queryset = queryset.filter(nivel_de_riesgo__contains=nivel_riesgo)
        
        # Buscar por nombre o código
        buscar = self.request.GET.get('q', '')
        if buscar:
            queryset = queryset.filter(
                nombre__icontains=buscar
            ) | queryset.filter(
                codigo_cie_10__icontains=buscar
            )
        
        return queryset.order_by('-fecha_creacion')


class PatologiaDetailView(DetailView):
    """Vista de detalle de una patología específica"""
    model = Patologias
    template_name = 'medico/patologia_detail.html'
    context_object_name = 'patologia'


def registrar_patologia(request):
    """Registrar una nueva patología en el catálogo"""
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre', '').strip()
            codigo_cie_10 = request.POST.get('codigo_cie_10', '')
            descripcion = request.POST.get('descripcion', '').strip()
            nivel_de_riesgo = request.POST.get('nivel_de_riesgo', '')
            protocolo = request.POST.get('protocologo_de_segimiento', '').strip()
            estado = request.POST.get('estado', 'Activo')
            
            # Validaciones básicas
            if not nombre or not codigo_cie_10 or not nivel_de_riesgo:
                messages.error(request, "Los campos nombre, código CIE-10 y nivel de riesgo son obligatorios.")
                return render(request, 'medico/registrar_patologia.html', {
                    'form_data': request.POST
                })
            
            # Crear la patología
            patologia = Patologias.objects.create(
                nombre=nombre,
                codigo_cie_10=codigo_cie_10,
                descripcion=descripcion,
                nivel_de_riesgo=nivel_de_riesgo,
                protocologo_de_segimiento=protocolo,
                estado=estado
            )
            
            messages.success(request, f"Patología '{patologia.nombre}' registrada correctamente.")
            return redirect('medico:detalle_patologia', pk=patologia.pk)
            
        except Exception as e:
            messages.error(request, f"Error al registrar la patología: {str(e)}")
            return render(request, 'medico/registrar_patologia.html', {
                'form_data': request.POST
            })
    
    # GET: mostrar formulario vacío
    return render(request, 'medico/registrar_patologia.html', {
        'cie_10_choices': Patologias.CIE_10_CHOICES,
        'nivel_riesgo_choices': Patologias.Nivel_de_riesgo_CHOICES,
        'estado_choices': Patologias.ESTADO_CHOICES,
    })


def editar_patologia(request, pk):
    """Editar una patología existente"""
    patologia = get_object_or_404(Patologias, pk=pk)
    
    if request.method == "POST":
        try:
            # Actualizar datos
            patologia.nombre = request.POST.get('nombre', '').strip()
            patologia.codigo_cie_10 = request.POST.get('codigo_cie_10', '')
            patologia.descripcion = request.POST.get('descripcion', '').strip()
            patologia.nivel_de_riesgo = request.POST.get('nivel_de_riesgo', '')
            patologia.protocologo_de_segimiento = request.POST.get('protocologo_de_segimiento', '').strip()
            patologia.estado = request.POST.get('estado', 'Activo')
            
            # Validaciones
            if not patologia.nombre or not patologia.codigo_cie_10 or not patologia.nivel_de_riesgo:
                messages.error(request, "Los campos nombre, código CIE-10 y nivel de riesgo son obligatorios.")
                return render(request, 'medico/editar_patologia.html', {
                    'patologia': patologia,
                    'cie_10_choices': Patologias.CIE_10_CHOICES,
                    'nivel_riesgo_choices': Patologias.Nivel_de_riesgo_CHOICES,
                    'estado_choices': Patologias.ESTADO_CHOICES,
                })
            
            patologia.save()
            messages.success(request, "Patología actualizada correctamente.")
            return redirect('medico:detalle_patologia', pk=patologia.pk)
            
        except Exception as e:
            messages.error(request, f"Error al actualizar la patología: {str(e)}")
    
    # GET: mostrar formulario con datos actuales
    return render(request, 'medico/editar_patologia.html', {
        'patologia': patologia,
        'cie_10_choices': Patologias.CIE_10_CHOICES,
        'nivel_riesgo_choices': Patologias.Nivel_de_riesgo_CHOICES,
        'estado_choices': Patologias.ESTADO_CHOICES,
    })


# ============================================
# API REST (AJAX)
# ============================================

@require_POST
def cambiar_estado_patologia(request, pk):
    """Cambiar el estado de una patología (Activo/Inactivo) vía AJAX"""
    try:
        patologia = get_object_or_404(Patologias, pk=pk)
        
        # Alternar estado
        if patologia.estado == 'Activo':
            patologia.estado = 'Inactivo'
        else:
            patologia.estado = 'Activo'
        
        patologia.save()
        
        return JsonResponse({
            'success': True,
            'nuevo_estado': patologia.estado,
            'mensaje': f"Patología cambiada a estado: {patologia.estado}"
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)