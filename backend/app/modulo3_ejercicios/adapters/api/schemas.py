"""Schemas Pydantic de entrada/salida HTTP del Modulo 3 (progreso)."""
from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.modulo3_ejercicios.domain.enums import EstadoMeta, TipoActividad

__all__ = [
    "RegistroCreateRequest",
    "RegistroResponse",
    "MetaCreateRequest",
    "MetaResponse",
    "MarcarMetaRequest",
    "InsigniaResponse",
    "ProgresoResponse",
]


class RegistroCreateRequest(BaseModel):
    perfil_id: str = Field(..., min_length=1)
    tipo: TipoActividad
    valor: int = Field(..., ge=0, le=10000)


class RegistroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    perfil_id: str
    tutor_id: str
    tipo: TipoActividad
    valor: int
    fecha: date


class MetaCreateRequest(BaseModel):
    perfil_id: str = Field(..., min_length=1)
    titulo: str = Field(..., min_length=1, max_length=120)
    descripcion: str = Field(default="", max_length=500)
    objetivo_semanal: int = Field(..., ge=1, le=7)


class MetaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    perfil_id: str
    tutor_id: str
    titulo: str
    descripcion: str
    objetivo_semanal: int
    estado: EstadoMeta
    completado_semana: int
    porcentaje: int


class MarcarMetaRequest(BaseModel):
    fecha: str = Field(..., min_length=10, max_length=10)


class InsigniaResponse(BaseModel):
    id: str
    nombre: str
    tipo: str
    meta: int


class ProgresoResponse(BaseModel):
    perfil_id: str
    racha_actual: int
    mejor_racha: int
    total_registros: int
    insignias_ganadas: list[str]
