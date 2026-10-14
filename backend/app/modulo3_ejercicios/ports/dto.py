"""DTOs publicos del Modulo 3 (progreso y motivacion)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from ..domain.enums import EstadoMeta, TipoActividad

__all__ = [
    "TipoActividad",
    "EstadoMeta",
    "RegistroDTO",
    "MetaDTO",
    "ProgresoDTO",
    "InsigniaDTO",
]


@dataclass(frozen=True)
class RegistroDTO:
    id: str
    perfil_id: str
    tutor_id: str
    tipo: TipoActividad
    valor: int
    fecha: date


@dataclass(frozen=True)
class MetaDTO:
    id: str
    perfil_id: str
    tutor_id: str
    titulo: str
    descripcion: str
    objetivo_semanal: int
    estado: EstadoMeta
    completado_semana: int
    porcentaje: int


@dataclass(frozen=True)
class InsigniaDTO:
    id: str
    nombre: str
    tipo: str
    meta: int


@dataclass(frozen=True)
class ProgresoDTO:
    perfil_id: str
    racha_actual: int
    mejor_racha: int
    total_registros: int
    insignias_ganadas: tuple[str, ...]
