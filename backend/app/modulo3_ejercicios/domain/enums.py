"""Enums del dominio del Modulo 3."""
from __future__ import annotations

from enum import Enum


class TipoActividad(str, Enum):
    """Tipos de actividad que un tutor puede registrar por perfil."""
    RUTINA = "rutina"
    AGUA = "agua"
    MINUTOS = "minutos"


class EstadoMeta(str, Enum):
    """Estado de una meta familiar."""
    ACTIVA = "activa"
    ARCHIVADA = "archivada"
