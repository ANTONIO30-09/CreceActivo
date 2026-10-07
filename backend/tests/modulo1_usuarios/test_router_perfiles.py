from fastapi.testclient import TestClient

from app.main import app
from app.core.security import verificar_firebase_token
from app.modulo1_usuarios.adapters.api.router import get_perfil_repository
from app.modulo1_usuarios.domain.enums import NivelActividadFisica, Sexo
from app.modulo1_usuarios.domain.perfil_infantil import PerfilInfantil
from app.modulo1_usuarios.ports import PerfilInfantilDTO


class RepoFalso:
    def __init__(self, entidad):
        self.entidad = entidad

    async def obtener_por_id(self, perfil_id):
        if perfil_id != self.entidad.id:
            return None
        return PerfilInfantilDTO.desde_entidad(self.entidad)

    async def obtener_entidad(self, perfil_id):
        return self.entidad if perfil_id == self.entidad.id else None

    async def actualizar(self, perfil):
        self.entidad = perfil


def _entidad(tutor_id="tutor-1"):
    return PerfilInfantil.crear(
        tutor_id=tutor_id, nombre="Ana", edad=8, sexo=list(Sexo)[0],
        peso_kg=30, estatura_cm=130,
        nivel_actividad_fisica=list(NivelActividadFisica)[0],
        habitos_alimenticios=None, alergias=(), objetivos=None,
    )


def _cliente(repo, uid):
    app.dependency_overrides[verificar_firebase_token] = lambda: {"uid": uid}
    app.dependency_overrides[get_perfil_repository] = lambda: repo
    return TestClient(app)  # sin "with": no corre el arranque de Firebase


def test_patch_actualiza_nombre_sin_error_500():
    entidad = _entidad()
    repo = RepoFalso(entidad)
    try:
        r = _cliente(repo, "tutor-1").patch(
            f"/modulo1/perfiles/{entidad.id}", json={"nombre": "Ana Maria"}
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    assert r.json()["nombre"] == "Ana Maria"


def test_patch_de_otro_tutor_devuelve_404():
    entidad = _entidad(tutor_id="tutor-1")
    repo = RepoFalso(entidad)
    try:
        r = _cliente(repo, "otro-tutor").patch(
            f"/modulo1/perfiles/{entidad.id}", json={"nombre": "Hackeado"}
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 404
    assert repo.entidad.nombre == "Ana"


def test_post_con_alergia_vacia_devuelve_422():
    repo = RepoFalso(_entidad())
    try:
        r = _cliente(repo, "tutor-1").post(
            "/modulo1/perfiles",
            json={
                "nombre": "Ana", "edad": 8, "sexo": list(Sexo)[0].value,
                "peso_kg": 30, "estatura_cm": 130,
                "nivel_actividad_fisica": list(NivelActividadFisica)[0].value,
                "alergias": [""],
            },
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 422
