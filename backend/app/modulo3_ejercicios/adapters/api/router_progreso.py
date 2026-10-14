"""Endpoints HTTP del Modulo 3: progreso, rachas, insignias y metas.

Complementa el router de storage de Kevin sin tocarlo.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db
from app.core.propiedad import exigir_perfil_del_tutor, get_perfil_port
from app.core.security import verificar_firebase_token
from app.modulo1_usuarios.ports import PerfilInfantilPort
from app.modulo3_ejercicios.adapters.api.schemas import (
    InsigniaResponse,
    MarcarMetaRequest,
    MetaCreateRequest,
    MetaResponse,
    ProgresoResponse,
    RegistroCreateRequest,
    RegistroResponse,
)
from app.modulo3_ejercicios.adapters.db.progreso_repository import (
    ProgresoRepository,
)

router = APIRouter(prefix="/modulo3", tags=["modulo3-progreso"])


def get_progreso_repository(
    db: Any = Depends(get_db),
) -> ProgresoRepository:
    """Dependencia: instancia el repositorio con la DB activa."""
    return ProgresoRepository(db)


# ---------------- Registros ----------------


@router.post(
    "/registros",
    response_model=RegistroResponse,
    status_code=status.HTTP_201_CREATED,
)
async def registrar_actividad(
    body: RegistroCreateRequest,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
    perfiles: PerfilInfantilPort = Depends(get_perfil_port),
) -> RegistroResponse:
    """Registra una actividad (rutina, agua, minutos) del dia."""
    await exigir_perfil_del_tutor(body.perfil_id, user, perfiles)
    registro = await repo.registrar_actividad(
        perfil_id=body.perfil_id,
        tutor_id=user["uid"],
        tipo=body.tipo,
        valor=body.valor,
    )
    return RegistroResponse.model_validate(registro)


@router.get(
    "/registros/{perfil_id}",
    response_model=list[RegistroResponse],
)
async def listar_registros(
    perfil_id: str,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
    perfiles: PerfilInfantilPort = Depends(get_perfil_port),
) -> list[RegistroResponse]:
    """Lista los registros de un perfil."""
    await exigir_perfil_del_tutor(perfil_id, user, perfiles)
    registros = await repo.listar_registros(perfil_id)
    return [RegistroResponse.model_validate(r) for r in registros]


# ---------------- Progreso ----------------


@router.get(
    "/progreso/{perfil_id}",
    response_model=ProgresoResponse,
)
async def obtener_progreso(
    perfil_id: str,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
    perfiles: PerfilInfantilPort = Depends(get_perfil_port),
) -> ProgresoResponse:
    """Devuelve racha actual, mejor racha, total e insignias del perfil."""
    await exigir_perfil_del_tutor(perfil_id, user, perfiles)
    progreso = await repo.obtener_progreso(perfil_id)
    return ProgresoResponse(
        perfil_id=progreso.perfil_id,
        racha_actual=progreso.racha_actual,
        mejor_racha=progreso.mejor_racha,
        total_registros=progreso.total_registros,
        insignias_ganadas=list(progreso.insignias_ganadas),
    )


@router.get(
    "/insignias/catalogo",
    response_model=list[InsigniaResponse],
)
async def catalogo_insignias(
    _user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
) -> list[InsigniaResponse]:
    """Devuelve el catalogo completo de insignias disponibles."""
    insignias = await repo.catalogo_insignias()
    return [
        InsigniaResponse(id=i.id, nombre=i.nombre, tipo=i.tipo, meta=i.meta)
        for i in insignias
    ]


# ---------------- Metas familiares ----------------


@router.post(
    "/metas",
    response_model=MetaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_meta(
    body: MetaCreateRequest,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
    perfiles: PerfilInfantilPort = Depends(get_perfil_port),
) -> MetaResponse:
    """Crea una meta familiar para un perfil."""
    await exigir_perfil_del_tutor(body.perfil_id, user, perfiles)
    meta = await repo.crear_meta(
        perfil_id=body.perfil_id,
        tutor_id=user["uid"],
        titulo=body.titulo,
        descripcion=body.descripcion,
        objetivo_semanal=body.objetivo_semanal,
    )
    return MetaResponse.model_validate(meta)


@router.get(
    "/metas/{perfil_id}",
    response_model=list[MetaResponse],
)
async def listar_metas(
    perfil_id: str,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
    perfiles: PerfilInfantilPort = Depends(get_perfil_port),
) -> list[MetaResponse]:
    """Lista las metas activas de un perfil con su avance semanal."""
    await exigir_perfil_del_tutor(perfil_id, user, perfiles)
    metas = await repo.listar_metas(perfil_id)
    return [MetaResponse.model_validate(m) for m in metas]


@router.post(
    "/metas/{meta_id}/marcar",
    response_model=MetaResponse,
)
async def marcar_meta(
    meta_id: str,
    body: MarcarMetaRequest,
    _user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
) -> MetaResponse:
    """Marca un dia cumplido para una meta. 404 si no existe o no esta activa."""
    meta = await repo.marcar_meta(meta_id, body.fecha)
    if meta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meta no encontrada o inactiva",
        )
    return MetaResponse.model_validate(meta)


@router.delete(
    "/metas/{meta_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def archivar_meta(
    meta_id: str,
    _user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: ProgresoRepository = Depends(get_progreso_repository),
) -> None:
    """Archiva (borrado logico) una meta. 404 si no existe."""
    ok = await repo.archivar_meta(meta_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meta no encontrada",
        )
