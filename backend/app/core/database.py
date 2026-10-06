"""Conexion a MongoDB Atlas usando motor (async).

El cliente se abre en el lifespan de FastAPI y se cierra al apagar.
Si la URI es invalida o la red no llega al cluster, falla al arrancar.
"""
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .config import get_settings

__all__ = ["conectar_mongodb", "cerrar_mongodb", "get_db"]


class _MongoState:
    """Estado global del cliente Mongo (uno por proceso)."""

    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


_state = _MongoState()


async def conectar_mongodb() -> None:
    """Abre el cliente y hace ping. Falla rapido si la URI no responde."""
    settings = get_settings()
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=5000,
    )
    await client.admin.command("ping")
    _state.client = client
    _state.db = client[settings.mongodb_db_name]


async def cerrar_mongodb() -> None:
    """Cierra el cliente si estaba abierto."""
    if _state.client is not None:
        _state.client.close()
        _state.client = None
        _state.db = None


def get_db() -> AsyncIOMotorDatabase:
    """Devuelve la base de datos activa o falla si no fue inicializada."""
    if _state.db is None:
        raise RuntimeError(
            "MongoDB no inicializado. Se esperaba que el lifespan lo abriera."
        )
    return _state.db
