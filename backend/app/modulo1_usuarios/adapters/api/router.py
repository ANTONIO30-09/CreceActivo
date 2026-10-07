"""Routers HTTP del Modulo 1.

Fase 2: solo health + whoami (verificacion de arranque y de auth).
Fase 3: aqui viviran los endpoints CRUD de PerfilInfantil.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import verificar_firebase_token
from app.modulo1_usuarios.domain.perfil_infantil import (
    PerfilInfantil,
    PerfilInfantilInvalido,
)
from app.modulo1_usuarios.adapters.db.perfil_repository import PerfilInfantilRepository
from app.modulo1_usuarios.adapters.api.schemas import (
    PerfilInfantilCreateSchema,
    PerfilInfantilUpdateSchema,
    PerfilInfantilResponseSchema,
)

router = APIRouter(prefix="/modulo1", tags=["modulo1"])

def get_perfil_repository(db: Any = Depends(get_db)) -> PerfilInfantilRepository:
    return PerfilInfantilRepository(db)


@router.get("/health")
async def health() -> dict[str, str]:
    """Health publico: estado de la app y de la conexion a Mongo."""
    settings = get_settings()
    db_status = "ok"
    try:
        db = get_db()
        await db.command("ping")
    except Exception:  # noqa: BLE001
        db_status = "error"

    return {
        "status": "ok",
        "env": settings.app_env,
        "db": db_status,
    }


@router.get("/whoami")
async def whoami(
    user: dict[str, Any] = Depends(verificar_firebase_token),
) -> dict[str, Any]:
    """Endpoint protegido: devuelve el uid/email del token Bearer."""
    return {"uid": user["uid"], "email": user.get("email")}


# ---------------- CRUD PERFILES INFANTILES ----------------

@router.post(
    "/perfiles",
    response_model=PerfilInfantilResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def crear_perfil(
    payload: PerfilInfantilCreateSchema,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: PerfilInfantilRepository = Depends(get_perfil_repository),
) -> Any:
    tutor_id = user["uid"]
    
    try:
        perfil = PerfilInfantil.crear(
            tutor_id=tutor_id,
            nombre=payload.nombre,
            edad=payload.edad,
            sexo=payload.sexo,
            peso_kg=payload.peso_kg,
            estatura_cm=payload.estatura_cm,
            nivel_actividad_fisica=payload.nivel_actividad_fisica,
            habitos_alimenticios=payload.habitos_alimenticios,
            alergias=payload.alergias,
            objetivos=payload.objetivos,
        )
    except PerfilInfantilInvalido as exc:
        raise HTTPException(
            status_code=422, detail=str(exc)
        ) from exc
    
    await repo.insertar(perfil)
    return await repo.obtener_por_id(perfil.id)


@router.get(
    "/perfiles",
    response_model=list[PerfilInfantilResponseSchema],
)
async def listar_perfiles(
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: PerfilInfantilRepository = Depends(get_perfil_repository),
) -> Any:
    tutor_id = user["uid"]
    return await repo.listar_por_tutor(tutor_id)


@router.get(
    "/perfiles/{perfil_id}",
    response_model=PerfilInfantilResponseSchema,
)
async def obtener_perfil(
    perfil_id: str,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: PerfilInfantilRepository = Depends(get_perfil_repository),
) -> Any:
    tutor_id = user["uid"]
    perfil = await repo.obtener_por_id(perfil_id)
    
    if not perfil or perfil.tutor_id != tutor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado o no pertenece al tutor",
        )
    return perfil


@router.patch(
    "/perfiles/{perfil_id}",
    response_model=PerfilInfantilResponseSchema,
)
async def actualizar_perfil(
    perfil_id: str,
    payload: PerfilInfantilUpdateSchema,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: PerfilInfantilRepository = Depends(get_perfil_repository),
) -> Any:
    tutor_id = user["uid"]
    entidad = await repo.obtener_entidad(perfil_id)

    if entidad is None or entidad.tutor_id != tutor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado o no pertenece al tutor",
        )

    datos = payload.model_dump(exclude_unset=True)
    if datos.get("alergias") is not None:
        datos["alergias"] = tuple(datos["alergias"])

    try:
        actualizado = replace(
            entidad, **datos, actualizado_en=datetime.now(timezone.utc)
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422, detail=str(exc)
        ) from exc

    await repo.actualizar(actualizado)
    return await repo.obtener_por_id(perfil_id)


@router.delete(
    "/perfiles/{perfil_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def desactivar_perfil(
    perfil_id: str,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: PerfilInfantilRepository = Depends(get_perfil_repository),
) -> None:
    tutor_id = user["uid"]
    perfil_dto = await repo.obtener_por_id(perfil_id)
    
    if not perfil_dto or perfil_dto.tutor_id != tutor_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado o no pertenece al tutor",
        )
        
    await repo.desactivar(perfil_id)