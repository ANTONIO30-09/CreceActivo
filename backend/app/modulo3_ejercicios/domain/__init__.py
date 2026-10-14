"""Dominio del Modulo 3 (ejercicios, progreso y motivacion)."""
from .entidades import MetaFamiliar, RegistroActividad, ahora_utc, nuevo_id
from .enums import EstadoMeta, TipoActividad
from .excepciones import ErrorDominioEjercicios, MetaInvalida, RegistroInvalido
from .reglas import (
    DIAS_GRACIA,
    INSIGNIAS,
    evaluar_insignias,
    mejor_racha,
    porcentaje_meta,
    racha_actual,
    semana_actual,
)

__all__ = [
    "TipoActividad",
    "EstadoMeta",
    "RegistroActividad",
    "MetaFamiliar",
    "nuevo_id",
    "ahora_utc",
    "ErrorDominioEjercicios",
    "RegistroInvalido",
    "MetaInvalida",
    "INSIGNIAS",
    "DIAS_GRACIA",
    "racha_actual",
    "mejor_racha",
    "semana_actual",
    "porcentaje_meta",
    "evaluar_insignias",
]
