"""Esquemas Mongo del Modulo 3 (registros_actividad, metas_familiares).

Sigue la convencion del Modulo 1: snake_case, UUID string en _id,
activo/estado cuando aplica, creado_en y actualizado_en UTC.
"""
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.modulo3_ejercicios.domain.enums import EstadoMeta, TipoActividad

__all__ = [
    "COLLECTION_REGISTROS",
    "COLLECTION_METAS",
    "asegurar_colecciones_modulo3",
]

COLLECTION_REGISTROS = "registros_actividad"
COLLECTION_METAS = "metas_familiares"

VALIDATION_LEVEL = "strict"
VALIDATION_ACTION = "error"

_UUID_PATTERN = (
    "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
    "-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def _validador_registros() -> dict:
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": [
                "_id", "perfil_id", "tutor_id", "tipo", "valor",
                "fecha", "creado_en", "actualizado_en",
            ],
            "properties": {
                "_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "perfil_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "tutor_id": {"bsonType": "string", "minLength": 1, "maxLength": 128},
                "meta_id": {
                    "oneOf": [
                        {"bsonType": "string", "pattern": _UUID_PATTERN},
                        {"bsonType": "null"},
                    ]
                },
                "tipo": {"enum": [t.value for t in TipoActividad]},
                "valor": {"bsonType": "int", "minimum": 0, "maximum": 10000},
                "fecha": {"bsonType": "date"},
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


def _validador_metas() -> dict:
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": [
                "_id", "perfil_id", "tutor_id", "titulo", "descripcion",
                "objetivo_semanal", "estado", "creado_en", "actualizado_en",
            ],
            "properties": {
                "_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "perfil_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "tutor_id": {"bsonType": "string", "minLength": 1, "maxLength": 128},
                "titulo": {"bsonType": "string", "minLength": 1, "maxLength": 120},
                "descripcion": {"bsonType": "string", "maxLength": 500},
                "objetivo_semanal": {"bsonType": "int", "minimum": 1, "maximum": 7},
                "estado": {"enum": [e.value for e in EstadoMeta]},
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


INDICE_REGISTROS_PERFIL = {
    "keys": [("perfil_id", 1), ("fecha", 1)],
    "name": "idx_registros_perfil_fecha",
    "partialFilterExpression": None,
}

INDICE_METAS_PERFIL = {
    "keys": [("perfil_id", 1), ("estado", 1)],
    "name": "idx_metas_perfil_estado",
    "partialFilterExpression": None,
}


async def _asegurar(db, nombre: str, validador: dict, indice: dict) -> None:
    opciones = {
        "validator": validador,
        "validationLevel": VALIDATION_LEVEL,
        "validationAction": VALIDATION_ACTION,
    }
    nombres = await db.list_collection_names()
    if nombre not in nombres:
        await db.create_collection(nombre, **opciones)
    else:
        await db.command("collMod", nombre, **opciones)

    kwargs = {"name": indice["name"]}
    if indice["partialFilterExpression"] is not None:
        kwargs["partialFilterExpression"] = indice["partialFilterExpression"]
    await db[nombre].create_index(indice["keys"], **kwargs)


async def asegurar_colecciones_modulo3(db: AsyncIOMotorDatabase) -> None:
    """Crea o actualiza validadores e indices del Modulo 3."""
    await _asegurar(db, COLLECTION_REGISTROS, _validador_registros(), INDICE_REGISTROS_PERFIL)
    await _asegurar(db, COLLECTION_METAS, _validador_metas(), INDICE_METAS_PERFIL)
