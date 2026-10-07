"""Contrato publico para almacenar videos educativos, no datos infantiles."""
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol
from uuid import UUID

from app.modulo3_ejercicios.domain.archivo_video import GrupoEdad


@dataclass(frozen=True)
class VideoAlmacenadoDTO:
    video_id: UUID
    grupo_edad: GrupoEdad
    storage_path: str


@dataclass(frozen=True)
class AccesoVideoDTO:
    url: str
    expires_at: datetime


class VideoNoEncontradoError(Exception):
    pass


class VideoYaExisteError(Exception):
    pass


class StorageNoDisponibleError(Exception):
    pass


class VideoStoragePort(Protocol):
    async def subir_video(self, archivo: Path, grupo: GrupoEdad,
                          video_id: UUID) -> VideoAlmacenadoDTO: ...

    async def obtener_acceso(self, grupo: GrupoEdad,
                             video_id: UUID) -> AccesoVideoDTO: ...
