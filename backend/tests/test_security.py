"""Tests del endpoint protegido /modulo1/whoami."""
from __future__ import annotations

from unittest.mock import patch


def test_whoami_sin_token_devuelve_401(client):
    response = client.get("/modulo1/whoami")
    assert response.status_code == 401


def test_whoami_con_token_invalido_devuelve_401(client):
    with patch(
        "app.core.security.firebase_auth.verify_id_token",
        side_effect=Exception("invalido"),
    ):
        response = client.get(
            "/modulo1/whoami",
            headers={"Authorization": "Bearer tokenfalso"},
        )
    assert response.status_code == 401


def test_whoami_con_token_valido_devuelve_uid_y_email(client):
    with patch(
        "app.core.security.firebase_auth.verify_id_token",
        return_value={"uid": "u1", "email": "test@example.com"},
    ):
        response = client.get(
            "/modulo1/whoami",
            headers={"Authorization": "Bearer tokening"},
        )
    assert response.status_code == 200

    data = response.json()
    assert data["uid"] == "u1"
    assert data["email"] == "test@example.com"
