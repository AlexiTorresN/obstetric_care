"""
Formularios para la gestión de ingresos hospitalarios
"""
from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import IngresoPaciente, Paciente
from gestionApp.models import Persona
from utilidad.rut_validator import normalizar_rut


class IngresoPacienteForm(forms.ModelForm):
    """Formulario para registrar ingreso de paciente"""
    
    rut_paciente = forms.CharField(
        max_length=12,
        label="RUT del Paciente",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_paciente_ingreso',
            'autocomplete': 'off'
        }),
        help_text="Ingrese el RUT del paciente a ingresar"
    )
    
    class Meta:
        model = IngresoPaciente
        fields = ['motivo_consulta', 'edad_gestacional_sem', 'derivacion', 'observaciones']
        widgets = {
            'motivo_consulta': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa el motivo de consulta',
                'required': True
            }),
            'edad_gestacional_sem': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '42',
                'placeholder': 'Semanas de gestación (1-42)'
            }),
            'derivacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Centro de salud de derivación'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            })
        }
        labels = {
            'motivo_consulta': 'Motivo de Consulta',
            'edad_gestacional_sem': 'Edad Gestacional (semanas)',
            'derivacion': 'Derivación',
            'observaciones': 'Observaciones'
        }
    
    def clean_rut_paciente(self):
        """Validar que el paciente exista"""
        rut = self.cleaned_data.get('rut_paciente')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if not hasattr(persona, 'paciente'):
                    raise ValidationError(
                        'Esta persona no está registrada como paciente. '
                        'Por favor, registre primero como paciente.'
                    )
                
                return persona.paciente
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT.'
                )
        return rut
    
    def clean_edad_gestacional_sem(self):
        """Validar edad gestacional"""
        edad = self.cleaned_data.get('edad_gestacional_sem')
        if edad and (edad < 1 or edad > 42):
            raise ValidationError('La edad gestacional debe estar entre 1 y 42 semanas.')
        return edad