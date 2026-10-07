"""Firebase Admin es sincronico: sus operaciones se ejecutan fuera del event loop."""
import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import UUID

from firebase_admin import storage
from google.api_core.exceptions import GoogleAPIError, NotFound, PreconditionFailed

from app.modulo3_ejercicios.domain.archivo_video import GrupoEdad, ruta_video, validar_video
from app.modulo3_ejercicios.ports.video_storage_port import (
    AccesoVideoDTO, StorageNoDisponibleError, VideoAlmacenadoDTO,
    VideoNoEncontradoError, VideoYaExisteError,
)


class FirebaseVideoStorage:
    def __init__(self, bucket_name: str, ttl_seconds: int = 900):
        if not bucket_name or "/" in bucket_name or ":" in bucket_name:
            raise ValueError("Configura FIREBASE_STORAGE_BUCKET con el nombre, sin gs://")
        if not 60 <= ttl_seconds <= 3600:
            raise ValueError("El TTL debe estar entre 60 y 3600 segundos")
        self.bucket_name = bucket_name
        self.ttl_seconds = ttl_seconds

    async def subir_video(self, archivo: Path, grupo: GrupoEdad,
                          video_id: UUID) -> VideoAlmacenadoDTO:
        return await asyncio.to_thread(self._subir_video, archivo, grupo, video_id)

    def _subir_video(self, archivo: Path, grupo: GrupoEdad,
                     video_id: UUID) -> VideoAlmacenadoDTO:
        validar_video(archivo)
        ruta = ruta_video(grupo, video_id)
        try:
            blob = storage.bucket(self.bucket_name).blob(ruta)
            blob.cache_control = "private, max-age=0, no-store"
            # La precondicion impide sobrescribir un objeto existente.
            blob.upload_from_filename(str(archivo), content_type="video/mp4",
                                      if_generation_match=0)
        except PreconditionFailed as exc:
            raise VideoYaExisteError(str(video_id)) from exc
        except (GoogleAPIError, ValueError, OSError) as exc:
            raise StorageNoDisponibleError("No se pudo subir el video") from exc
        return VideoAlmacenadoDTO(video_id, grupo, ruta)

    async def obtener_acceso(self, grupo: GrupoEdad,
                             video_id: UUID) -> AccesoVideoDTO:
        return await asyncio.to_thread(self._obtener_acceso, grupo, video_id)

    def _obtener_acceso(self, grupo: GrupoEdad, video_id: UUID) -> AccesoVideoDTO:
        ruta = ruta_video(grupo, video_id)
        try:
            blob = storage.bucket(self.bucket_name).blob(ruta)
            blob.reload()
            expires_at = datetime.now(timezone.utc) + timedelta(seconds=self.ttl_seconds)
            url = blob.generate_signed_url(
                version="v4", expiration=expires_at, method="GET",
                response_type="video/mp4",
            )
        except NotFound as exc:
            raise VideoNoEncontradoError(str(video_id)) from exc
        except (GoogleAPIError, ValueError, AttributeError, OSError) as exc:
            raise StorageNoDisponibleError("No se pudo obtener acceso al video") from exc
        return AccesoVideoDTO(url, expires_at)
