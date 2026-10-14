"""Tests del router del Modulo 2 con repositorio falso. Sin Mongo ni Firebase."""
from __future__ import annotations

from fastapi.testclient import TestClient

from types import SimpleNamespace

from app.core.propiedad import get_perfil_port
from app.core.security import verificar_firebase_token
from app.main import app
from app.modulo2_nutricion.adapters.api.router import get_nutricion_repository
from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida
from app.modulo2_nutricion.ports import (
    EspecialistaDTO,
    GuiaDTO,
    MenuDTO,
    PlatoDTO,
)


class RepoFalso:
    """Implementa ContenidoNutricionalPort en memoria para tests."""

    def __init__(
        self,
        guias: list[GuiaDTO] | None = None,
        menus: list[MenuDTO] | None = None,
        especialistas: list[EspecialistaDTO] | None = None,
    ) -> None:
        self.guias = guias or []
        self.menus = menus or []
        self.especialistas = especialistas or []
        self.solicitudes_creadas: list[dict] = []

    async def listar_guias(self, rango_edad=None):
        if rango_edad is None:
            return list(self.guias)
        return [g for g in self.guias if g.rango_edad == rango_edad]

    async def obtener_guia(self, guia_id):
        for g in self.guias:
            if g.id == guia_id:
                return g
        return None

    async def listar_menus(self, rango_edad=None, tipo_comida=None):
        resultado = list(self.menus)
        if rango_edad is not None:
            resultado = [m for m in resultado if m.rango_edad == rango_edad]
        if tipo_comida is not None:
            resultado = [m for m in resultado if m.tipo_comida == tipo_comida]
        return resultado

    async def obtener_menu(self, menu_id):
        for m in self.menus:
            if m.id == menu_id:
                return m
        return None

    async def listar_especialistas(self):
        return list(self.especialistas)

    async def crear_solicitud_orientacion(
        self, tutor_id, perfil_id, especialista_id, mensaje
    ):
        solicitud_id = f"sol-{len(self.solicitudes_creadas) + 1}"
        self.solicitudes_creadas.append(
            {
                "id": solicitud_id,
                "tutor_id": tutor_id,
                "perfil_id": perfil_id,
                "especialista_id": especialista_id,
                "mensaje": mensaje,
            }
        )
        return solicitud_id


def _guia(gid: str, rango: RangoEdad, titulo: str = "Guia") -> GuiaDTO:
    return GuiaDTO(
        id=gid,
        titulo=titulo,
        categoria="Habitos",
        rango_edad=rango,
        contenido="Contenido de prueba",
        habitos_clave=("Habito 1",),
    )


def _plato() -> PlatoDTO:
    return PlatoDTO(
        nombre="Avena",
        descripcion="Avena con leche",
        calorias_aprox=250,
        ingredientes=("Avena", "Leche"),
    )


def _menu(mid: str, rango: RangoEdad, tipo: TipoComida) -> MenuDTO:
    return MenuDTO(
        id=mid,
        titulo="Menu de prueba",
        rango_edad=rango,
        tipo_comida=tipo,
        platos=(_plato(),),
        recomendaciones=("Comer despacio",),
    )


def _especialista(eid: str, rol: str = "Nutricionista") -> EspecialistaDTO:
    return EspecialistaDTO(
        id=eid,
        nombre_completo="Dra. Prueba",
        rol=rol,
        especialidad="Nutricion Infantil",
        experiencia_anios=5,
        biografia="Biografia de prueba",
        contacto_email="test@example.com",
        disponible=True,
    )


class _PerfilesFalso:
    """Simula el Modulo 1: todo perfil consultado pertenece a `uid`."""

    def __init__(self, uid: str) -> None:
        self.uid = uid

    async def obtener_por_id(self, perfil_id):
        return SimpleNamespace(id=perfil_id, tutor_id=self.uid)


def _cliente(repo: RepoFalso, uid: str = "tutor-1") -> TestClient:
    """Cliente con repo y auth mockeados (sin lifespan de Firebase)."""
    app.dependency_overrides[verificar_firebase_token] = lambda: {"uid": uid}
    app.dependency_overrides[get_nutricion_repository] = lambda: repo
    app.dependency_overrides[get_perfil_port] = lambda: _PerfilesFalso(uid)
    return TestClient(app)


# ---------- GUIAS ----------


def test_listar_guias_vacio():
    repo = RepoFalso()
    try:
        r = _cliente(repo).get("/modulo2/guias")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    assert r.json() == []


