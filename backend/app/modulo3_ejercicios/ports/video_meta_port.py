"""Contrato publico de metadatos de videos (Modulo 3)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

from app.modulo3_ejercicios.domain.archivo_video import GrupoEdad
from app.modulo3_ejercicios.domain.enums_video import Dificultad

__all__ = ["VideoMetaDTO", "VideoMetaPort"]


@dataclass(frozen=True)
class VideoMetaDTO:
    id: UUID
    titulo: str
    descripcion: str
    grupo_edad: GrupoEdad
    duracion_seg: int
    dificultad: Dificultad
    materiales: tuple[str, ...]
    recomendaciones_seguridad: tuple[str, ...]


@runtime_checkable
class VideoMetaPort(Protocol):
    """Lectura de metadatos de videos educativos.

    Semantica:
    - Sin resultados -> lista vacia.
    - Video inexistente o inactivo -> None.
    """

    async def listar(self, grupo: GrupoEdad | None = None) -> list[VideoMetaDTO]: ...

    async def obtener(self, video_id: UUID) -> VideoMetaDTO | None: ...
