"""
Formularios para la gestión de patologías
"""
from django import forms
from medicoApp.models import Patologias


class RegistrarPatologiaForm(forms.ModelForm):
    """Formulario para registrar patologías"""
    
    class Meta:
        model = Patologias
        fields = ['nombre', 'codigo_cie_10', 'descripcion', 
                  'nivel_de_riesgo', 'protocologo_de_segimiento', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la patología',
                'required': True
            }),
            'codigo_cie_10': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción de la patología',
                'rows': 3,
                'required': True
            }),
            'nivel_de_riesgo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'protocologo_de_segimiento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el protocolo de seguimiento',
                'rows': 4,
                'required': True
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }
        labels = {
            'nombre': 'Nombre de la Patología',
            'codigo_cie_10': 'Código CIE-10',
            'descripcion': 'Descripción',
            'nivel_de_riesgo': 'Nivel de Riesgo',
            'protocologo_de_segimiento': 'Protocolo de Seguimiento',
            'estado': 'Estado'
        }


class EditarPatologiaForm(forms.ModelForm):
    """Formulario para editar patologías existentes"""
    
    class Meta:
        model = Patologias
        fields = ['nombre', 'codigo_cie_10', 'descripcion', 
                  'nivel_de_riesgo', 'protocologo_de_segimiento', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la patología'
            }),
            'codigo_cie_10': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la descripción de la patología',
                'rows': 3
            }),
            'nivel_de_riesgo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'protocologo_de_segimiento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el protocolo de seguimiento',
                'rows': 4
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Patología',
            'codigo_cie_10': 'Código CIE-10',
            'descripcion': 'Descripción',
            'nivel_de_riesgo': 'Nivel de Riesgo',
            'protocologo_de_segimiento': 'Protocolo de Seguimiento',
            'estado': 'Estado'
        }