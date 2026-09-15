"""Tests del endpoint publico de health."""
from __future__ import annotations


def test_health_responde_ok(client):
    response = client.get("/modulo1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "ok"
    assert "env" in data


def test_root_responde_info_servicio(client):
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == "CreceActivo backend"
    assert "version" in data
