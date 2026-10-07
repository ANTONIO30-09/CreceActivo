"""Enums del dominio de nutrición. Sin lógica."""
from __future__ import annotations

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
