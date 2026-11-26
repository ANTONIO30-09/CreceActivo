"""Entrega acceso temporal a la biblioteca educativa para tutores autenticados."""
from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import verificar_firebase_token
from app.modulo3_ejercicios.adapters.api.schemas_video import VideoMetaResponse
from app.modulo3_ejercicios.adapters.db.video_meta_repository import VideoMetaRepository
from app.modulo3_ejercicios.adapters.storage.firebase_video_storage import FirebaseVideoStorage
from app.modulo3_ejercicios.ports.video_meta_port import VideoMetaPort
from app.modulo3_ejercicios.ports.video_storage_port import (
    GrupoEdad, StorageNoDisponibleError, VideoNoEncontradoError, VideoStoragePort,
)

router = APIRouter(prefix="/modulo3", tags=["modulo3-storage"])


class AccesoVideoResponse(BaseModel):
    url: str
    expires_at: datetime


def get_video_meta_repository(db=Depends(get_db)) -> VideoMetaRepository:
    return VideoMetaRepository(db)


def get_video_storage() -> VideoStoragePort:
    settings = get_settings()
    try:
        return FirebaseVideoStorage(settings.firebase_storage_bucket,
                                    settings.video_url_ttl_seconds)
    except ValueError as exc:
        raise HTTPException(503, "Storage no configurado") from exc


@router.get("/videos/{grupo_edad}/{video_id}/url", response_model=AccesoVideoResponse)
async def obtener_url_video(
    grupo_edad: GrupoEdad,
    video_id: UUID,
    response: Response,
    usuario: dict = Depends(verificar_firebase_token),
    storage: VideoStoragePort = Depends(get_video_storage),
) -> AccesoVideoResponse:
    try:
        acceso = await storage.obtener_acceso(grupo_edad, video_id)
    except VideoNoEncontradoError as exc:
        raise HTTPException(404, "Video no encontrado") from exc
    except StorageNoDisponibleError as exc:
        raise HTTPException(503, "Storage no disponible") from exc
    response.headers["Cache-Control"] = "no-store"
    return AccesoVideoResponse(url=acceso.url, expires_at=acceso.expires_at)


# ---------------- Metadatos de videos (RF-11) ----------------


@router.get("/videos", response_model=list[VideoMetaResponse])
async def listar_videos(
    grupo_edad: GrupoEdad | None = None,
    usuario: dict = Depends(verificar_firebase_token),
    repo: VideoMetaPort = Depends(get_video_meta_repository),
) -> list[VideoMetaResponse]:
    """Lista metadatos de videos, opcionalmente filtrado por grupo de edad."""
    metas = await repo.listar(grupo_edad)
    return [VideoMetaResponse.model_validate(m) for m in metas]


@router.get("/videos/{video_id}", response_model=VideoMetaResponse)
async def obtener_video(
    video_id: UUID,
    usuario: dict = Depends(verificar_firebase_token),
    repo: VideoMetaPort = Depends(get_video_meta_repository),
) -> VideoMetaResponse:
    """Devuelve los metadatos de un video concreto."""
    meta = await repo.obtener(video_id)
    if meta is None:
        raise HTTPException(404, "Video no encontrado")
    return VideoMetaResponse.model_validate(meta)
