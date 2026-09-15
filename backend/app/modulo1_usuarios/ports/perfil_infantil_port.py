"""Contrato publico del Modulo 1 (Usuarios y perfil infantil).

Este archivo es la UNICA superficie que los Modulos 2 y 3 pueden importar
de `modulo1_usuarios`. No deben importar `domain`, `adapters` ni `service`
directamente: si manana separamos el modulo en microservicio, solo cambia
la implementacion del puerto, no la logica de nadie.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from ..domain.enums import NivelActividadFisica, Sexo
from ..domain.perfil_infantil import PerfilInfantil

__all__ = [
    "Sexo",
    "NivelActividadFisica",
    "PerfilInfantilDTO",
    "PerfilInfantilPort",
]


@dataclass(frozen=True)
class PerfilInfantilDTO:
    """Read-model publico de un perfil infantil.

    No expone campos internos (activo, creado_en, actualizado_en).
    Inmutable, sin comportamiento de negocio.
    """

    id: str
    tutor_id: str
    nombre: str
    edad: int
    sexo: Sexo
    peso_kg: float
    estatura_cm: float
    nivel_actividad_fisica: NivelActividadFisica
    habitos_alimenticios: str | None
    alergias: tuple[str, ...]
    objetivos: str | None

    @classmethod
    def desde_entidad(cls, perfil: PerfilInfantil) -> "PerfilInfantilDTO":
        """Proyecta una entidad de dominio al read-model publico."""
        return cls(
            id=perfil.id,
            tutor_id=perfil.tutor_id,
            nombre=perfil.nombre,
            edad=perfil.edad,
            sexo=perfil.sexo,
            peso_kg=perfil.peso_kg,
            estatura_cm=perfil.estatura_cm,
            nivel_actividad_fisica=perfil.nivel_actividad_fisica,
            habitos_alimenticios=perfil.habitos_alimenticios,
            alergias=perfil.alergias,
            objetivos=perfil.objetivos,
        )


@runtime_checkable
class PerfilInfantilPort(Protocol):
    """Puerto que el Modulo 1 OFRECE a los Modulos 2 y 3.

    Semantica:
    - Perfil inexistente o inactivo -> None / lista vacia / False.
    - No se lanzan excepciones de dominio en esta fase (decision del contrato).
    """

    async def obtener_por_id(self, perfil_id: str) -> PerfilInfantilDTO | None:
        ...

    async def listar_por_tutor(self, tutor_id: str) -> list[PerfilInfantilDTO]:
        ...

    async def existe(self, perfil_id: str) -> bool:
        ...
