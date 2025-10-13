# medicoApp/management/commands/cargar_patologias.py
"""
Comando para cargar patologías obstétricas predefinidas
Ejecutar: python manage.py cargar_patologias
"""
from django.core.management.base import BaseCommand
from medicoApp.models import Patologias


class Command(BaseCommand):
    help = 'Carga las patologías obstétricas predefinidas en el sistema'

    def handle(self, *args, **kwargs):
        patologias_data = [
            {
                'nombre': 'Hipertensión Preexistente',
                'codigo_cie_10': 'O10',
                'descripcion': 'Hipertensión arterial crónica que existía antes del embarazo o se diagnostica antes de las 20 semanas de gestación.',
                'nivel_de_riesgo': 'Alto',
                'protocolo_seguimiento': 'Control prenatal cada 2 semanas. Monitoreo de presión arterial semanal. Evaluación de función renal mensual. Doppler fetal mensual desde las 28 semanas. Ecografía de crecimiento fetal cada 3-4 semanas.'
            },
            {
                'nombre': 'Diabetes Mellitus en el Embarazo',
                'codigo_cie_10': 'O24',
                'descripcion': 'Diabetes mellitus gestacional o diabetes preexistente que complica el embarazo, parto o puerperio.',
                'nivel_de_riesgo': 'Alto',
                'protocolo_seguimiento': 'Control prenatal cada 2 semanas hasta las 32 semanas, luego semanal. Hemoglucotest diario. Control con endocrinólogo mensual. Ecografía de crecimiento fetal cada 3-4 semanas. Perfil biofísico fetal desde las 32 semanas.'
            },
            {
                'nombre': 'Preeclampsia',
                'codigo_cie_10': 'O14',
                'descripcion': 'Hipertensión gestacional con proteinuria significativa que aparece después de las 20 semanas de embarazo.',
                'nivel_de_riesgo': 'Crítico',
                'protocolo_seguimiento': 'Hospitalización según severidad. Control de presión arterial cada 4-6 horas. Monitoreo de síntomas (cefalea, alteraciones visuales, dolor epigástrico). Exámenes de laboratorio cada 48-72 horas. Evaluación fetal diaria. Considerar interrupción del embarazo según evolución.'
            },
            {
                'nombre': 'Anemia en el Embarazo',
                'codigo_cie_10': 'O99.0',
                'descripcion': 'Anemia que complica el embarazo, parto o puerperio. Hemoglobina menor a 11 g/dL en primer y tercer trimestre, o menor a 10.5 g/dL en segundo trimestre.',
                'nivel_de_riesgo': 'Medio',
                'protocolo_seguimiento': 'Control prenatal mensual. Hemograma de control cada 4-6 semanas. Suplementación con hierro y ácido fólico. Evaluar causa de anemia. Derivar a hematología si anemia severa o no responde a tratamiento.'
            },
            {
                'nombre': 'Enfermedades Endocrinas en el Embarazo',
                'codigo_cie_10': 'O99.2',
                'descripcion': 'Enfermedades del sistema endocrino que complican el embarazo, como hipotiroidismo, hipertiroidismo u otras alteraciones hormonales.',
                'nivel_de_riesgo': 'Medio',
                'protocolo_seguimiento': 'Control prenatal mensual. Control con endocrinólogo cada 6-8 semanas. Monitoreo de función tiroidea cada trimestre. Ajuste de medicación según evolución. Ecografía obstétrica según protocolo habitual.'
            },
            {
                'nombre': 'Otras Complicaciones del Embarazo',
                'codigo_cie_10': 'O26',
                'descripcion': 'Otras complicaciones específicas del embarazo no clasificadas en otra parte, como hiperemesis gravídica, complicaciones venosas, infecciones del tracto urinario recurrentes.',
                'nivel_de_riesgo': 'Medio',
                'protocolo_seguimiento': 'Control prenatal según severidad. Manejo específico según complicación. Hidratación y tratamiento sintomático. Hospitalización si hay deshidratación o descompensación. Evaluación por especialista según necesidad.'
            },
            {
                'nombre': 'Amenaza de Parto Prematuro',
                'codigo_cie_10': 'O60',
                'descripcion': 'Contracciones uterinas regulares que causan cambios cervicales antes de las 37 semanas de gestación.',
                'nivel_de_riesgo': 'Alto',
                'protocolo_seguimiento': 'Hospitalización para evaluación. Monitoreo de dinámica uterina. Evaluación cervical frecuente. Corticoides para maduración pulmonar si es pertinente. Tocolisis según protocolo. Reposo relativo. Control cada 1-2 semanas posterior al alta.'
            },
            {
                'nombre': 'Restricción del Crecimiento Fetal',
                'codigo_cie_10': 'O36.5',
                'descripcion': 'Crecimiento fetal menor al percentil 10 para la edad gestacional.',
                'nivel_de_riesgo': 'Alto',
                'protocolo_seguimiento': 'Control prenatal cada 1-2 semanas. Ecografía de crecimiento cada 2-3 semanas. Doppler fetal semanal. Perfil biofísico fetal bisemanal. Monitoreo fetal intraparto estricto. Evaluar momento y vía de interrupción del embarazo.'
            },
            {
                'nombre': 'Embarazo Múltiple',
                'codigo_cie_10': 'O30',
                'descripcion': 'Gestación de dos o más fetos.',
                'nivel_de_riesgo': 'Alto',
                'protocolo_seguimiento': 'Control prenatal cada 2-3 semanas hasta las 28 semanas, luego cada 2 semanas. Ecografía mensual para evaluar crecimiento. Monitoreo de complicaciones específicas (síndrome de transfusión feto-fetal en monocoriales). Determinar corionicidad tempranamente. Planificar vía de parto según presentación.'
            },
            {
                'nombre': 'Placenta Previa',
                'codigo_cie_10': 'O44',
                'descripcion': 'Implantación anormal de la placenta en el segmento inferior uterino que cubre parcial o totalmente el orificio cervical interno.',
                'nivel_de_riesgo': 'Crítico',
                'protocolo_seguimiento': 'Reposo pélvico estricto (no tactos vaginales, no relaciones sexuales). Ecografía transvaginal para confirmar ubicación placentaria. Hospitalización si hay sangrado. Corticoides para maduración pulmonar a las 34 semanas. Cesárea electiva entre 36-37 semanas. Plan de atención con banco de sangre disponible.'
            },
            {
                'nombre': 'Desprendimiento Prematuro de Placenta',
                'codigo_cie_10': 'O45',
                'descripcion': 'Separación prematura de la placenta normalmente insertada antes del nacimiento del feto.',
                'nivel_de_riesgo': 'Crítico',
                'protocolo_seguimiento': 'EMERGENCIA OBSTÉTRICA. Hospitalización inmediata. Monitoreo fetal continuo. Evaluación del estado materno (signos vitales, coagulación). Interrupción inmediata del embarazo según estabilidad materna y fetal. Vía de parto según condiciones obstétricas. Disponibilidad de transfusión sanguínea.'
            },
            {
                'nombre': 'Infección del Tracto Urinario en Embarazo',
                'codigo_cie_10': 'O23',
                'descripcion': 'Infección del tracto urinario que complica el embarazo, incluyendo cistitis, pielonefritis o bacteriuria asintomática.',
                'nivel_de_riesgo': 'Medio',
                'protocolo_seguimiento': 'Urocultivo de control 1-2 semanas post-tratamiento. Profilaxis antibiótica si infecciones recurrentes. Evaluación de función renal. Control prenatal según protocolo habitual. Descartar diabetes gestacional. Derivar a urología si infecciones persistentes.'
            },
        ]

        creadas = 0
        actualizadas = 0

        for data in patologias_data:
            patologia, created = Patologias.objects.update_or_create(
                codigo_cie_10=data['codigo_cie_10'],
                defaults={
                    'nombre': data['nombre'],
                    'descripcion': data['descripcion'],
                    'nivel_de_riesgo': data['nivel_de_riesgo'],
                    'protocolo_seguimiento': data['protocolo_seguimiento'],
                    'estado': 'Inactivo'  # Por defecto inactivas, el médico las activa
                }
            )
            
            if created:
                creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Creada: {patologia.nombre}')
                )
            else:
                actualizadas += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Actualizada: {patologia.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Proceso completado: {creadas} creadas, {actualizadas} actualizadas'
            )
        )