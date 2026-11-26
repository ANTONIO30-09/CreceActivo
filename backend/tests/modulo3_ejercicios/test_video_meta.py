"""Tests de metadatos de videos (Modulo 3) sin Mongo real."""
from __future__ import annotations
from uuid import UUID, uuid4
import pytest
from fastapi.testclient import TestClient

from app.core.security import verificar_firebase_token
from app.main import app
from app.modulo3_ejercicios.adapters.api.router import get_video_meta_repository
from app.modulo3_ejercicios.domain.archivo_video import GrupoEdad
from app.modulo3_ejercicios.ports.video_meta_port import VideoMetaDTO


def _dto(grupo: GrupoEdad, titulo: str = "T") -> VideoMetaDTO:
    return VideoMetaDTO(
        id=uuid4(), titulo=titulo, descripcion="d",
        grupo_edad=grupo, duracion_seg=180,
        dificultad="facil", materiales=("colchoneta",),
        recomendaciones_seguridad=("calentar",),
    )


class _FakeRepo:
    def __init__(self, metas):
        self._metas = list(metas)
    async def listar(self, grupo=None):
        if grupo is None:
            return list(self._metas)
        return [m for m in self._metas if m.grupo_edad == grupo]
    async def obtener(self, video_id):
        return next((m for m in self._metas if m.id == video_id), None)


def _user():
    return {"uid": "t1"}


@pytest.fixture
def client():
    app.dependency_overrides[verificar_firebase_token] = _user
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_listar_sin_filtro(client):
    metas = [_dto(GrupoEdad.INFANTIL), _dto(GrupoEdad.MAYOR)]
    app.dependency_overrides[get_video_meta_repository] = lambda: _FakeRepo(metas)
    r = client.get("/modulo3/videos")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_listar_por_grupo(client):
    metas = [_dto(GrupoEdad.INFANTIL), _dto(GrupoEdad.MAYOR)]
    app.dependency_overrides[get_video_meta_repository] = lambda: _FakeRepo(metas)
    r = client.get("/modulo3/videos?grupo_edad=6-8")
    assert r.status_code == 200
    assert [v["grupo_edad"] for v in r.json()] == ["6-8"]


def test_listar_grupo_invalido_422(client):
    app.dependency_overrides[get_video_meta_repository] = lambda: _FakeRepo([])
    r = client.get("/modulo3/videos?grupo_edad=99-100")
    assert r.status_code == 422


def test_obtener_existente(client):
    dto = _dto(GrupoEdad.INTERMEDIO)
    app.dependency_overrides[get_video_meta_repository] = lambda: _FakeRepo([dto])
    r = client.get(f"/modulo3/videos/{dto.id}")
    assert r.status_code == 200
    assert r.json()["id"] == str(dto.id)


def test_obtener_inexistente_404(client):
    app.dependency_overrides[get_video_meta_repository] = lambda: _FakeRepo([])
    r = client.get(f"/modulo3/videos/{uuid4()}")
    assert r.status_code == 404


def test_obtener_id_invalido_422(client):
    app.dependency_overrides[get_video_meta_repository] = lambda: _FakeRepo([])
    r = client.get("/modulo3/videos/no-es-uuid")
    assert r.status_code == 422
