from django.db import models

class Patologias(models.Model):

    CIE_10_CHOICES = [
        ('A09 - Enfermedades diarreicas de probable origen infeccioso', 'A09 - Enfermedades diarreicas de probable origen infeccioso'),
        ('E11 - Diabetes mellitus tipo 2', 'E11 - Diabetes mellitus tipo 2'),
        ('I10 - Hipertensión esencial (primaria)', 'I10 - Hipertensión esencial (primaria)'),
        ('J00 - Resfriado común', 'J00 - Resfriado común'),
        ('F32 - Episodio depresivo mayor, episodio único', 'F32 - Episodio depresivo mayor, episodio único'),
        ('K21 - Enfermedad por reflujo gastroesofágico (ERGE)', 'K21 - Enfermedad por reflujo gastroesofágico (ERGE)'),
        ('M54 - Dolor en la columna vertebral', 'M54 - Dolor en la columna vertebral'),
        ('N39 - Infección del tracto urinario no especificada', 'N39 - Infección del tracto urinario no especificada'),
    ]

    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    
    Nivel_de_riesgo_CHOICES = [

        ('CV_Bajo', 'Cardiovascular (CV) - Bajo'),
        ('MB_Bajo', 'Metabólica (MB) - Bajo'),
        ('CV_Medio', 'Cardiovascular (CV) - Medio'),
        ('MB_Medio', 'Metabólica (MB) - Medio'),
        ('RR_Alto', 'Respiratoria (RR) - Alto'),
        ('NN_Alto', 'Neurológica (NN) - Alto'),
        ]

    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre de la patología",
        help_text="Nombre de la patología"
    )

    codigo_cie_10 = models.CharField(
        max_length=100,
        choices=CIE_10_CHOICES,
        verbose_name="Código CIE-10",
        help_text="Código CIE-10 de la patología"
    )

    descripcion = models.TextField(
        verbose_name="Descripción de la patología",
        help_text="Breve descripción de la patología"
    )

    nivel_de_riesgo = models.CharField(
        max_length=50,
        choices=Nivel_de_riesgo_CHOICES,
        verbose_name="Nivel de riesgo",
        help_text="Nivel de riesgo de la patología (Ej. Cardiovascular, Respiratoria)"
    )
    protocologo_de_segimiento = models.TextField(
        verbose_name="Protocolo de seguimiento",
        help_text="Protocolo de seguimiento de la patología"
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='Activo',
        verbose_name="Estado de la patología",
        help_text="Estado de la patología (Activo/Inactivo)"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Patología: {self.nombre} - Código: {self.codigo_cie_10}"

    class Meta:
        verbose_name = "Registro de Patología"
        verbose_name_plural = "Registros de Patologías"
        ordering = ['-fecha_creacion']
