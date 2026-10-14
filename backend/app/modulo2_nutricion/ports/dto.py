"""DTOs publicos del Modulo 2 (Nutricion y orientacion profesional).

Read-models inmutables que el puerto expone hacia otros modulos.
No incluyen campos internos ni comportamiento de negocio.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..domain.enums import RangoEdad, TipoComida

__all__ = [
    "RangoEdad",
    "TipoComida",
    "GuiaDTO",
    "PlatoDTO",
    "MenuDTO",
    "EspecialistaDTO",
]


@dataclass(frozen=True)
class GuiaDTO:
    """Read-model publico de una guia nutricional."""

    id: str
    titulo: str
    categoria: str
    rango_edad: RangoEdad
    contenido: str
    habitos_clave: tuple[str, ...]


@dataclass(frozen=True)
class PlatoDTO:
    """Read-model publico de un plato."""

    nombre: str
    descripcion: str
    calorias_aprox: int
    ingredientes: tuple[str, ...]


@dataclass(frozen=True)
class MenuDTO:
    """Read-model publico de un menu infantil."""

    id: str
    titulo: str
    rango_edad: RangoEdad
    tipo_comida: TipoComida
    platos: tuple[PlatoDTO, ...]
    recomendaciones: tuple[str, ...]


@dataclass(frozen=True)
class EspecialistaDTO:
    """Read-model publico de un especialista."""

    id: str
    nombre_completo: str
    rol: str
    especialidad: str
    experiencia_anios: int
    biografia: str
    contacto_email: str
    disponible: bool
