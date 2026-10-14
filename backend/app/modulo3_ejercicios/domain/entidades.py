"""Entidades inmutables del dominio del Modulo 3."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import uuid4

from .enums import EstadoMeta, TipoActividad
from .excepciones import MetaInvalida, RegistroInvalido

MAX_TITULO = 120
MAX_DESCRIPCION = 500
MAX_VALOR = 10000


@dataclass(frozen=True)
class RegistroActividad:
    """Una actividad completada por un perfil en una fecha."""
    id: str
    perfil_id: str
    tutor_id: str
    tipo: TipoActividad
    valor: int
    fecha: date
    creado_en: datetime

    def __post_init__(self) -> None:
        if not self.id:
            raise RegistroInvalido("El id no puede estar vacio.")
        if not self.perfil_id:
            raise RegistroInvalido("El perfil_id no puede estar vacio.")
        if not self.tutor_id:
            raise RegistroInvalido("El tutor_id no puede estar vacio.")
        if not isinstance(self.tipo, TipoActividad):
            raise RegistroInvalido("El tipo debe ser TipoActividad.")
        if self.valor < 0 or self.valor > MAX_VALOR:
            raise RegistroInvalido(
                f"El valor debe estar entre 0 y {MAX_VALOR}."
            )


@dataclass(frozen=True)
class MetaFamiliar:
    """Meta semanal que un tutor define para un perfil infantil."""
    id: str
    perfil_id: str
    tutor_id: str
    titulo: str
    descripcion: str
    objetivo_semanal: int
    estado: EstadoMeta
    creado_en: datetime

    def __post_init__(self) -> None:
        if not self.id:
            raise MetaInvalida("El id no puede estar vacio.")
        if not self.perfil_id:
            raise MetaInvalida("El perfil_id no puede estar vacio.")
        if not self.tutor_id:
            raise MetaInvalida("El tutor_id no puede estar vacio.")
        if not self.titulo or not self.titulo.strip():
            raise MetaInvalida("El titulo no puede estar vacio.")
        if len(self.titulo) > MAX_TITULO:
            raise MetaInvalida(f"El titulo no puede superar {MAX_TITULO} caracteres.")
        if len(self.descripcion) > MAX_DESCRIPCION:
            raise MetaInvalida(
                f"La descripcion no puede superar {MAX_DESCRIPCION} caracteres."
            )
        if self.objetivo_semanal < 1 or self.objetivo_semanal > 7:
            raise MetaInvalida("El objetivo semanal debe estar entre 1 y 7.")
        if not isinstance(self.estado, EstadoMeta):
            raise MetaInvalida("El estado debe ser EstadoMeta.")


def nuevo_id() -> str:
    """Genera un id UUID string para nuevas entidades."""
    return str(uuid4())


def ahora_utc() -> datetime:
    """Fecha/hora actual en UTC."""
    return datetime.now(timezone.utc)
