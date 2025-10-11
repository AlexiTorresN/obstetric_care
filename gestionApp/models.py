from django.db import models
from utilidad.rut_validator import validar_rut, normalizar_rut, validar_rut_chileno

# ============================================
# MODELO BASE: PERSONA
# ============================================
class Persona(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    ]

    Rut = models.CharField(
        max_length=100,
        unique=True,
        validators=[validar_rut_chileno],
        verbose_name="RUT",
        help_text="Ingrese RUT de la persona (formato: 12345678-9)"
    )
    Nombre = models.CharField(max_length=100, verbose_name="Nombre")
    Apellido = models.CharField(max_length=100, verbose_name="Apellido")
    Sexo = models.CharField(max_length=100, choices=SEXO_CHOICES, verbose_name="Sexo")
    Fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    Telefono = models.CharField(max_length=100, verbose_name="Telefono", blank=True)
    Direccion = models.CharField(max_length=100, verbose_name="Direccion", blank=True)
    Email = models.CharField(max_length=100, verbose_name="Email", blank=True)
    Activo = models.BooleanField(default=True, verbose_name="Activo")

    def save(self, *args, **kwargs):
        if self.Rut:
            self.Rut = normalizar_rut(self.Rut)
            validar_rut_chileno(self.Rut)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Nombre} {self.Apellido} - {self.Rut}"


# ============================================
# MODELO MÉDICO
# ============================================
class Medico(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Obstetricia General', 'Obstetricia General'),
        ('Ginecología', 'Ginecología'),
        ('Medicina Materno Fetal', 'Medicina Materno Fetal'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.persona.Nombre} {self.persona.Apellido} - {self.Especialidad}"


# ============================================
# MODELO MATRONA
# ============================================
class Matrona(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Atención del Parto', 'Atención del Parto'),
        ('Control Prenatal', 'Control Prenatal'),
        ('Neonatología', 'Neonatología'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Matrona: {self.persona.Nombre} {self.persona.Apellido}"


# ============================================
# MODELO TENS
# ============================================
class Tens(models.Model):
    NIVEL_CHOICES = [
        ('Preparto', 'Preparto'),
        ('Parto', 'Parto'),
        ('Puerperio', 'Puerperio'),
        ('Neonatología', 'Neonatología'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    CERTIFICACION_CHOICES = [
        ('SVB', 'Soporte Vital Básico'),
        ('Parto Normal', 'Certificación en Parto Normal'),
    ]

    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Nivel = models.CharField(max_length=100, choices=NIVEL_CHOICES)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Certificaciones = models.CharField(max_length=100, choices=CERTIFICACION_CHOICES)
    Activo = models.BooleanField(default=True)

    def __str__(self):
        return f"TENS: {self.persona.Nombre} {self.persona.Apellido} - {self.Nivel}"
