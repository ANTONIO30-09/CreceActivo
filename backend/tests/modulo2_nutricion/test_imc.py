"""Tests del dominio IMC/OMS (Modulo 2)."""
from __future__ import annotations
import csv
from pathlib import Path
import pytest
from app.modulo1_usuarios.ports import Sexo
from app.modulo2_nutricion.domain.imc import (
    AVISO_ORIENTATIVO, _lms, calcular_z, evaluar_imc,
)

CSV_BOYS = Path("app/modulo2_nutricion/domain/datos/oms/bmi_z_boys.csv")


def test_tabla_oms_168_filas():
    with CSV_BOYS.open() as f:
        filas = list(csv.DictReader(f))
    assert len(filas) == 168
    assert filas[0]["edad_meses"] == "61"
    assert filas[-1]["edad_meses"] == "228"


def test_z_cero_en_mediana():
    L, M, S = _lms(Sexo.MASCULINO, 61)
    assert abs(calcular_z(M, L, M, S)) < 1e-9


def test_categoria_adecuado_en_mediana():
    M = 15.2641
    peso = M * 1.10 * 1.10
    r = evaluar_imc(Sexo.MASCULINO, 5, peso, 110.0)
    assert r.categoria == "adecuado"
    assert abs(r.z) < 0.01
    assert r.aviso == AVISO_ORIENTATIVO


def test_bajo():
    r = evaluar_imc(Sexo.FEMENINO, 10, 15.0, 150.0)
    assert r.categoria == "bajo"
    assert r.z < -2


def test_muy_alto():
    r = evaluar_imc(Sexo.MASCULINO, 10, 90.0, 140.0)
    assert r.categoria == "muy_alto"
    assert r.z > 2


def test_sexo_otro_no_rompe():
    r = evaluar_imc(Sexo.OTRO, 8, 25.0, 130.0)
    assert r.aviso == AVISO_ORIENTATIVO
    assert r.categoria in {"bajo", "adecuado", "alto", "muy_alto"}


def test_edad_fuera_de_rango_se_recorta():
    r = evaluar_imc(Sexo.FEMENINO, 3, 12.0, 95.0)
    assert isinstance(r.z, float)


def test_entradas_invalidas():
    with pytest.raises(ValueError):
        evaluar_imc(Sexo.MASCULINO, 8, 25.0, 0.0)
    with pytest.raises(ValueError):
        evaluar_imc(Sexo.MASCULINO, 8, 0.0, 130.0)
