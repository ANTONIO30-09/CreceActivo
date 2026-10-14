"""Punto de entrada del backend de CreceActivo (Modulos 1, 2 y 3).

Arranque:
    cd backend
    uvicorn app.main:app --reload

Al levantar, el lifespan:
1. Inicializa Firebase Admin (falla si el service account no existe).
2. Abre el cliente de MongoDB Atlas y hace ping (falla si la URI no responde).
3. Asegura el validador y el indice de perfiles_infantiles.
4. Asegura los validadores e indices de las colecciones del Modulo 2.
5. Asegura los validadores e indices de las colecciones del Modulo 3.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import cerrar_mongodb, conectar_mongodb, get_db
from app.core.security import inicializar_firebase
from app.modulo1_usuarios.adapters.api.router import router as modulo1_router
from app.modulo2_nutricion.adapters.api.router import router as modulo2_router
from app.modulo1_usuarios.adapters.db import asegurar_perfiles_infantiles
from app.modulo2_nutricion.adapters.db import asegurar_colecciones_modulo2
from app.modulo3_ejercicios.adapters.db import asegurar_colecciones_modulo3
from app.modulo3_ejercicios.adapters.api.router import router as modulo3_router
from app.modulo3_ejercicios.adapters.api.router_progreso import (
    router as modulo3_progreso_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Recursos compartidos durante la vida de la app."""
    inicializar_firebase()
    await conectar_mongodb()
    await asegurar_perfiles_infantiles(get_db())
    await asegurar_colecciones_modulo2(get_db())
    await asegurar_colecciones_modulo3(get_db())
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
app.include_router(modulo2_router)
app.include_router(modulo3_router)
app.include_router(modulo3_progreso_router)


@app.get("/")
async def root() -> dict[str, str]:
    """Info basica del servicio."""
    return {"service": "CreceActivo backend", "version": settings.app_version}
