"""Capa de persistencia del Modulo 2.

Los esquemas y validadores de las colecciones viven aqui.
El repositorio que implementa ContenidoNutricionalPort tambien.
"""
from .nutricion_repository import NutricionRepository
from .validadores import asegurar_colecciones_modulo2

__all__ = [
    "NutricionRepository",
    "asegurar_colecciones_modulo2",
]
