"""Verificacion de tokens de Firebase Auth en el backend.

Usa Firebase Admin SDK para validar firma, expiracion y revocacion.
La dependencia `verificar_firebase_token` se inyecta en endpoints protegidos
y devuelve un dict con `uid` y `email`.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import firebase_admin
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials

from .config import get_settings

__all__ = ["inicializar_firebase", "verificar_firebase_token"]

_bearer = HTTPBearer(auto_error=False)


def inicializar_firebase() -> None:
    """Inicializa Firebase Admin una sola vez por proceso."""
    if firebase_admin._apps:  # type: ignore[attr-defined]
        return

    settings = get_settings()
    cred_path = Path(settings.firebase_service_account_path)
    if not cred_path.exists():
        raise RuntimeError(
            f"No existe el service account de Firebase: {cred_path}. "
            "Revisa FIREBASE_SERVICE_ACCOUNT_PATH en tu .env."
        )

    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(
        cred, {"projectId": settings.firebase_project_id}
    )


async def verificar_firebase_token(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict[str, Any]:
    """Valida el token Bearer y devuelve {uid, email}."""
    if creds is None or not creds.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        decoded = firebase_auth.verify_id_token(creds.credentials)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return {"uid": decoded["uid"], "email": decoded.get("email")}
