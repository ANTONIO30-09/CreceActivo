"""Schemas HTTP de metadatos de videos (Modulo 3)."""
from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.modulo3_ejercicios.domain.archivo_video import GrupoEdad
from app.modulo3_ejercicios.domain.enums_video import Dificultad

__all__ = ["VideoMetaResponse"]


class VideoMetaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    titulo: str
    descripcion: str
    grupo_edad: GrupoEdad
    duracion_seg: int
    dificultad: Dificultad
    materiales: list[str]
    recomendaciones_seguridad: list[str]
