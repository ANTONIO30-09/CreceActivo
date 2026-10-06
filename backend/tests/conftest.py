"""Configuracion global de pytest.

Fija variables de entorno ANTES de que se importe la app, para que
pydantic-settings construya Settings sin depender del .env real.
"""
from __future__ import annotations

import os
from unittest.mock import AsyncMock, patch

import pytest

os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017")
os.environ.setdefault("MONGODB_DB_NAME", "test_db")
os.environ.setdefault("FIREBASE_PROJECT_ID", "test-project")
os.environ.setdefault(
    "FIREBASE_SERVICE_ACCOUNT_PATH", "/tmp/nonexistent-service-account.json"
)


@pytest.fixture
def client():
    """TestClient con lifespan mockeado (sin Firebase real ni Mongo real)."""
    from fastapi.testclient import TestClient

    mock_db = AsyncMock()
    mock_db.command = AsyncMock(return_value={"ok": 1})

    with patch("app.main.inicializar_firebase"), \
         patch("app.main.conectar_mongodb", new_callable=AsyncMock), \
         patch("app.main.cerrar_mongodb", new_callable=AsyncMock), \
         patch(
             "app.modulo1_usuarios.adapters.api.router.get_db",
             return_value=mock_db,
         ):
        from app.main import app

        with TestClient(app) as test_client:
            yield test_client
