"""Configuracion del backend cargada desde variables de entorno.

Se usa pydantic-settings para validar y tipar al arrancar: si falta una
variable obligatoria, la app falla temprano con un mensaje claro en vez de
explotar a mitad de una peticion.

El .env se busca en la RAIZ del monorepo (junto a README.md y .gitignore),
no relativo al directorio donde se ejecute uvicorn. Esto funciona igual
desde backend/ o desde la raiz, y no afecta a Cloud Run porque ahi las
variables vienen del entorno del contenedor.

Los origenes de CORS se declaran como string separado por comas para
evitar los problemas de parseo de listas (JSON) en el .env:

    CORS_ORIGINS=http://localhost:5173,http://localhost:3000
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "get_settings"]

# backend/app/core/config.py -> parents[3] es la raiz del repo
_REPO_ROOT = Path(__file__).resolve().parents[3]
_ENV_FILE = _REPO_ROOT / ".env"


class Settings(BaseSettings):
    """Configuracion tipada del backend."""

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
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

    # String separado por comas. Ver `cors_origins_list`.
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        """Devuelve la lista de origenes limpia."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Devuelve la configuracion cacheada (se lee una sola vez)."""
    return Settings()
