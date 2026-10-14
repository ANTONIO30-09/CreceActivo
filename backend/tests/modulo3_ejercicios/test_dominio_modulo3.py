"""Tests de dominio puro del Modulo 3. Sin Mongo ni Firebase."""
from __future__ import annotations

from datetime import date

import pytest

from app.modulo3_ejercicios.domain.entidades import (
    MetaFamiliar,
    RegistroActividad,
    ahora_utc,
    nuevo_id,
)
from app.modulo3_ejercicios.domain.enums import EstadoMeta, TipoActividad
from app.modulo3_ejercicios.domain.excepciones import MetaInvalida, RegistroInvalido
from app.modulo3_ejercicios.domain.reglas import (
    evaluar_insignias,
    mejor_racha,
    porcentaje_meta,
    racha_actual,
    semana_actual,
)


# ---------- racha_actual ----------

@pytest.mark.parametrize(
    "fechas,hoy,esperado",
    [
        ([], date(2026, 10, 14), 0),
        ([date(2026, 10, 14)], date(2026, 10, 14), 1),
        ([date(2026, 10, 12), date(2026, 10, 13), date(2026, 10, 14)],
         date(2026, 10, 14), 3),
        # Con 1 dia de gracia, gap de 1 dia se permite
        ([date(2026, 10, 12), date(2026, 10, 14)],
         date(2026, 10, 14), 2),
        # Gap de 2+ dias rompe
        ([date(2026, 10, 1), date(2026, 10, 14)],
         date(2026, 10, 14), 1),
    ],
)
def test_racha_actual(fechas, hoy, esperado):
    assert racha_actual(fechas, hoy) == esperado


def test_racha_actual_fecha_muy_vieja_devuelve_0():
    hoy = date(2026, 10, 14)
    fechas = [date(2026, 9, 1)]
    assert racha_actual(fechas, hoy) == 0


# ---------- mejor_racha ----------

def test_mejor_racha_lista_vacia():
    assert mejor_racha([]) == 0


def test_mejor_racha_detecta_la_mas_larga():
    fechas = [
        date(2026, 10, 1), date(2026, 10, 2), date(2026, 10, 3),
        date(2026, 10, 10), date(2026, 10, 11),
    ]
    assert mejor_racha(fechas) == 3


# ---------- semana_actual ----------

def test_semana_actual_lunes_a_domingo():
    lunes, domingo = semana_actual(date(2026, 10, 14))  # miercoles
    assert lunes == date(2026, 10, 12)
    assert domingo == date(2026, 10, 18)


# ---------- porcentaje_meta ----------

@pytest.mark.parametrize(
    "completado,objetivo,esperado",
    [(0, 7, 0), (3, 7, 43), (7, 7, 100), (10, 7, 100), (5, 0, 0)],
)
def test_porcentaje_meta(completado, objetivo, esperado):
    assert porcentaje_meta(completado, objetivo) == esperado


# ---------- evaluar_insignias ----------

def test_evaluar_insignias_sin_logros():
    nuevas = evaluar_insignias(total=0, mejor=0, variedad=0, ya_ganadas=set())
    assert nuevas == []


def test_evaluar_insignias_con_un_registro():
    nuevas = evaluar_insignias(total=1, mejor=1, variedad=1, ya_ganadas=set())
    ids = {i["id"] for i in nuevas}
    assert "primer_paso" in ids


def test_evaluar_insignias_no_duplica():
    nuevas = evaluar_insignias(
        total=10, mejor=7, variedad=3, ya_ganadas={"primer_paso", "racha_3"}
    )
    ids = {i["id"] for i in nuevas}
    assert "primer_paso" not in ids
    assert "racha_3" not in ids
    assert "racha_7" in ids
    assert "total_10" in ids
    assert "variedad_3" in ids


# ---------- Entidades ----------

def test_registro_actividad_valido():
    r = RegistroActividad(
        id=nuevo_id(), perfil_id="p1", tutor_id="t1",
        tipo=TipoActividad.AGUA, valor=8, fecha=date(2026, 10, 14),
        creado_en=ahora_utc(),
    )
    assert r.tipo == TipoActividad.AGUA


@pytest.mark.parametrize("valor", [-1, 10001])
def test_registro_valor_fuera_de_rango(valor):
    with pytest.raises(RegistroInvalido):
        RegistroActividad(
            id=nuevo_id(), perfil_id="p1", tutor_id="t1",
            tipo=TipoActividad.AGUA, valor=valor, fecha=date(2026, 10, 14),
            creado_en=ahora_utc(),
        )


def test_meta_valida():
    m = MetaFamiliar(
        id=nuevo_id(), perfil_id="p1", tutor_id="t1",
        titulo="Caminar 20 min", descripcion="Todos los dias",
        objetivo_semanal=5, estado=EstadoMeta.ACTIVA, creado_en=ahora_utc(),
    )
    assert m.objetivo_semanal == 5


@pytest.mark.parametrize("objetivo", [0, 8, -1])
def test_meta_objetivo_fuera_de_rango(objetivo):
    with pytest.raises(MetaInvalida):
        MetaFamiliar(
            id=nuevo_id(), perfil_id="p1", tutor_id="t1",
            titulo="X", descripcion="", objetivo_semanal=objetivo,
            estado=EstadoMeta.ACTIVA, creado_en=ahora_utc(),
        )


def test_meta_titulo_vacio():
    with pytest.raises(MetaInvalida):
        MetaFamiliar(
            id=nuevo_id(), perfil_id="p1", tutor_id="t1",
            titulo="   ", descripcion="", objetivo_semanal=3,
            estado=EstadoMeta.ACTIVA, creado_en=ahora_utc(),
        )
