"""Tests unitarios de la entidad PerfilInfantil (dominio puro)."""
from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from app.modulo1_usuarios.domain.enums import NivelActividadFisica, Sexo
from app.modulo1_usuarios.domain.perfil_infantil import (
    EDAD_MAXIMA,
    EDAD_MINIMA,
    NOMBRE_MAX_LEN,
    PerfilInfantil,
    PerfilInfantilInvalido,
)


def _kwargs_validos(**overrides):
    base = dict(
        tutor_id="tutor-123",
        nombre="Ana",
        edad=10,
        sexo=Sexo.FEMENINO,
        peso_kg=32.5,
        estatura_cm=140.0,
        nivel_actividad_fisica=NivelActividadFisica.MODERADO,
    )
    base.update(overrides)
    return base


def test_crear_perfil_valido():
    perfil = PerfilInfantil.crear(**_kwargs_validos())

    assert perfil.id
    assert perfil.nombre == "Ana"
    assert perfil.edad == 10
    assert perfil.activo is True
    assert perfil.alergias == ()
    assert perfil.habitos_alimenticios is None
    assert perfil.objetivos is None
    assert isinstance(perfil.creado_en, datetime)
    assert perfil.creado_en == perfil.actualizado_en
    assert perfil.creado_en.tzinfo is not None


def test_nombre_se_normaliza():
    perfil = PerfilInfantil.crear(**_kwargs_validos(nombre="   Ana   "))
    assert perfil.nombre == "Ana"


@pytest.mark.parametrize("edad", [EDAD_MINIMA - 1, EDAD_MAXIMA + 1, 0, -3])
def test_edad_fuera_de_rango(edad):
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(edad=edad))


def test_edad_no_entera():
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(edad="10"))


def test_nombre_vacio():
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(nombre="   "))


def test_nombre_muy_largo():
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(nombre="a" * (NOMBRE_MAX_LEN + 1)))


@pytest.mark.parametrize("peso", [0, -1, 201, "32.5"])
def test_peso_invalido(peso):
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(peso_kg=peso))


@pytest.mark.parametrize("estatura", [0, -10, 300, "140"])
def test_estatura_invalida(estatura):
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(estatura_cm=estatura))


def test_sexo_invalido():
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(sexo="femenino"))


def test_nivel_actividad_invalido():
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(nivel_actividad_fisica="moderado"))


def test_alergias_se_normalizan_y_son_tupla():
    perfil = PerfilInfantil.crear(
        **_kwargs_validos(alergias=["  mani ", "lactosa"])
    )
    assert perfil.alergias == ("mani", "lactosa")
    assert isinstance(perfil.alergias, tuple)


def test_alergia_vacia_falla():
    with pytest.raises(PerfilInfantilInvalido):
        PerfilInfantil.crear(**_kwargs_validos(alergias=[""]))


def test_habitos_vacios_se_convierten_en_none():
    perfil = PerfilInfantil.crear(**_kwargs_validos(habitos_alimenticios="   "))
    assert perfil.habitos_alimenticios is None


def test_entidad_es_inmutable():
    perfil = PerfilInfantil.crear(**_kwargs_validos())
    with pytest.raises(FrozenInstanceError):
        perfil.nombre = "Otra"
