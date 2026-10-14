"""Entidad de metadatos de video educativo (Modulo 3).

No accede a Firebase ni a Mongo. Solo describe el video: que se
necesita, cuanto dura, para que edad es y que precauciones tomar.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from .archivo_video import GrupoEdad
from .enums_video import Dificultad

MAX_TITULO = 120
MAX_DESCRIPCION = 500


@dataclass(frozen=True)
class VideoMeta:
    id: UUID
    titulo: str
    descripcion: str
    grupo_edad: GrupoEdad
    duracion_seg: int
    dificultad: Dificultad
    materiales: tuple[str, ...]
    recomendaciones_seguridad: tuple[str, ...]
    activo: bool = True
    url_demo: str | None = None
    creado_en: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.id, UUID):
            raise ValueError("id debe ser UUID")
        if not self.titulo or not self.titulo.strip():
            raise ValueError("titulo obligatorio")
        if len(self.titulo) > MAX_TITULO:
            raise ValueError(f"titulo > {MAX_TITULO}")
        if len(self.descripcion) > MAX_DESCRIPCION:
            raise ValueError(f"descripcion > {MAX_DESCRIPCION}")
        if not isinstance(self.grupo_edad, GrupoEdad):
            raise ValueError("grupo_edad invalido")
        if self.duracion_seg <= 0 or self.duracion_seg > 3600:
            raise ValueError("duracion_seg fuera de rango")
        if not isinstance(self.dificultad, Dificultad):
            raise ValueError("dificultad invalida")
        for m in self.materiales:
            if not isinstance(m, str) or not m.strip():
                raise ValueError("material vacio")
        for r in self.recomendaciones_seguridad:
            if not isinstance(r, str) or not r.strip():
                raise ValueError("recomendacion vacia")
        if self.creado_en is None:
            object.__setattr__(self, "creado_en", datetime.now(timezone.utc))
        elif self.creado_en.tzinfo is None:
            object.__setattr__(
                self, "creado_en",
                self.creado_en.replace(tzinfo=timezone.utc),
            )
