"""Entidades del dominio de nutrición. Inmutables y auto-validadas."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .enums import RangoEdad, TipoComida
from .excepciones import MenuInvalido, PlatoInvalido


@dataclass(frozen=True)
class Plato:
    nombre: str
    descripcion: str
    calorias_aprox: int
    ingredientes: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise PlatoInvalido("El nombre del plato no puede estar vacío.")
        if not self.descripcion or not self.descripcion.strip():
            raise PlatoInvalido("La descripción del plato no puede estar vacía.")
        if self.calorias_aprox < 0:
            raise PlatoInvalido("Las calorías no pueden ser negativas.")
        if not self.ingredientes:
            raise PlatoInvalido("El plato debe tener al menos un ingrediente.")
        if any(not i or not i.strip() for i in self.ingredientes):
            raise PlatoInvalido("Los ingredientes no pueden estar vacíos.")


@dataclass(frozen=True)
class MenuInfantil:
    titulo: str
    rango_edad: RangoEdad
    tipo_comida: TipoComida
    platos: Tuple[Plato, ...]
    recomendaciones: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.titulo or not self.titulo.strip():
            raise MenuInvalido("El título del menú no puede estar vacío.")
        if not self.platos:
            raise MenuInvalido("El menú debe tener al menos un plato.")
        if any(not isinstance(p, Plato) for p in self.platos):
            raise MenuInvalido("Todos los elementos de platos deben ser Plato.")
        if any(not r or not r.strip() for r in self.recomendaciones):
            raise MenuInvalido("Las recomendaciones no pueden estar vacías.")
