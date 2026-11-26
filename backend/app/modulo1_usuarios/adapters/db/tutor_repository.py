"""Repositorio Mongo de tutores (Modulo 1)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .tutores import COLLECTION_TUTORES

__all__ = ["TutorRepository"]


class TutorRepository:
    """CRUD minimo sobre la coleccion `tutores`."""

    def __init__(self, db: Any) -> None:
        self._col = db[COLLECTION_TUTORES]

    async def sincronizar(
        self, uid: str, email: str, nombre: str = ""
    ) -> dict[str, Any]:
        """Crea o actualiza el documento del tutor autenticado."""
        ahora = datetime.now(timezone.utc)
        await self._col.update_one(
            {"_id": uid},
            {
                "$set": {
                    "email": email,
                    "nombre": nombre or email.split("@")[0],
                    "actualizado_en": ahora,
                },
                "$setOnInsert": {"creado_en": ahora},
            },
            upsert=True,
        )
        return await self._col.find_one({"_id": uid})
