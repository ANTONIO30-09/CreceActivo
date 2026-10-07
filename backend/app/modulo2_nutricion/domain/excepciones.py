"""Excepciones de dominio del módulo 2 (nutrición).

Heredan de ValueError para no romper código que ya capture ese tipo,
pero permiten capturar el caso específico cuando haga falta.
"""
from __future__ import annotations


class ErrorDominioNutricion(ValueError):
    """Base de todos los errores de dominio del módulo 2."""


class EdadFueraDeRango(ErrorDominioNutricion):
    """La edad no está en el rango 6-14 años."""


class PlatoInvalido(ErrorDominioNutricion):
    """Un Plato no cumple las invariantes del dominio."""


class MenuInvalido(ErrorDominioNutricion):
    """Un MenuInfantil no cumple las invariantes del dominio."""
