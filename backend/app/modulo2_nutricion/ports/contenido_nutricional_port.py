"""Contrato publico del Modulo 2 (Nutricion y orientacion profesional).

Este archivo es la UNICA superficie que los Modulos 1 y 3 pueden importar
de `modulo2_nutricion`. No deben importar `domain`, `adapters` ni `service`
directamente.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from .dto import EspecialistaDTO, GuiaDTO, MenuDTO, PlatoDTO, RangoEdad, TipoComida

__all__ = [
    "RangoEdad",
    "TipoComida",
    "GuiaDTO",
    "PlatoDTO",
    "MenuDTO",
    "EspecialistaDTO",
    "ContenidoNutricionalPort",
]


@runtime_checkable
class ContenidoNutricionalPort(Protocol):
    """Puerto que el Modulo 2 OFRECE a los Modulos 1 y 3.

    Semantica:
    - Guia o menu inexistente o inactivo -> None.
    - Sin resultados -> lista vacia.
    - No se lanzan excepciones de dominio en lectura.
    """

    async def listar_guias(
        self, rango_edad: RangoEdad | None = None
    ) -> list[GuiaDTO]:
        ...

    async def obtener_guia(self, guia_id: str) -> GuiaDTO | None:
        ...

    async def listar_menus(
        self,
        rango_edad: RangoEdad | None = None,
        tipo_comida: TipoComida | None = None,
    ) -> list[MenuDTO]:
        ...

    async def obtener_menu(self, menu_id: str) -> MenuDTO | None:
        ...

    async def listar_especialistas(self) -> list[EspecialistaDTO]:
        ...

    async def crear_solicitud_orientacion(
        self,
        tutor_id: str,
        perfil_id: str,
        especialista_id: str,
        mensaje: str,
    ) -> str:
        ...
