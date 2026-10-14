"""Excepciones de dominio del Modulo 3."""
from __future__ import annotations


class ErrorDominioEjercicios(ValueError):
    """Base de todos los errores del Modulo 3."""


class RegistroInvalido(ErrorDominioEjercicios):
    """Un RegistroActividad no cumple las invariantes."""


class MetaInvalida(ErrorDominioEjercicios):
    """Una MetaFamiliar no cumple las invariantes."""
