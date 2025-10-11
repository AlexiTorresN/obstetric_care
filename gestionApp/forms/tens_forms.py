"""
Formularios para la gestión de TENS
"""
from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Tens
from utilidad.rut_validator import normalizar_rut, validar_rut, validar_rut_chileno


class TensForm(forms.ModelForm):
    """Formulario para vincular TENS a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_tens'
        }),
        help_text="Ingrese el RUT de la persona a vincular como TENS"
    )
    
    class Meta:
        model = Tens
        fields = ['Nivel', 'Años_experiencia', 'Turno', 'Certificaciones']
        widgets = {
            'Nivel': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '50',
                'required': True
            }),
            'Turno': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Certificaciones': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            })
        }
        labels = {
            'Nivel': 'Nivel TENS',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo',
            'Certificaciones': 'Certificaciones'
        }
    
    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya TENS"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'tens'):
                    raise ValidationError(
                        f'Esta persona ya está registrada como TENS.'
                    )
                
                return persona
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return rut