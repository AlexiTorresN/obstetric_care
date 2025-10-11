from django import forms
from .models import Patologias, Tratamientos

# registrar patologia
class RegistrarPatologia(forms.ModelForm):
    class Meta:
        model = Tratamientos
        fields = ['nombre', 'codigo_cie_10', 'descripcion', 'nivel_de_riesgo', 'protocologo_de_segimiento', 'estado']
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de la patología'}),
            'codigo_cie_10': forms.Select(attrs={'class': 'form-control'}, choices=Patologias.CIE_10_CHOICES),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción de la patología'}),
            'nivel_de_riesgo': forms.Select(attrs={'class': 'form-control'}, choices=Patologias.Nivel_de_riesgo_CHOICES),
            'protocologo_de_segimiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el protocolo de seguimiento'}),
            'estado': forms.Select(attrs={'class': 'form-control'}, choices=Patologias.ESTADO_CHOICES),

        }