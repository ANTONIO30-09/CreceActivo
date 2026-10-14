from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.core.propiedad import get_perfil_port
from app.core.security import verificar_firebase_token
from app.main import app
from app.modulo3_ejercicios.adapters.api.router_progreso import (
    get_progreso_repository,
)


class PuertoPerfilesFalso:
    """Simula el Modulo 1: el perfil p-ajeno es del tutor-A."""

    def __init__(self):
        self.consultas = []

    async def obtener_por_id(self, perfil_id):
        self.consultas.append(perfil_id)
        if perfil_id == "p-ajeno":
            return SimpleNamespace(id=perfil_id, tutor_id="tutor-A")
        return None


class RepoProhibido:
    def __getattr__(self, nombre):
        raise AssertionError(f"El repositorio no debia usarse: {nombre}")


@pytest.mark.parametrize(
    "ruta",
    [
        "/modulo3/registros/p-ajeno",
        "/modulo3/progreso/p-ajeno",
        "/modulo3/metas/p-ajeno",
    ],
)
def test_tutor_no_puede_leer_datos_de_perfil_ajeno(ruta):
    puerto = PuertoPerfilesFalso()
    app.dependency_overrides[verificar_firebase_token] = lambda: {"uid": "tutor-B"}
    app.dependency_overrides[get_perfil_port] = lambda: puerto
    app.dependency_overrides[get_progreso_repository] = lambda: RepoProhibido()
    try:
        r = TestClient(app).get(ruta)
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 404
    assert puerto.consultas == ["p-ajeno"]  # el 404 vino de la comprobacion
