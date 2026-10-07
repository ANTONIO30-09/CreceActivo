from dataclasses import dataclass
from typing import Tuple

from .enums import RangoEdad, TipoComida


@dataclass(frozen=True)
class Plato:
    nombre: str
    descripcion: str
    calorias_aprox: int
    ingredientes: Tuple[str, ...]


@dataclass(frozen=True)
class MenuInfantil:
    titulo: str
    rango_edad: RangoEdad
    tipo_comida: TipoComida
    platos: Tuple[Plato, ...]
    recomendaciones: Tuple[str, ...]
