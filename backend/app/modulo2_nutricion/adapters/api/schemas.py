"""Schemas Pydantic de entrada/salida HTTP del Modulo 2.

Capa HTTP: no son el dominio ni los DTOs publicos. Los schemas de
respuesta se construyen desde los DTOs.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida

__all__ = [
    "GuiaResponse",
    "PlatoResponse",
    "MenuResponse",
    "EspecialistaResponse",
    "SolicitudCreateRequest",
    "SolicitudResponse",
]


class GuiaResponse(BaseModel):
    """Respuesta publica de una guia."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    titulo: str
    categoria: str
    rango_edad: RangoEdad
    contenido: str
    habitos_clave: list[str]


class PlatoResponse(BaseModel):
    """Respuesta publica de un plato."""

    model_config = ConfigDict(from_attributes=True)

    nombre: str
    descripcion: str
    calorias_aprox: int
    ingredientes: list[str]


class MenuResponse(BaseModel):
    """Respuesta publica de un menu."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    titulo: str
    rango_edad: RangoEdad
    tipo_comida: TipoComida
    platos: list[PlatoResponse]
    recomendaciones: list[str]


class EspecialistaResponse(BaseModel):
    """Respuesta publica de un especialista."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_completo: str
    rol: str
    especialidad: str
    experiencia_anios: int
    biografia: str
    contacto_email: str
    disponible: bool


class SolicitudCreateRequest(BaseModel):
    """Body para POST /modulo2/solicitudes."""

    perfil_id: str = Field(..., min_length=1)
    especialista_id: str = Field(..., min_length=1)
    mensaje: str = Field(..., min_length=1, max_length=1000)


class SolicitudResponse(BaseModel):
    """Respuesta de POST /modulo2/solicitudes."""

    id: str
    estado: str
