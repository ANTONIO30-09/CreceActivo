"""Enums de dominio del Modulo 1 (Usuarios y perfil infantil).

Son parte del contrato publico del modulo: se re-exportan desde
`modulo1_usuarios.ports.perfil_infantil_port` para que los Modulos 2 y 3
los consuman sin acoplarse a rutas internas.
"""
from __future__ import annotations

from enum import Enum

__all__ = ["Sexo", "NivelActividadFisica"]


class Sexo(str, Enum):
    """Sexo declarado del perfil infantil."""

    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"
    PREFIERO_NO_DECIR = "prefiero_no_decir"


class NivelActividadFisica(str, Enum):
    """Nivel de actividad fisica declarado por el tutor."""

    SEDENTARIO = "sedentario"
    LIGERO = "ligero"
    MODERADO = "moderado"
    ACTIVO = "activo"
    MUY_ACTIVO = "muy_activo"
