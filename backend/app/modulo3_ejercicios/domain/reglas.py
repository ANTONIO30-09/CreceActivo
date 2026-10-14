"""Reglas puras del Modulo 3: rachas, insignias y semanas.

Logica portada del aporte de Luis David Cespedes Camacho
(racha_actual, mejor_racha, insignias) y adaptada al dominio del proyecto.
Sin dependencias de Mongo, Firebase ni FastAPI.
"""
from __future__ import annotations

from datetime import date, timedelta

DIAS_GRACIA = 1

INSIGNIAS = (
    {"id": "primer_paso", "nombre": "Primer paso", "tipo": "total", "meta": 1},
    {"id": "racha_3", "nombre": "Ritmo en marcha", "tipo": "racha", "meta": 3},
    {"id": "racha_7", "nombre": "Una semana constante", "tipo": "racha", "meta": 7},
    {"id": "racha_14", "nombre": "Habito en raices", "tipo": "racha", "meta": 14},
    {"id": "racha_30", "nombre": "Un mes de cuidado", "tipo": "racha", "meta": 30},
    {"id": "total_10", "nombre": "10 pasos de cuidado", "tipo": "total", "meta": 10},
    {"id": "total_50", "nombre": "50 pasos de cuidado", "tipo": "total", "meta": 50},
    {"id": "variedad_3", "nombre": "Dia equilibrado", "tipo": "variedad", "meta": 3},
)


def _fechas_ordenadas(fechas: list[date]) -> list[date]:
    return sorted({f for f in fechas})


def racha_actual(fechas: list[date], hoy: date | None = None,
                 gracia: int = DIAS_GRACIA) -> int:
    """Dias consecutivos (con gracia) hasta hoy o el ultimo registro."""
    hoy = hoy or date.today()
    dias = _fechas_ordenadas(fechas)[::-1]
    if not dias or (hoy - dias[0]).days > gracia + 1:
        return 0
    racha = 1
    for i in range(1, len(dias)):
        if (dias[i - 1] - dias[i]).days <= gracia + 1:
            racha += 1
        else:
            break
    return racha


def mejor_racha(fechas: list[date], gracia: int = DIAS_GRACIA) -> int:
    """Racha mas larga historica."""
    dias = _fechas_ordenadas(fechas)
    if not dias:
        return 0
    mejor = actual = 1
    for i in range(1, len(dias)):
        if (dias[i] - dias[i - 1]).days <= gracia + 1:
            actual += 1
        else:
            actual = 1
        mejor = max(mejor, actual)
    return mejor


def semana_actual(hoy: date | None = None) -> tuple[date, date]:
    """Devuelve (lunes, domingo) de la semana que contiene `hoy`."""
    hoy = hoy or date.today()
    lunes = hoy - timedelta(days=hoy.weekday())
    domingo = lunes + timedelta(days=6)
    return lunes, domingo


def porcentaje_meta(completado: int, objetivo: int) -> int:
    """Porcentaje 0-100 de avance semanal de una meta."""
    if objetivo <= 0:
        return 0
    return min(100, round(completado / objetivo * 100))


def evaluar_insignias(total: int, mejor: int, variedad: int,
                      ya_ganadas: set[str]) -> list[dict]:
    """Devuelve las insignias NUEVAS que corresponden al progreso dado."""
    valores = {"total": total, "racha": mejor, "variedad": variedad}
    nuevas = []
    for ins in INSIGNIAS:
        if ins["id"] in ya_ganadas:
            continue
        if valores[ins["tipo"]] >= ins["meta"]:
            nuevas.append(ins)
    return nuevas
