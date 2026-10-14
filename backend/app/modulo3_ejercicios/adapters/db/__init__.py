"""Capa de persistencia del Modulo 3."""
from .progreso_repository import ProgresoRepository
from .validadores import asegurar_colecciones_modulo3
from .video_meta_repository import VideoMetaRepository

__all__ = [
    "ProgresoRepository",
    "VideoMetaRepository",
    "asegurar_colecciones_modulo3",
]
