"""Punto de entrada del backend de CreceActivo (Modulo 1).

Arranque:
    cd backend
    uvicorn app.main:app --reload

Al levantar, el lifespan:
1. Inicializa Firebase Admin (falla si el service account no existe).
2. Abre el cliente de MongoDB Atlas y hace ping (falla si la URI no responde).
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import cerrar_mongodb, conectar_mongodb
from app.core.security import inicializar_firebase
from app.modulo1_usuarios.adapters.api.router import router as modulo1_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Recursos compartidos durante la vida de la app."""
    inicializar_firebase()
    await conectar_mongodb()
    try:
        yield
    finally:
        await cerrar_mongodb()


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(modulo1_router)


@app.get("/")
async def root() -> dict[str, str]:
    """Info basica del servicio."""
    return {"service": "CreceActivo backend", "version": settings.app_version}
