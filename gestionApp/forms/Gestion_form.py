from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Medico, Matrona, Tens
from matronaApp.models import Paciente  # ← Importar desde matronaApp
from utilidad.rut_validator import validar_rut_chileno, normalizar_rut
from datetime import date

# ============================================
# FORMULARIOS DE PERSONA
# ============================================

class PersonaForm(forms.ModelForm):
    """Formulario para registro de personas (datos básicos)"""
    
    class Meta:
        model = Persona
        fields = ['Rut', 'Nombre', 'Apellido', 'Sexo', 'Fecha_nacimiento', 'Telefono', 'Direccion', 'Email']
        widgets = {
            'Rut': forms.TextInput(attrs={'class': 'form-control','placeholder': '12345678-9','maxlength': '12','id': 'rut_input'}),
            'Nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese nombre','required': True}),
            'Apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Ingrese apellido','required': True}),
            'Sexo': forms.Select(attrs={'class': 'form-select','required': True}),
            'Fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control','type': 'date','required': True}),
            'Telefono': forms.TextInput(attrs={'class': 'form-control','placeholder': '+56912345678'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Calle, número, comuna'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'correo@ejemplo.com'})
        }
        labels = {
            'Rut': 'RUT',
            'Nombre': 'Nombre',
            'Apellido': 'Apellido',
            'Sexo': 'Sexo',
            'Fecha_nacimiento': 'Fecha de Nacimiento',
            'Telefono': 'Teléfono',
            'Direccion': 'Dirección',
            'Email': 'Correo Electrónico'
        }
    
    def clean_Rut(self):
        """Validación y normalización del RUT"""
        rut = self.cleaned_data.get('Rut')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            validar_rut_chileno(rut_normalizado)
            if not self.instance.pk:
                if Persona.objects.filter(Rut=rut_normalizado).exists():
                    raise ValidationError('Este RUT ya está registrado.')
            return rut_normalizado
        return rut
    
    def clean_Fecha_nacimiento(self):
        """Validar que la fecha de nacimiento sea coherente"""
        fecha = self.cleaned_data.get('Fecha_nacimiento')
        if fecha:
            hoy = date.today()
            edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
            if edad < 0:
                raise ValidationError('La fecha de nacimiento no puede ser futura.')
            if edad > 120:
                raise ValidationError('La fecha de nacimiento no es válida.')
        return fecha


class BuscarPersonaForm(forms.Form):
    """Formulario para búsqueda rápida de personas por RUT"""
    rut = forms.CharField(
        max_length=12,
        label="Buscar por RUT",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '12345678-9','id': 'buscar_rut','autocomplete': 'off'})
    )
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            return normalizar_rut(rut)
        return rut


# ============================================
# FORMULARIOS DE ROLES (Vinculación a Persona)
# ============================================

class PacienteForm(forms.ModelForm):
    """Formulario para vincular paciente a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_paciente'
        }),
        help_text="Ingrese el RUT de la persona a vincular como paciente"
    )
    
    class Meta:
        model = Paciente
        fields = ['Edad', 'Estado_civil', 'Previcion', 'Acompañante', 'Contacto_emergencia']
        widgets = {
            'Edad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 12,
                'max': 60
            }),
            'Estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'Previcion': forms.Select(attrs={'class': 'form-select'}),
            'Acompañante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante (opcional)'
            }),
            'Contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            }),
        }
        labels = {
            'Edad': 'Edad',
            'Estado_civil': 'Estado Civil',
            'Previcion': 'Previsión',
            'Acompañante': 'Acompañante',
            'Contacto_emergencia': 'Contacto de Emergencia'
        }

    def clean_rut_persona(self):
        """Validar que el RUT exista y no esté ya vinculado"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'paciente'):
                    raise ValidationError('Esta persona ya está registrada como paciente.')
                return persona
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return None
    
    def clean_Edad(self):
        """Validar rango de edad permitido"""
        edad = self.cleaned_data.get('Edad')
        if edad and (edad < 12 or edad > 60):
            raise ValidationError('La edad debe estar entre 12 y 60 años.')
        return edad
    
    def save(self, commit=True):
        """Guardar el paciente vinculado a la persona"""
        paciente = super().save(commit=False)
        persona = self.cleaned_data.get('rut_persona')
        
        if persona:
            paciente.persona = persona
            
        if commit:
            paciente.save()
        
        return paciente


class MedicoForm(forms.ModelForm):
    """Formulario para vincular médico a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '12345678-9','id': 'rut_persona_medico'}),
        help_text="Ingrese el RUT de la persona a vincular como médico"
    )
    
    class Meta:
        model = Medico
        fields = ['Especialidad','Registro_medico','Años_experiencia','Turno']
        widgets = {
            'Especialidad': forms.Select(attrs={'class': 'form-select'}),
            'Registro_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'Años_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'Turno': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_rut_persona(self):
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'medico'):
                    raise ValidationError('Esta persona ya está registrada como médico.')
                return persona
            except Persona.DoesNotExist:
                raise ValidationError('No existe una persona registrada con este RUT.')
        return rut
    
    def clean_Registro_medico(self):
        registro = self.cleaned_data.get('Registro_medico')
        if registro and Medico.objects.filter(Registro_medico=registro).exists():
            raise ValidationError('Este número de registro médico ya existe.')
        return registro
    
    def save(self, commit=True):
        medico = super().save(commit=False)
        persona = self.cleaned_data.get('rut_persona')
        if persona:
            medico.persona = persona
        if commit:
            medico.save()
        return medico


class MatronaForm(forms.ModelForm):
    """Formulario para vincular matrona a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '12345678-9','id': 'rut_persona_matrona'}),
        help_text="Ingrese el RUT de la persona a vincular como matrona"
    )
    
    class Meta:
        model = Matrona
        fields = ['Especialidad','Registro_medico','Años_experiencia','Turno']
        widgets = {
            'Especialidad': forms.Select(attrs={'class': 'form-select'}),
            'Registro_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'Años_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'Turno': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_rut_persona(self):
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'matrona'):
                    raise ValidationError('Esta persona ya está registrada como matrona.')
                return persona
            except Persona.DoesNotExist:
                raise ValidationError('No existe una persona registrada con este RUT.')
        return rut
    
    def clean_Registro_medico(self):
        registro = self.cleaned_data.get('Registro_medico')
        if registro and Matrona.objects.filter(Registro_medico=registro).exists():
            raise ValidationError('Este número de registro ya existe.')
        return registro
    
    def save(self, commit=True):
        matrona = super().save(commit=False)
        persona = self.cleaned_data.get('rut_persona')
        if persona:
            matrona.persona = persona
        if commit:
            matrona.save()
        return matrona


class TensForm(forms.ModelForm):
    """Formulario para vincular TENS a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '12345678-9','id': 'rut_persona_tens'}),
        help_text="Ingrese el RUT de la persona a vincular como TENS"
    )
    
    class Meta:
        model = Tens
        fields = ['Nivel','Años_experiencia','Turno','Certificaciones']
        widgets = {
            'Nivel': forms.Select(attrs={'class': 'form-select'}),
            'Años_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'Turno': forms.Select(attrs={'class': 'form-select'}),
            'Certificaciones': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_rut_persona(self):
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'tens'):
                    raise ValidationError('Esta persona ya está registrada como TENS.')
                return persona
            except Persona.DoesNotExist:
                raise ValidationError('No existe una persona registrada con este RUT.')
        return rut
    
    def save(self, commit=True):
        tens = super().save(commit=False)
        persona = self.cleaned_data.get('rut_persona')
        if persona:
            tens.persona = persona
        if commit:
            tens.save()
        return tens