"""Tests del endpoint /modulo1/tutores/sync sin Mongo."""
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient

from app.core.security import verificar_firebase_token
from app.main import app
from app.modulo1_usuarios.adapters.api.router import get_tutor_repository


class _FakeRepo:
    def __init__(self):
        self.llamadas = []
    async def sincronizar(self, uid, email, nombre=""):
        self.llamadas.append((uid, email, nombre))
        return {"_id": uid, "email": email, "nombre": nombre or email.split("@")[0]}


def _user():
    return {"uid": "u1", "email": "maria@creceactivo.bo"}


@pytest.fixture
def client():
    app.dependency_overrides[verificar_firebase_token] = _user
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_sync_crea_tutor(client):
    repo = _FakeRepo()
    app.dependency_overrides[get_tutor_repository] = lambda: repo
    r = client.post("/modulo1/tutores/sync", json={"nombre": "María López"})
    assert r.status_code == 200
    assert r.json() == {"uid": "u1", "email": "maria@creceactivo.bo", "nombre": "María López"}
    assert repo.llamadas == [("u1", "maria@creceactivo.bo", "María López")]


def test_sync_sin_nombre(client):
    repo = _FakeRepo()
    app.dependency_overrides[get_tutor_repository] = lambda: repo
    r = client.post("/modulo1/tutores/sync", json={})
    assert r.status_code == 200
    assert r.json()["nombre"] == "maria"
