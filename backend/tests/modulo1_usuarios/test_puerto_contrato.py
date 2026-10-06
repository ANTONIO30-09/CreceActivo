"""Tests del contrato publico del Modulo 1."""
from __future__ import annotations

import pytest

from app.modulo1_usuarios.domain.enums import (
    NivelActividadFisica as NivelActividadFisicaDomain,
)
from app.modulo1_usuarios.domain.enums import Sexo as SexoDomain
from app.modulo1_usuarios.domain.perfil_infantil import PerfilInfantil
from app.modulo1_usuarios.ports.perfil_infantil_port import (
    NivelActividadFisica,
    PerfilInfantilDTO,
    PerfilInfantilPort,
    Sexo,
)


def _dto_valido(perfil_id: str = "p-1", tutor_id: str = "t-1") -> PerfilInfantilDTO:
    return PerfilInfantilDTO(
        id=perfil_id,
        tutor_id=tutor_id,
        nombre="Ana",
        edad=10,
        sexo=Sexo.FEMENINO,
        peso_kg=32.5,
        estatura_cm=140.0,
        nivel_actividad_fisica=NivelActividadFisica.MODERADO,
        habitos_alimenticios=None,
        alergias=(),
        objetivos=None,
    )


def test_puerto_reexpone_enums_del_dominio():
    assert Sexo is SexoDomain
    assert NivelActividadFisica is NivelActividadFisicaDomain


def test_dto_no_expone_campos_internos():
    dto = _dto_valido()
    for campo_interno in ("activo", "creado_en", "actualizado_en"):
        assert not hasattr(dto, campo_interno), (
            f"El DTO no debe exponer el campo interno '{campo_interno}'"
        )


def test_desde_entidad_proyecta_campos_publicos():
    perfil = PerfilInfantil.crear(
        tutor_id="t-1",
        nombre="Ana",
        edad=10,
        sexo=Sexo.FEMENINO,
        peso_kg=32.5,
        estatura_cm=140.0,
        nivel_actividad_fisica=NivelActividadFisica.MODERADO,
        alergias=["mani"],
    )
    dto = PerfilInfantilDTO.desde_entidad(perfil)

    assert dto.id == perfil.id
    assert dto.tutor_id == perfil.tutor_id
    assert dto.nombre == perfil.nombre
    assert dto.alergias == ("mani",)


@pytest.mark.asyncio
async def test_consumidor_externo_usa_solo_el_puerto():
    """Un consumidor implementa el Protocol sin heredar ni tocar adapters."""

    class _AdapterEnMemoria:
        def __init__(self, perfiles: list[PerfilInfantilDTO]) -> None:
            self._perfiles = {p.id: p for p in perfiles}

        async def obtener_por_id(self, perfil_id: str) -> PerfilInfantilDTO | None:
            return self._perfiles.get(perfil_id)

        async def listar_por_tutor(self, tutor_id: str) -> list[PerfilInfantilDTO]:
            return [p for p in self._perfiles.values() if p.tutor_id == tutor_id]

        async def existe(self, perfil_id: str) -> bool:
            return perfil_id in self._perfiles

    adapter: PerfilInfantilPort = _AdapterEnMemoria([_dto_valido()])

    assert isinstance(adapter, PerfilInfantilPort)
    assert await adapter.existe("p-1") is True
    assert await adapter.existe("nope") is False

    perfil = await adapter.obtener_por_id("p-1")
    assert perfil is not None and perfil.nombre == "Ana"
    assert await adapter.obtener_por_id("nope") is None

    assert len(await adapter.listar_por_tutor("t-1")) == 1
    assert await adapter.listar_por_tutor("otro") == []
