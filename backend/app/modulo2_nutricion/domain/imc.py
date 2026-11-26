"""Calculo de IMC y clasificacion por percentiles OMS (5-19 anos).

Dominio puro: no importa FastAPI ni Mongo. Usa tablas LMS oficiales
WHO 2007 BMI-for-age (5-19 years), embebidas en CSV.

Fuente: https://www.who.int/tools/growth-reference-data-for-5to19-years/indicators/bmi-for-age
Categorias NEUTRAS: no se etiqueta al nino con terminos clinicos.
La respuesta incluye siempre un aviso orientativo.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.modulo1_usuarios.ports import Sexo

__all__ = ["ResultadoIMC", "evaluar_imc", "AVISO_ORIENTATIVO"]

AVISO_ORIENTATIVO = (
    "Este resultado es orientativo y no constituye un diagnostico medico. "
    "Consulta siempre a un profesional de la salud."
)

_DATOS = Path(__file__).parent / "datos" / "oms"
MES_MIN = 61
MES_MAX = 228
_CORTES = ((-2.0, "bajo"), (1.0, "adecuado"), (2.0, "alto"), (float("inf"), "muy_alto"))


@dataclass(frozen=True)
class ResultadoIMC:
    imc: float
    z: float
    categoria: str
    aviso: str = AVISO_ORIENTATIVO


@lru_cache(maxsize=2)
def _cargar(sexo_key: str) -> dict[int, tuple[float, float, float]]:
    p = _DATOS / f"bmi_z_{sexo_key}.csv"
    tabla: dict[int, tuple[float, float, float]] = {}
    with p.open() as f:
        for fila in csv.DictReader(f):
            tabla[int(fila["edad_meses"])] = (
                float(fila["L"]), float(fila["M"]), float(fila["S"]))
    assert len(tabla) == 168, f"{sexo_key}: {len(tabla)} filas, esperaba 168"
    assert MES_MIN in tabla and MES_MAX in tabla, f"{sexo_key}: faltan extremos"
    return tabla


def _sexo_key(sexo: Sexo) -> str | None:
    if sexo is Sexo.MASCULINO:
        return "boys"
    if sexo is Sexo.FEMENINO:
        return "girls"
    return None


def _lms(sexo: Sexo, edad_meses: int) -> tuple[float, float, float]:
    m = max(MES_MIN, min(MES_MAX, edad_meses))
    key = _sexo_key(sexo)
    if key is not None:
        return _cargar(key)[m]
    Lb, Mb, Sb = _cargar("boys")[m]
    Lg, Mg, Sg = _cargar("girls")[m]
    return ((Lb + Lg) / 2, (Mb + Mg) / 2, (Sb + Sg) / 2)


def calcular_z(imc: float, L: float, M: float, S: float) -> float:
    if L == 0:
        import math
        return math.log(imc / M) / S
    return ((imc / M) ** L - 1) / (L * S)


def _categoria(z: float) -> str:
    for corte, nombre in _CORTES:
        if z < corte:
            return nombre
    return "muy_alto"


def evaluar_imc(sexo: Sexo, edad_anios: int, peso_kg: float, estatura_cm: float) -> ResultadoIMC:
    if estatura_cm <= 0:
        raise ValueError("estatura_cm debe ser > 0")
    if peso_kg <= 0:
        raise ValueError("peso_kg debe ser > 0")
    altura_m = estatura_cm / 100.0
    imc = peso_kg / (altura_m * altura_m)
    L, M, S = _lms(sexo, edad_anios * 12)
    z = calcular_z(imc, L, M, S)
    return ResultadoIMC(imc=round(imc, 2), z=round(z, 3), categoria=_categoria(z))
