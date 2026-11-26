"""Tests del chatbot nutricional (Modulo 2) sin tocar Gemini real."""
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient

from app.core.security import verificar_firebase_token
from app.main import app
from app.modulo2_nutricion.adapters.api.router import (
    get_chatbot_port, get_nutricion_repository,
)
from app.modulo2_nutricion.ports.chatbot_port import DERIVAR


class _FakeRepo:
    def __init__(self, guias=None, menus=None):
        self._guias = guias or []
        self._menus = menus or []
    async def listar_guias(self, rango_edad=None):
        return list(self._guias)
    async def listar_menus(self, rango_edad=None, tipo_comida=None):
        return list(self._menus)


class _FakeBot:
    def __init__(self, respuesta: str = "ok"):
        self.respuesta = respuesta
        self.ultimo_contexto: str | None = None
        self.ultima_pregunta: str | None = None
    async def responder(self, pregunta: str, contexto: str) -> str:
        self.ultima_pregunta = pregunta
        self.ultimo_contexto = contexto
        return self.respuesta


def _fake_user():
    return {"uid": "t1", "email": "x@y.z"}


@pytest.fixture
def client():
    app.dependency_overrides[verificar_firebase_token] = _fake_user
    app.dependency_overrides[get_nutricion_repository] = lambda: _FakeRepo()
    yield TestClient(app)
    app.dependency_overrides.clear()


def _override_chatbot(bot):
    app.dependency_overrides[get_chatbot_port] = lambda: bot


def test_chat_503_si_no_hay_api_key(client, monkeypatch):
    from app.core.config import get_settings
    monkeypatch.setenv("GEMINI_API_KEY", "")
    get_settings.cache_clear()
    # No overrideamos get_chatbot_port: debe saltar el 503 real
    r = client.post("/modulo2/chat", json={"pregunta": "hola"})
    assert r.status_code == 503
    get_settings.cache_clear()


def test_chat_deriva_pregunta_medica(client):
    bot = _FakeBot(respuesta=DERIVAR)
    _override_chatbot(bot)
    r = client.post("/modulo2/chat", json={"pregunta": "Mi hijo tiene fiebre"})
    assert r.status_code == 200
    assert r.json()["respuesta"] == DERIVAR


def test_chat_usa_contexto_de_guias_y_menus(client):
    class G:
        titulo = "Frutas"; contenido = "Come frutas"; habitos_clave = ("5 al dia",)
    class P:
        nombre = "Ensalada"; descripcion = "Verde"
    class M:
        titulo = "Comida"
        class tipo_comida: value = "almuerzo"
        platos = (P(),); recomendaciones = ("Poca sal",)
    app.dependency_overrides[get_nutricion_repository] = (
        lambda: _FakeRepo(guias=[G()], menus=[M()])
    )
    bot = _FakeBot(respuesta="Come 5 frutas")
    _override_chatbot(bot)
    r = client.post("/modulo2/chat", json={"pregunta": "Que meriendo?"})
    assert r.status_code == 200
    assert r.json()["respuesta"] == "Come 5 frutas"
    assert bot.ultimo_contexto and "Frutas" in bot.ultimo_contexto
    assert "Ensalada" in bot.ultimo_contexto


def test_chat_requiere_pregunta(client):
    _override_chatbot(_FakeBot())
    r = client.post("/modulo2/chat", json={"pregunta": ""})
    assert r.status_code == 422
