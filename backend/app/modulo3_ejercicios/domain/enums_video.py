"""Enums del dominio de metadatos de videos (Modulo 3)."""
from __future__ import annotations
from enum import Enum

__all__ = ["Dificultad"]


class Dificultad(str, Enum):
    """Dificultad declarada de un video educativo."""
    FACIL = "facil"
    MEDIA = "media"
    DIFICIL = "dificil"
