"""Configuracion del backend cargada desde variables de entorno.

Se usa pydantic-settings para validar y tipar al arrancar: si falta una
variable obligatoria, la app falla temprano con un mensaje claro en vez de
explotar a mitad de una peticion.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Configuracion tipada del backend.

    Lee de .env en local y de variables de entorno en Cloud Run.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = "development"
    app_name: str = "CreceActivo"
    app_version: str = "0.1.0"

    mongodb_uri: str = Field(..., description="URI de conexion a MongoDB Atlas")
    mongodb_db_name: str = "creceactivo"

    firebase_project_id: str = Field(...)
    firebase_service_account_path: str = Field(...)

    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    """Devuelve la configuracion cacheada (se lee una sola vez)."""
    return Settings()
