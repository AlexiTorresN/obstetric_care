import re
from django.core.exceptions import ValidationError

def normalizar_rut(rut: str) -> str:
    """
    Limpia puntos y pasa a mayúsculas.
    Ej: '12.345.678-k' -> '12345678-K'
    """
    return rut.replace(".", "").replace(" ", "").upper()

def validar_rut_chileno(value: str) -> str:
    """
    Valida el formato y el dígito verificador del RUT chileno.
    Lanza ValidationError si no es válido.
    """
    rut = normalizar_rut(value)

    # Regex básico: 7 u 8 dígitos + guion + dígito verificador
    if not re.match(r"^\d{7,8}-[\dkK]$", rut):
        raise ValidationError("Formato RUT inválido. Ej: 12345678-9")

    cuerpo, dv = rut.split("-")
    dv = dv.upper()

    # Calcular dígito verificador
    suma, mult = 0, 2
    for c in reversed(cuerpo):
        suma += int(c) * mult
        mult = 2 if mult == 7 else mult + 1

    res = 11 - (suma % 11)
    dv_calc = "0" if res == 11 else "K" if res == 10 else str(res)

    if dv != dv_calc:
        raise ValidationError("Dígito verificador incorrecto.")

    return rut
