"""Esquema Mongo de la coleccion perfiles_infantiles.

El validador replica las invariantes del dominio para que un insert
directo a Atlas no pueda saltarse las reglas de la entidad. Los modulos
2 y 3 no importan este modulo: consumen el puerto.
"""
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.modulo1_usuarios.domain.enums import NivelActividadFisica, Sexo
from app.modulo1_usuarios.domain.perfil_infantil import (
    ALERGIA_MAX_LEN,
    ALERGIAS_MAX_ITEMS,
    EDAD_MAXIMA,
    EDAD_MINIMA,
    ESTATURA_MAX_CM,
    HABITOS_MAX_LEN,
    NOMBRE_MAX_LEN,
    OBJETIVOS_MAX_LEN,
    PESO_MAX_KG,
    TUTOR_ID_MAX_LEN,
)

__all__ = [
    "COLLECTION_NAME",
    "INDEX_NAME",
    "INDICE_TUTOR_ACTIVO",
    "VALIDATION_ACTION",
    "VALIDATION_LEVEL",
    "asegurar_perfiles_infantiles",
    "validador_perfiles_infantiles",
]

COLLECTION_NAME = "perfiles_infantiles"
INDEX_NAME = "idx_perfiles_tutor_activo"
VALIDATION_LEVEL = "strict"
VALIDATION_ACTION = "error"

# UUID canonico (8-4-4-4-12). _id es string, no ObjectId.
_UUID_PATTERN = (
    "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
    "-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

INDICE_TUTOR_ACTIVO = {
    "keys": [("tutor_id", 1)],
    "name": INDEX_NAME,
    "partialFilterExpression": {"activo": True},
}


def _texto_opcional(max_len: int) -> dict:
    """String no vacio acotado, o null. MongoDB usa JSON Schema draft 4."""
    return {
        "anyOf": [
            {"bsonType": "null"},
            {"bsonType": "string", "minLength": 1, "maxLength": max_len},
        ]
    }


def _numero_positivo(maximo: float) -> dict:
    """Mayor a 0 y menor o igual a maximo. exclusiveMinimum es booleano en draft 4."""
    return {
        "bsonType": ["double", "int", "long", "decimal"],
        "minimum": 0,
        "exclusiveMinimum": True,
        "maximum": maximo,
    }


def validador_perfiles_infantiles() -> dict:
    """Documento validator de Mongo ($jsonSchema)."""
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": [
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
            ],
            "properties": {
                "_id": {
                    "bsonType": "string",
                    "pattern": _UUID_PATTERN,
                    "description": "UUID string. No ObjectId.",
                },
                "tutor_id": {
                    "bsonType": "string",
                    "minLength": 1,
                    "maxLength": TUTOR_ID_MAX_LEN,
                    "description": "UID de Firebase del tutor. No es un UUID.",
                },
                "nombre": {
                    "bsonType": "string",
                    "minLength": 1,
                    "maxLength": NOMBRE_MAX_LEN,
                },
                "edad": {
                    "bsonType": "int",
                    "minimum": EDAD_MINIMA,
                    "maximum": EDAD_MAXIMA,
                    "description": (
                        "Edad declarada por el tutor, entre 6 y 14. "
                        "No se calcula desde una fecha de nacimiento."
                    ),
                },
                "sexo": {
                    "enum": [sexo.value for sexo in Sexo],
                },
                "peso_kg": _numero_positivo(PESO_MAX_KG),
                "estatura_cm": _numero_positivo(ESTATURA_MAX_CM),
                "nivel_actividad_fisica": {
                    "enum": [nivel.value for nivel in NivelActividadFisica],
                },
                "habitos_alimenticios": _texto_opcional(HABITOS_MAX_LEN),
                "alergias": {
                    "bsonType": "array",
                    "maxItems": ALERGIAS_MAX_ITEMS,
                    "items": {
                        "bsonType": "string",
                        "minLength": 1,
                        "maxLength": ALERGIA_MAX_LEN,
                    },
                },
                "objetivos": _texto_opcional(OBJETIVOS_MAX_LEN),
                "activo": {"bsonType": "bool"},
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


def _opciones_de_validacion() -> dict:
    return {
        "validator": validador_perfiles_infantiles(),
        "validationLevel": VALIDATION_LEVEL,
        "validationAction": VALIDATION_ACTION,
    }


async def asegurar_perfiles_infantiles(db: AsyncIOMotorDatabase) -> None:
    """Crea o actualiza validador e indice. Idempotente. No borra documentos."""
    nombres = await db.list_collection_names()
    if COLLECTION_NAME not in nombres:
        await db.create_collection(COLLECTION_NAME, **_opciones_de_validacion())
    else:
        await db.command(
            "collMod",
            COLLECTION_NAME,
            **_opciones_de_validacion(),
        )

    indice = INDICE_TUTOR_ACTIVO
    await db[COLLECTION_NAME].create_index(
        indice["keys"],
        name=indice["name"],
        partialFilterExpression=indice["partialFilterExpression"],
    )
