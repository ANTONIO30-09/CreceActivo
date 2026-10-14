"""Repositorio Mongo de metadatos de videos (Modulo 3)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from app.modulo3_ejercicios.domain.archivo_video import GrupoEdad
from app.modulo3_ejercicios.domain.enums_video import Dificultad
from app.modulo3_ejercicios.domain.video_meta import VideoMeta
from app.modulo3_ejercicios.ports.video_meta_port import VideoMetaDTO

from .validadores import COLLECTION_VIDEOS_META

__all__ = ["VideoMetaRepository"]


def _a_utc(valor: datetime | None) -> datetime:
    if valor is None:
        return datetime.now(timezone.utc)
    if valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor


def _doc_a_meta(doc: dict[str, Any]) -> VideoMeta:
    return VideoMeta(
        id=UUID(doc["_id"]),
        titulo=doc["titulo"],
        descripcion=doc.get("descripcion") or "",
        grupo_edad=GrupoEdad(doc["grupo_edad"]),
        duracion_seg=int(doc["duracion_seg"]),
        dificultad=Dificultad(doc["dificultad"]),
        materiales=tuple(doc.get("materiales") or ()),
        recomendaciones_seguridad=tuple(doc.get("recomendaciones_seguridad") or ()),
        activo=bool(doc.get("activo", True)),
        url_demo=doc.get("url_demo"),
        creado_en=_a_utc(doc.get("creado_en")),
    )


def _a_dto(m: VideoMeta) -> VideoMetaDTO:
    return VideoMetaDTO(
        id=m.id, titulo=m.titulo, descripcion=m.descripcion,
        grupo_edad=m.grupo_edad, duracion_seg=m.duracion_seg,
        dificultad=m.dificultad, materiales=m.materiales,
        recomendaciones_seguridad=m.recomendaciones_seguridad,
        url_demo=m.url_demo,
    )


class VideoMetaRepository:
    """Implementacion Mongo del VideoMetaPort."""

    def __init__(self, db: Any) -> None:
        self._col = db[COLLECTION_VIDEOS_META]

    async def listar(self, grupo: GrupoEdad | None = None) -> list[VideoMetaDTO]:
        filtro: dict[str, Any] = {"activo": True}
        if grupo is not None:
            filtro["grupo_edad"] = grupo.value
        cursor = self._col.find(filtro).sort("titulo", 1)
        docs = await cursor.to_list(length=None)
        return [_a_dto(_doc_a_meta(d)) for d in docs]

    async def obtener(self, video_id: UUID) -> VideoMetaDTO | None:
        doc = await self._col.find_one({"_id": str(video_id), "activo": True})
        return None if doc is None else _a_dto(_doc_a_meta(doc))
