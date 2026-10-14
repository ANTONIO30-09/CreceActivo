from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.core.security import verificar_firebase_token
from app.main import app
from app.modulo3_ejercicios.adapters.api.router_progreso import (
    get_progreso_repository,
)


class RepoMetas:
    """La meta m1 es del tutor-A. Escribir sobre ella esta prohibido en el test."""

    def __init__(self):
        self.consultas = []

    async def obtener_meta(self, meta_id):
        self.consultas.append(meta_id)
        if meta_id == "m1":
            return SimpleNamespace(id="m1", tutor_id="tutor-A")
        return None

    async def marcar_meta(self, *a, **k):
        raise AssertionError("marcar_meta no debia ejecutarse")

    async def archivar_meta(self, *a, **k):
        raise AssertionError("archivar_meta no debia ejecutarse")


def _llamar(metodo, ruta, **kw):
    repo = RepoMetas()
    app.dependency_overrides[verificar_firebase_token] = lambda: {"uid": "tutor-B"}
    app.dependency_overrides[get_progreso_repository] = lambda: repo
    try:
        r = getattr(TestClient(app), metodo)(ruta, **kw)
    finally:
        app.dependency_overrides.clear()
    return r, repo


def test_tutor_no_puede_marcar_meta_ajena():
    r, repo = _llamar("post", "/modulo3/metas/m1/marcar", json={"fecha": "2026-10-07"})
    assert r.status_code == 404
    assert repo.consultas == ["m1"]


def test_tutor_no_puede_archivar_meta_ajena():
    r, repo = _llamar("delete", "/modulo3/metas/m1")
    assert r.status_code == 404
    assert repo.consultas == ["m1"]
