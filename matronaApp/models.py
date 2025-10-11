from django.db import models
from django.utils import timezone
from django.db import transaction
from gestionApp.models import Persona  # ← Importar Persona

class Paciente(models.Model):
    """Rol de Paciente vinculado a Persona"""
    
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERA', 'Soltera'),
        ('CASADA', 'Casada'),
        ('CONVIVIENTE', 'Conviviente'),
        ('DIVORCIADA', 'Divorciada'),
        ('VIUDA', 'Viuda'),
    ]
    
    PREVISION_CHOICES = [
        ('FONASA_A', 'FONASA A'),
        ('FONASA_B', 'FONASA B'),
        ('FONASA_C', 'FONASA C'),
        ('FONASA_D', 'FONASA D'),
        ('ISAPRE', 'Isapre'),
        ('PARTICULAR', 'Particular'),
    ]
    
    # Relación OneToOne con Persona
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='paciente',
        primary_key=True
    )
    
    # Datos específicos de Paciente
    Edad = models.PositiveSmallIntegerField(
        help_text="Edad entre 12 y 60 años"
    )
    Estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES)
    Previcion = models.CharField("Previsión", max_length=20, choices=PREVISION_CHOICES)
    
    Acompañante = models.CharField(max_length=120, blank=True)
    Contacto_emergencia = models.CharField(max_length=30, blank=True)
    
    # Auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.Edad and (self.Edad < 12 or self.Edad > 60):
            raise ValidationError({'Edad': 'La edad debe estar entre 12 y 60 años.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Paciente: {self.persona.Nombre} {self.persona.Apellido} ({self.persona.Rut})"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"


class IngresoPaciente(models.Model):
    """Registro de ingresos hospitalarios"""
    
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.PROTECT, 
        related_name="ingresos"
    )
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    numero_ficha = models.CharField(
        "Número de ficha", 
        max_length=32, 
        unique=True, 
        blank=True
    )
    
    motivo_consulta = models.TextField()
    edad_gestacional_sem = models.PositiveSmallIntegerField(null=True, blank=True)
    derivacion = models.CharField(max_length=120, blank=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ["-fecha_ingreso"]
    
    def __str__(self):
        return f"Ingreso {self.numero_ficha} - {self.paciente.persona.Rut}"
    
    @classmethod
    def _generar_numero_ficha(cls) -> str:
        """Genera número de ficha: F-AAAA-####"""
        year = timezone.localtime().year
        prefix = f"F-{year}-"
        
        with transaction.atomic():
            ultimo = (
                cls.objects.select_for_update()
                .filter(numero_ficha__startswith=prefix)
                .order_by("-numero_ficha")
                .first()
            )
            
            sec = 0
            if ultimo and ultimo.numero_ficha:
                try:
                    sec = int(ultimo.numero_ficha.split("-")[-1])
                except Exception:
                    sec = 0
            
            sec += 1
            numero = f"{prefix}{sec:04d}"
            
            # Verificar que no exista
            while cls.objects.filter(numero_ficha=numero).exists():
                sec += 1
                numero = f"{prefix}{sec:04d}"
            
            return numero
    
    def save(self, *args, **kwargs):
        if not self.numero_ficha:
            self.numero_ficha = self._generar_numero_ficha()
        return super().save(*args, **kwargs)


class SeleccionPatologia(models.Model):
    """Patologías asignadas al paciente"""
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="patologias_asignadas"
    )
    catalogo_id = models.PositiveIntegerField()
    nombre = models.CharField(max_length=180)
    codigo_cie_10 = models.CharField(max_length=60, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("paciente", "catalogo_id")
        ordering = ["-creado_en"]
    
    def __str__(self):
        return f"{self.nombre} ({self.codigo_cie_10})"