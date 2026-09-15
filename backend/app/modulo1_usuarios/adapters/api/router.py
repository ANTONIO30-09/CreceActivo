"""Routers HTTP del Modulo 1.

Fase 2: solo health + whoami (verificacion de arranque y de auth).
Fase 3: aqui viviran los endpoints CRUD de PerfilInfantil.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import verificar_firebase_token

router = APIRouter(prefix="/modulo1", tags=["modulo1"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Health publico: estado de la app y de la conexion a Mongo."""
    settings = get_settings()
    db_status = "ok"
    try:
        db = get_db()
        await db.command("ping")
    except Exception:  # noqa: BLE001
        db_status = "error"

    return {
        "status": "ok",
        "env": settings.app_env,
        "db": db_status,
    }


@router.get("/whoami")
async def whoami(
    user: dict[str, Any] = Depends(verificar_firebase_token),
) -> dict[str, Any]:
    """Endpoint protegido: devuelve el uid/email del token Bearer."""
    return {"uid": user["uid"], "email": user.get("email")}
