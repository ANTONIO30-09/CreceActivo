"""Esquema Mongo de la coleccion tutores (Modulo 1)."""
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

__all__ = [
    "COLLECTION_TUTORES",
    "INDEX_TUTORES_EMAIL",
    "asegurar_tutores",
    "validador_tutores",
]

COLLECTION_TUTORES = "tutores"
INDEX_TUTORES_EMAIL = "idx_tutores_email_uid"

_UUID_PATTERN = (
    "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
    "-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
_VALIDATION_LEVEL = "strict"
_VALIDATION_ACTION = "error"


def validador_tutores() -> dict:
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": ["_id", "email", "nombre", "creado_en", "actualizado_en"],
            "properties": {
                "_id": {"bsonType": "string", "minLength": 1, "maxLength": 128},
                "email": {
                    "bsonType": "string",
                    "minLength": 5,
                    "maxLength": 200,
                },
                "nombre": {"bsonType": "string", "maxLength": 120},
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


async def asegurar_tutores(db: AsyncIOMotorDatabase) -> None:
    """Crea o actualiza el validador y el indice de tutores."""
    opciones = {
        "validator": validador_tutores(),
        "validationLevel": _VALIDATION_LEVEL,
        "validationAction": _VALIDATION_ACTION,
    }
    nombres = await db.list_collection_names()
    if COLLECTION_TUTORES not in nombres:
        await db.create_collection(COLLECTION_TUTORES, **opciones)
    else:
        await db.command("collMod", COLLECTION_TUTORES, **opciones)

    await db[COLLECTION_TUTORES].create_index(
        [("email", 1)],
        name=INDEX_TUTORES_EMAIL,
        unique=True,
    )