def test_listar_guias_devuelve_las_del_repo():
    repo = RepoFalso(
        guias=[
            _guia("g1", RangoEdad.DE_6_A_8, "Guia A"),
            _guia("g2", RangoEdad.DE_9_A_11, "Guia B"),
        ]
    )
    try:
        r = _cliente(repo).get("/modulo2/guias")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert data[0]["titulo"] == "Guia A"


def test_listar_guias_filtro_rango_edad():
    repo = RepoFalso(
        guias=[
            _guia("g1", RangoEdad.DE_6_A_8),
            _guia("g2", RangoEdad.DE_9_A_11),
        ]
    )
    try:
        r = _cliente(repo).get(
            "/modulo2/guias", params={"rango_edad": RangoEdad.DE_6_A_8.value}
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_obtener_guia_existente():
    repo = RepoFalso(guias=[_guia("g1", RangoEdad.DE_6_A_8, "Encontrada")])
    try:
        r = _cliente(repo).get("/modulo2/guias/g1")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    assert r.json()["titulo"] == "Encontrada"


def test_obtener_guia_inexistente_404():
    repo = RepoFalso()
    try:
        r = _cliente(repo).get("/modulo2/guias/no-existe")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 404


# ---------- MENUS ----------


def test_listar_menus_devuelve_los_del_repo():
    repo = RepoFalso(
        menus=[
            _menu("m1", RangoEdad.DE_6_A_8, TipoComida.DESAYUNO),
            _menu("m2", RangoEdad.DE_9_A_11, TipoComida.ALMUERZO),
        ]
    )
    try:
        r = _cliente(repo).get("/modulo2/menus")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_listar_menus_filtro_tipo_comida():
    repo = RepoFalso(
        menus=[
            _menu("m1", RangoEdad.DE_6_A_8, TipoComida.DESAYUNO),
            _menu("m2", RangoEdad.DE_6_A_8, TipoComida.ALMUERZO),
        ]
    )
    try:
        r = _cliente(repo).get(
            "/modulo2/menus", params={"tipo_comida": TipoComida.DESAYUNO.value}
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_obtener_menu_inexistente_404():
    repo = RepoFalso()
    try:
        r = _cliente(repo).get("/modulo2/menus/no-existe")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 404


# ---------- ESPECIALISTAS ----------


def test_listar_especialistas_devuelve_los_del_repo():
    repo = RepoFalso(
        especialistas=[
            _especialista("e1", "Nutricionista"),
            _especialista("e2", "Pediatra"),
        ]
    )
    try:
        r = _cliente(repo).get("/modulo2/especialistas")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert data[0]["rol"] == "Nutricionista"


def test_listar_especialistas_vacio():
    repo = RepoFalso()
    try:
        r = _cliente(repo).get("/modulo2/especialistas")
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 200
    assert r.json() == []


# ---------- SOLICITUDES (protegidas) ----------


def test_solicitud_sin_token_devuelve_401():
    repo = RepoFalso()
    app.dependency_overrides[get_nutricion_repository] = lambda: repo
    try:
        r = TestClient(app).post(
            "/modulo2/solicitudes",
            json={
                "perfil_id": "p1",
                "especialista_id": "e1",
                "mensaje": "Necesito orientacion",
            },
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 401


def test_solicitud_con_token_crea_y_devuelve_201():
    repo = RepoFalso()
    try:
        r = _cliente(repo, uid="tutor-99").post(
            "/modulo2/solicitudes",
            json={
                "perfil_id": "p1",
                "especialista_id": "e1",
                "mensaje": "Consulta de prueba",
            },
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 201
    data = r.json()
    assert data["estado"] == "pendiente"
    assert data["id"].startswith("sol-")
    # Verificar que el repo guardo los datos correctos
    assert len(repo.solicitudes_creadas) == 1
    assert repo.solicitudes_creadas[0]["tutor_id"] == "tutor-99"


def test_solicitud_mensaje_vacio_devuelve_422():
    repo = RepoFalso()
    try:
        r = _cliente(repo).post(
            "/modulo2/solicitudes",
            json={"perfil_id": "p1", "especialista_id": "e1", "mensaje": ""},
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 422


def test_solicitud_sin_perfil_id_devuelve_422():
    repo = RepoFalso()
    try:
        r = _cliente(repo).post(
            "/modulo2/solicitudes",
            json={"especialista_id": "e1", "mensaje": "Hola"},
        )
    finally:
        app.dependency_overrides.clear()
    assert r.status_code == 422


# ---------- HEALTH ----------


def test_health_modulo2_responde_ok():
    r = TestClient(app).get("/modulo2/health")
    # En tests, get_db lanza RuntimeError -> db: "error". Pero status debe ser 200.
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "env" in data
    assert "db" in data
