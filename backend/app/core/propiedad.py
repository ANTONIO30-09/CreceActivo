"""Comprobacion de que un perfil infantil pertenece al tutor autenticado.

Los modulos 2 y 3 la usan a traves de PerfilInfantilPort; nunca importan
el adaptador del Modulo 1 directamente.
"""
from __future__ import annotations

from typing import Any

from fastapi import Depends, HTTPException, status

from app.core.database import get_db
from app.modulo1_usuarios.adapters.db.perfil_repository import (
    PerfilInfantilRepository,
)
from app.modulo1_usuarios.ports import PerfilInfantilPort


def get_perfil_port(db: Any = Depends(get_db)) -> PerfilInfantilPort:
    return PerfilInfantilRepository(db)


async def exigir_perfil_del_tutor(
    perfil_id: str, user: dict[str, Any], perfiles: PerfilInfantilPort
) -> None:
    """404 si el perfil no existe, esta inactivo o es de otro tutor."""
    perfil = await perfiles.obtener_por_id(perfil_id)
    if perfil is None or perfil.tutor_id != user["uid"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado o no pertenece al tutor",
        )
