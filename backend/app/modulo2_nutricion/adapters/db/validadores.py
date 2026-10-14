"""Esquemas Mongo de las colecciones del Modulo 2.

Los validadores replican las invariantes del dominio. Se aplican al
arrancar con asegurar_colecciones_modulo2, idempotente.
"""
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida

__all__ = [
    "COLLECTION_GUIAS",
    "COLLECTION_MENUS",
    "COLLECTION_ESPECIALISTAS",
    "COLLECTION_SOLICITUDES",
    "asegurar_colecciones_modulo2",
]

COLLECTION_GUIAS = "guias_nutricionales"
COLLECTION_MENUS = "menus_infantiles"
COLLECTION_ESPECIALISTAS = "especialistas"
COLLECTION_SOLICITUDES = "solicitudes_orientacion"

VALIDATION_LEVEL = "strict"
VALIDATION_ACTION = "error"

_UUID_PATTERN = (
    "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
    "-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def _validador_guias() -> dict:
    """Validador de la coleccion guias_nutricionales."""
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": [
                "_id", "titulo", "categoria", "rango_edad",
                "contenido", "habitos_clave", "activo",
                "creado_en", "actualizado_en",
            ],
            "properties": {
                "_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "titulo": {
                    "bsonType": "string", "minLength": 1, "maxLength": 120,
                },
                "categoria": {
                    "bsonType": "string", "minLength": 1, "maxLength": 80,
                },
                "rango_edad": {"enum": [r.value for r in RangoEdad]},
                "contenido": {
                    "bsonType": "string", "minLength": 1, "maxLength": 5000,
                },
                "habitos_clave": {
                    "bsonType": "array",
                    "maxItems": 10,
                    "items": {
                        "bsonType": "string", "minLength": 1, "maxLength": 200,
                    },
                },
                "activo": {"bsonType": "bool"},
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


def _validador_menus() -> dict:
    """Validador de la coleccion menus_infantiles."""
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": [
                "_id", "titulo", "rango_edad", "tipo_comida",
                "platos", "recomendaciones", "activo",
                "creado_en", "actualizado_en",
            ],
            "properties": {
                "_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "titulo": {
                    "bsonType": "string", "minLength": 1, "maxLength": 120,
                },
                "rango_edad": {"enum": [r.value for r in RangoEdad]},
                "tipo_comida": {"enum": [t.value for t in TipoComida]},
                "platos": {
                    "bsonType": "array",
                    "minItems": 1,
                    "items": {
                        "bsonType": "object",
                        "additionalProperties": False,
                        "required": [
                            "nombre", "descripcion",
                            "calorias_aprox", "ingredientes",
                        ],
                        "properties": {
                            "nombre": {
                                "bsonType": "string",
                                "minLength": 1,
                                "maxLength": 100,
                            },
                            "descripcion": {
                                "bsonType": "string",
                                "minLength": 1,
                                "maxLength": 300,
                            },
                            "calorias_aprox": {
                                "bsonType": "int", "minimum": 0,
                            },
                            "ingredientes": {
                                "bsonType": "array",
                                "minItems": 1,
                                "items": {
                                    "bsonType": "string",
                                    "minLength": 1,
                                    "maxLength": 80,
                                },
                            },
                        },
                    },
                },
                "recomendaciones": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "string", "minLength": 1, "maxLength": 200,
                    },
                },
                "activo": {"bsonType": "bool"},
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


def _validador_especialistas() -> dict:
    """Validador de la coleccion especialistas."""
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": [
                "_id", "nombre_completo", "rol", "especialidad",
                "experiencia_anios", "biografia", "contacto_email",
                "disponible", "creado_en", "actualizado_en",
            ],
            "properties": {
                "_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "nombre_completo": {
                    "bsonType": "string", "minLength": 1, "maxLength": 100,
                },
                "rol": {
                    "enum": ["Nutricionista", "Pediatra", "Entrenador"],
                },
                "especialidad": {
                    "bsonType": "string", "minLength": 1, "maxLength": 100,
                },
                "experiencia_anios": {
                    "bsonType": "int", "minimum": 0,
                },
                "biografia": {
                    "bsonType": "string", "minLength": 1, "maxLength": 1000,
                },
                "contacto_email": {
                    "bsonType": "string", "minLength": 5, "maxLength": 120,
                },
                "disponible": {"bsonType": "bool"},
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


