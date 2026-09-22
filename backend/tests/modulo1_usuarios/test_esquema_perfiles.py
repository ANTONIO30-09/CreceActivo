"""Tests del esquema Mongo de perfiles_infantiles. No requieren Atlas."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.modulo1_usuarios.adapters.db.perfiles_infantiles import (
    COLLECTION_NAME,
    INDEX_NAME,
    INDICE_TUTOR_ACTIVO,
    VALIDATION_ACTION,
    VALIDATION_LEVEL,
    asegurar_perfiles_infantiles,
    validador_perfiles_infantiles,
)
from app.modulo1_usuarios.domain.enums import NivelActividadFisica, Sexo
from app.modulo1_usuarios.domain.perfil_infantil import (
    ALERGIA_MAX_LEN,
    ALERGIAS_MAX_ITEMS,
    EDAD_MAXIMA,
    EDAD_MINIMA,
    TUTOR_ID_MAX_LEN,
)


def _esquema() -> dict:
    return validador_perfiles_infantiles()["$jsonSchema"]


def test_campos_requeridos_y_sin_propiedades_extra():
    esquema = _esquema()
    assert esquema["additionalProperties"] is False
    assert set(esquema["required"]) == {
        "_id",
        "tutor_id",
        "nombre",
        "edad",
        "sexo",
        "peso_kg",
        "estatura_cm",
        "nivel_actividad_fisica",
        "habitos_alimenticios",
        "alergias",
        "objetivos",
        "activo",
        "creado_en",
        "actualizado_en",
    }


def test_enums_coinciden_con_el_dominio():
    esquema = _esquema()
    assert set(esquema["properties"]["sexo"]["enum"]) == {sexo.value for sexo in Sexo}
    assert set(esquema["properties"]["nivel_actividad_fisica"]["enum"]) == {
        nivel.value for nivel in NivelActividadFisica
    }


def test_edad_usa_el_rango_del_dominio():
    edad = _esquema()["properties"]["edad"]
    assert edad["bsonType"] == "int"
    assert edad["minimum"] == EDAD_MINIMA
    assert edad["maximum"] == EDAD_MAXIMA


def test_alergias_y_tutor_id_usan_los_topes_del_dominio():
    esquema = _esquema()
    alergias = esquema["properties"]["alergias"]
    assert alergias["maxItems"] == ALERGIAS_MAX_ITEMS
    assert alergias["items"]["maxLength"] == ALERGIA_MAX_LEN
    assert esquema["properties"]["tutor_id"]["maxLength"] == TUTOR_ID_MAX_LEN


def test_indice_parcial_por_tutor_activo():
    assert INDICE_TUTOR_ACTIVO["name"] == INDEX_NAME
    assert INDICE_TUTOR_ACTIVO["keys"] == [("tutor_id", 1)]
    assert INDICE_TUTOR_ACTIVO["partialFilterExpression"] == {"activo": True}


class _DbFalsa:
    def __init__(self, nombres: list[str]) -> None:
        self._nombres = nombres
        self.command = AsyncMock()
        self.create_collection = AsyncMock()
        self.coleccion = AsyncMock()

    async def list_collection_names(self) -> list[str]:
        return self._nombres

    def __getitem__(self, nombre: str):
        assert nombre == COLLECTION_NAME
        return self.coleccion


@pytest.mark.asyncio
async def test_asegurar_crea_la_coleccion_si_no_existe():
    db = _DbFalsa([])

    await asegurar_perfiles_infantiles(db)  # type: ignore[arg-type]

    db.create_collection.assert_awaited_once()
    kwargs = db.create_collection.await_args.kwargs
    assert kwargs["validationLevel"] == VALIDATION_LEVEL
    assert kwargs["validationAction"] == VALIDATION_ACTION
    assert "$jsonSchema" in kwargs["validator"]
    db.command.assert_not_awaited()
    db.coleccion.create_index.assert_awaited_once_with(
        [("tutor_id", 1)],
        name=INDEX_NAME,
        partialFilterExpression={"activo": True},
    )


@pytest.mark.asyncio
async def test_asegurar_actualiza_validador_sin_borrar_documentos():
    db = _DbFalsa([COLLECTION_NAME])

    await asegurar_perfiles_infantiles(db)  # type: ignore[arg-type]

    db.create_collection.assert_not_awaited()
    db.command.assert_awaited_once_with(
        "collMod",
        COLLECTION_NAME,
        validator=validador_perfiles_infantiles(),
        validationLevel=VALIDATION_LEVEL,
        validationAction=VALIDATION_ACTION,
    )
    db.coleccion.create_index.assert_awaited_once()
