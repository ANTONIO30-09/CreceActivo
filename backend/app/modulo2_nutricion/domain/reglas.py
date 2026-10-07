"""Reglas de dominio del módulo 2 (nutrición).

Sin dependencias de infraestructura ni de otros módulos.
"""
from __future__ import annotations

from .enums import RangoEdad
from .excepciones import EdadFueraDeRango

EDAD_MINIMA = 6
EDAD_MAXIMA = 14


def obtener_rango_edad(edad: int) -> RangoEdad:
    """Mapea una edad (6-14) al RangoEdad correspondiente.

    Raises:
        EdadFueraDeRango: si la edad no está entre 6 y 14 inclusive.
    """
    if not isinstance(edad, int) or isinstance(edad, bool):
        raise EdadFueraDeRango(f"La edad debe ser un entero, recibido: {type(edad).__name__}")
    if edad < EDAD_MINIMA or edad > EDAD_MAXIMA:
        raise EdadFueraDeRango(
            f"La edad debe estar entre {EDAD_MINIMA} y {EDAD_MAXIMA} años."
        )
    if edad <= 8:
        return RangoEdad.DE_6_A_8
    if edad <= 11:
        return RangoEdad.DE_9_A_11
    return RangoEdad.DE_12_A_14
