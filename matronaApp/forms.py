# matronaApp/forms.py
from django import forms
from django.apps import apps
from .models import IngresoPaciente, Paciente

# ---------------------------
# Form principal de Ingreso
# ---------------------------
class IngresoForm(forms.ModelForm):
    # Datos de paciente
    rut = forms.CharField(label="RUT")
    nombres = forms.CharField(label="Nombres")
    apellidos = forms.CharField(label="Apellidos")
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento", required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    telefono = forms.CharField(required=False, label="Teléfono")
    email = forms.EmailField(required=False, label="Email")
    direccion = forms.CharField(required=False, label="Dirección")

    ESTADO_CIVIL_CHOICES = [
        ("SOLTERA", "Soltera"),
        ("CASADA", "Casada"),
        ("DIVORCIADA", "Divorciada"),
        ("VIUDA", "Viuda"),
        ("CONVIVIENTE", "Conviviente"),
        ("OTRO", "Otro"),
    ]
    estado_civil = forms.ChoiceField(choices=ESTADO_CIVIL_CHOICES, label="Estado civil", required=False)
    estado_civil_otro = forms.CharField(
        required=False, label="Otro estado civil",
        widget=forms.TextInput(attrs={"class": "form-control d-none"})
    )

    PREVISION_CHOICES = [
        ("FONASA", "FONASA"),
        ("ISAPRE", "ISAPRE"),
        ("PARTICULAR", "Particular"),
        ("OTRO", "Otro"),
    ]
    prevision = forms.ChoiceField(choices=PREVISION_CHOICES, label="Previsión", required=False)
    prevision_otro = forms.CharField(
        required=False, label="Otra previsión",
        widget=forms.TextInput(attrs={"class": "form-control d-none"})
    )

    acompanante = forms.CharField(required=False, label="Acompañante")
    contacto_emergencia = forms.CharField(required=False, label="Contacto emergencia")

    class Meta:
        model = IngresoPaciente
        fields = [
            "rut","nombres","apellidos","fecha_nacimiento","telefono","email","direccion",
            "estado_civil","estado_civil_otro","prevision","prevision_otro",
            "acompanante","contacto_emergencia",
            "motivo_consulta","edad_gestacional_sem","derivacion","observaciones",
        ]
        widgets = {
            "motivo_consulta": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "edad_gestacional_sem": forms.NumberInput(attrs={"class": "form-control"}),
            "derivacion": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica Bootstrap
        for f in self.fields.values():
            w = f.widget
            if isinstance(w, (forms.TextInput, forms.EmailInput, forms.NumberInput,
                            forms.DateInput, forms.TimeInput, forms.URLInput, forms.Textarea)):
                w.attrs["class"] = (w.attrs.get("class", "") + " form-control").strip()
            elif isinstance(w, forms.Select):
                w.attrs["class"] = (w.attrs.get("class", "") + " form-select").strip()
        # Placeholders
        self.fields["rut"].widget.attrs.setdefault("placeholder", "12.345.678-9")
        self.fields["telefono"].widget.attrs.setdefault("placeholder", "+56912345678")
        self.fields["email"].widget.attrs.setdefault("placeholder", "correo@ejemplo.cl")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("estado_civil") == "OTRO":
            cleaned["estado_civil"] = cleaned.get("estado_civil_otro") or "Otro"
        if cleaned.get("prevision") == "OTRO":
            cleaned["prevision"] = cleaned.get("prevision_otro") or "Otro"
        return cleaned

    def save(self, commit=True):
        rut = self.cleaned_data["rut"]
        paciente, _ = Paciente.objects.get_or_create(rut=rut)
        for f in ("nombres","apellidos","fecha_nacimiento","telefono","email","direccion",
                "estado_civil","prevision","acompanante","contacto_emergencia"):
            setattr(paciente, f, self.cleaned_data.get(f))
        if commit:
            paciente.save()
        ingreso = super().save(commit=False)
        ingreso.paciente = paciente
        if commit:
            ingreso.save()
        return ingreso


# ------------------------------------------------
# Form para seleccionar múltiples patologías
# (NO es ModelForm: evita campo inexistente)
# ------------------------------------------------
def _get_catalogo_patologias_qs():
    candidatos = ["Patologia", "CatalogoPatologia", "PatologiaCIE10", "Enfermedad"]
    for nombre in candidatos:
        try:
            Model = apps.get_model("medicoApp", nombre)
            if not Model:
                continue
            campos = {f.name for f in Model._meta.get_fields()}
            if {"nombre", "codigo_cie_10"}.issubset(campos):
                return Model.objects.all().order_by("nombre")
        except Exception:
            continue
    return None


class SeleccionarPatologiasForm(forms.Form):
    patologias = forms.MultipleChoiceField(
        label="Seleccionar patologías (catálogo médico)",
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = _get_catalogo_patologias_qs()
        if qs is None:
            self.fields["patologias"].choices = []
            self.fields["patologias"].help_text = "No se encontró el catálogo en medicoApp."
        else:
            self.fields["patologias"].choices = [
                (str(obj.pk), f"{getattr(obj, 'nombre', '(s/n)')} — {getattr(obj, 'codigo_cie_10', '')}")
                for obj in qs
            ]
