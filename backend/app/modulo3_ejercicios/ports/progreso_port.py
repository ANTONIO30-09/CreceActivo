"""Contrato publico del Modulo 3 para progreso y motivacion.

Este puerto lo consumen el API del propio modulo y, si hiciera falta,
otros modulos. No expone adapters ni domain.
"""
from __future__ import annotations

from datetime import date
from typing import Protocol, runtime_checkable

from .dto import InsigniaDTO, MetaDTO, ProgresoDTO, RegistroDTO, TipoActividad

__all__ = [
    "TipoActividad",
    "RegistroDTO",
    "MetaDTO",
    "ProgresoDTO",
    "InsigniaDTO",
    "ProgresoPort",
]


@runtime_checkable
class ProgresoPort(Protocol):
    """Puerto que el Modulo 3 OFRECE.

    Semantica:
    - Registro o meta inexistente -> None.
    - Sin resultados -> lista vacia.
    - No se lanzan excepciones de dominio en lectura.
    """

    async def registrar_actividad(
        self,
        perfil_id: str,
        tutor_id: str,
        tipo: TipoActividad,
        valor: int,
    ) -> RegistroDTO:
        ...

    async def listar_registros(
        self, perfil_id: str
    ) -> list[RegistroDTO]:
        ...

    async def crear_meta(
        self,
        perfil_id: str,
        tutor_id: str,
        titulo: str,
        descripcion: str,
        objetivo_semanal: int,
    ) -> MetaDTO:
        ...

    async def listar_metas(self, perfil_id: str) -> list[MetaDTO]:
        ...

    async def marcar_meta(
        self, meta_id: str, fecha: date
    ) -> MetaDTO | None:
        ...

    async def archivar_meta(self, meta_id: str) -> bool:
        ...

    async def obtener_progreso(self, perfil_id: str) -> ProgresoDTO:
        ...
