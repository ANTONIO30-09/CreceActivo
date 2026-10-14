"""Routers HTTP del Modulo 2 (Nutricion y orientacion profesional).

Endpoints publicos: guias, menus, especialistas, health.
Endpoints protegidos: POST /modulo2/solicitudes (Bearer Firebase).
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import verificar_firebase_token
from app.modulo2_nutricion.adapters.api.schemas import (
    EspecialistaResponse,
    GuiaResponse,
    MenuResponse,
    SolicitudCreateRequest,
    SolicitudResponse,
)
from app.modulo2_nutricion.adapters.db.nutricion_repository import (
    NutricionRepository,
)
from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida

router = APIRouter(prefix="/modulo2", tags=["modulo2"])


def get_nutricion_repository(db: Any = Depends(get_db)) -> NutricionRepository:
    """Dependencia: instancia el repositorio con la DB activa."""
    return NutricionRepository(db)


# ---------------- Health ----------------


@router.get("/health")
async def health() -> dict[str, str]:
    """Health publico del Modulo 2: estado de la app y de Mongo."""
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


# ---------------- Guias ----------------


@router.get("/guias", response_model=list[GuiaResponse])
async def listar_guias(
    rango_edad: RangoEdad | None = None,
    repo: NutricionRepository = Depends(get_nutricion_repository),
) -> list[GuiaResponse]:
    """Lista guias nutricionales. Filtro opcional por rango de edad."""
    guias = await repo.listar_guias(rango_edad=rango_edad)
    return [GuiaResponse.model_validate(g) for g in guias]


@router.get("/guias/{guia_id}", response_model=GuiaResponse)
async def obtener_guia(
    guia_id: str,
    repo: NutricionRepository = Depends(get_nutricion_repository),
) -> GuiaResponse:
    """Devuelve una guia por id. 404 si no existe o esta inactiva."""
    guia = await repo.obtener_guia(guia_id)
    if guia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guia no encontrada",
        )
    return GuiaResponse.model_validate(guia)


# ---------------- Menus ----------------


@router.get("/menus", response_model=list[MenuResponse])
async def listar_menus(
    rango_edad: RangoEdad | None = None,
    tipo_comida: TipoComida | None = None,
    repo: NutricionRepository = Depends(get_nutricion_repository),
) -> list[MenuResponse]:
    """Lista menus infantiles. Filtros opcionales por rango y tipo de comida."""
    menus = await repo.listar_menus(
        rango_edad=rango_edad,
        tipo_comida=tipo_comida,
    )
    return [MenuResponse.model_validate(m) for m in menus]


@router.get("/menus/{menu_id}", response_model=MenuResponse)
async def obtener_menu(
    menu_id: str,
    repo: NutricionRepository = Depends(get_nutricion_repository),
) -> MenuResponse:
    """Devuelve un menu por id. 404 si no existe o esta inactivo."""
    menu = await repo.obtener_menu(menu_id)
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu no encontrado",
        )
    return MenuResponse.model_validate(menu)


# ---------------- Especialistas ----------------


@router.get("/especialistas", response_model=list[EspecialistaResponse])
async def listar_especialistas(
    repo: NutricionRepository = Depends(get_nutricion_repository),
) -> list[EspecialistaResponse]:
    """Lista especialistas disponibles (nutricionistas, pediatras, entrenadores)."""
    especialistas = await repo.listar_especialistas()
    return [EspecialistaResponse.model_validate(e) for e in especialistas]


# ---------------- Solicitudes (protegido) ----------------


@router.post(
    "/solicitudes",
    response_model=SolicitudResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_solicitud(
    body: SolicitudCreateRequest,
    user: dict[str, Any] = Depends(verificar_firebase_token),
    repo: NutricionRepository = Depends(get_nutricion_repository),
) -> SolicitudResponse:
    """Crea una solicitud de orientacion a un especialista.

    Requiere Bearer Firebase. El tutor_id se toma del token.
    """
    solicitud_id = await repo.crear_solicitud_orientacion(
        tutor_id=user["uid"],
        perfil_id=body.perfil_id,
        especialista_id=body.especialista_id,
        mensaje=body.mensaje,
    )
    return SolicitudResponse(id=solicitud_id, estado="pendiente")
