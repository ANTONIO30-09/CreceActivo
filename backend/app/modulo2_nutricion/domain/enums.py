from enum import Enum


class RangoEdad(str, Enum):
    DE_6_A_8 = "6-8 años"
    DE_9_A_11 = "9-11 años"
    DE_12_A_14 = "12-14 años"


class TipoComida(str, Enum):
    DESAYUNO = "Desayuno"
    ALMUERZO = "Almuerzo"
    CENA = "Cena"
    MERIENDA = "Merienda"


def obtener_rango_edad(edad: int) -> RangoEdad:
    if edad < 6 or edad > 14:
        raise ValueError("La edad debe estar entre 6 y 14 años.")
    if edad <= 8:
        return RangoEdad.DE_6_A_8
    if edad <= 11:
        return RangoEdad.DE_9_A_11
    return RangoEdad.DE_12_A_14