def _validador_solicitudes() -> dict:
    """Validador de la coleccion solicitudes_orientacion."""
    return {
        "$jsonSchema": {
            "bsonType": "object",
            "additionalProperties": False,
            "required": [
                "_id", "tutor_id", "perfil_id", "especialista_id",
                "mensaje", "estado", "creado_en", "actualizado_en",
            ],
            "properties": {
                "_id": {"bsonType": "string", "pattern": _UUID_PATTERN},
                "tutor_id": {
                    "bsonType": "string", "minLength": 1, "maxLength": 128,
                },
                "perfil_id": {
                    "bsonType": "string", "pattern": _UUID_PATTERN,
                },
                "especialista_id": {
                    "bsonType": "string", "pattern": _UUID_PATTERN,
                },
                "mensaje": {
                    "bsonType": "string", "minLength": 1, "maxLength": 1000,
                },
                "estado": {
                    "enum": ["pendiente", "respondida", "cerrada"],
                },
                "creado_en": {"bsonType": "date"},
                "actualizado_en": {"bsonType": "date"},
            },
        }
    }


INDICE_MENUS = {
    "keys": [("rango_edad", 1), ("tipo_comida", 1)],
    "name": "idx_menus_rango_tipo",
    "partialFilterExpression": {"activo": True},
}

INDICE_GUIAS = {
    "keys": [("rango_edad", 1)],
    "name": "idx_guias_rango",
    "partialFilterExpression": {"activo": True},
}

INDICE_ESPECIALISTAS = {
    "keys": [("disponible", 1)],
    "name": "idx_especialistas_disponible",
    "partialFilterExpression": None,
}

INDICE_SOLICITUDES = {
    "keys": [("tutor_id", 1)],
    "name": "idx_solicitudes_tutor",
    "partialFilterExpression": None,
}


def _opciones_de_validacion(validador: dict) -> dict:
    return {
        "validator": validador,
        "validationLevel": VALIDATION_LEVEL,
        "validationAction": VALIDATION_ACTION,
    }


async def _asegurar_coleccion(
    db: AsyncIOMotorDatabase,
    nombre: str,
    validador: dict,
    indice: dict,
) -> None:
    """Crea o actualiza validador e indice de una coleccion. Idempotente."""
    nombres = await db.list_collection_names()
    if nombre not in nombres:
        await db.create_collection(nombre, **_opciones_de_validacion(validador))
    else:
        await db.command("collMod", nombre, **_opciones_de_validacion(validador))

    kwargs = {"name": indice["name"]}
    if indice["partialFilterExpression"] is not None:
        kwargs["partialFilterExpression"] = indice["partialFilterExpression"]
    await db[nombre].create_index(indice["keys"], **kwargs)


async def asegurar_colecciones_modulo2(db: AsyncIOMotorDatabase) -> None:
    """Crea o actualiza validadores e indices de las 4 colecciones del M2."""
    await _asegurar_coleccion(
        db, COLLECTION_GUIAS, _validador_guias(), INDICE_GUIAS,
    )
    await _asegurar_coleccion(
        db, COLLECTION_MENUS, _validador_menus(), INDICE_MENUS,
    )
    await _asegurar_coleccion(
        db, COLLECTION_ESPECIALISTAS, _validador_especialistas(), INDICE_ESPECIALISTAS,
    )
    await _asegurar_coleccion(
        db, COLLECTION_SOLICITUDES, _validador_solicitudes(), INDICE_SOLICITUDES,
    )
