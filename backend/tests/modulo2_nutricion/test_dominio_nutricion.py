"""Tests de dominio puro del módulo 2. Sin Mongo ni Firebase."""
from __future__ import annotations

import pytest

from app.modulo2_nutricion.domain.entidades import MenuInfantil, Plato
from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida
from app.modulo2_nutricion.domain.excepciones import (
    EdadFueraDeRango,
    MenuInvalido,
    PlatoInvalido,
)
from app.modulo2_nutricion.domain.reglas import obtener_rango_edad


# ---------- obtener_rango_edad ----------

@pytest.mark.parametrize(
    "edad,esperado",
    [
        (6, RangoEdad.DE_6_A_8),
        (7, RangoEdad.DE_6_A_8),
        (8, RangoEdad.DE_6_A_8),
        (9, RangoEdad.DE_9_A_11),
        (10, RangoEdad.DE_9_A_11),
        (11, RangoEdad.DE_9_A_11),
        (12, RangoEdad.DE_12_A_14),
        (13, RangoEdad.DE_12_A_14),
        (14, RangoEdad.DE_12_A_14),
    ],
)
def test_obtener_rango_edad_limites_validos(edad: int, esperado: RangoEdad) -> None:
    assert obtener_rango_edad(edad) is esperado


@pytest.mark.parametrize("edad", [5, 0, -1, 15, 100])
def test_obtener_rango_edad_fuera_de_rango(edad: int) -> None:
    with pytest.raises(EdadFueraDeRango):
        obtener_rango_edad(edad)


@pytest.mark.parametrize("edad", ["8", 8.0, None, True])
def test_obtener_rango_edad_tipo_invalido(edad) -> None:
    with pytest.raises(EdadFueraDeRango):
        obtener_rango_edad(edad)  # type: ignore[arg-type]


def test_obtener_rango_edad_no_es_valueerror_generico() -> None:
    # Sigue siendo capturable como ValueError (compatibilidad),
    # pero el tipo específico permite distinguirlo.
    with pytest.raises(ValueError):
        obtener_rango_edad(99)


def test_obtener_rango_edad_ya_no_vive_en_enums() -> None:
    from app.modulo2_nutricion.domain import enums
    assert not hasattr(enums, "obtener_rango_edad")


# ---------- Plato ----------

def _plato_valido(**overrides) -> Plato:
    base = dict(
        nombre="Puré de calabaza",
        descripcion="Puré suave con calabaza y zanahoria",
        calorias_aprox=180,
        ingredientes=("calabaza", "zanahoria"),
    )
    base.update(overrides)
    return Plato(**base)


def test_plato_valido_se_crea() -> None:
    p = _plato_valido()
    assert p.calorias_aprox == 180
    assert "calabaza" in p.ingredientes


def test_plato_es_inmutable() -> None:
    p = _plato_valido()
    with pytest.raises(Exception):
        p.nombre = "otro"  # type: ignore[misc]


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("nombre", ""),
        ("nombre", "   "),
        ("descripcion", ""),
        ("descripcion", "   "),
        ("calorias_aprox", -1),
        ("ingredientes", ()),
        ("ingredientes", ("calabaza", "")),
        ("ingredientes", ("", "zanahoria")),
    ],
)
def test_plato_invalido(campo: str, valor) -> None:
    with pytest.raises(PlatoInvalido):
        _plato_valido(**{campo: valor})


def test_plato_calorias_cero_es_valido() -> None:
    assert _plato_valido(calorias_aprox=0).calorias_aprox == 0


# ---------- MenuInfantil ----------

def _menu_valido(**overrides) -> MenuInfantil:
    base = dict(
        titulo="Desayuno saludable",
        rango_edad=RangoEdad.DE_6_A_8,
        tipo_comida=TipoComida.DESAYUNO,
        platos=(_plato_valido(),),
        recomendaciones=("Acompañar con agua",),
    )
    base.update(overrides)
    return MenuInfantil(**base)


def test_menu_valido_se_crea() -> None:
    m = _menu_valido()
    assert m.rango_edad is RangoEdad.DE_6_A_8
    assert len(m.platos) == 1


def test_menu_es_inmutable() -> None:
    m = _menu_valido()
    with pytest.raises(Exception):
        m.titulo = "otro"  # type: ignore[misc]


@pytest.mark.parametrize(
    "campo,valor",
    [
        ("titulo", ""),
        ("titulo", "   "),
        ("platos", ()),
        ("platos", ("no soy un Plato",)),
        ("recomendaciones", ("ok", "")),
        ("recomendaciones", ("   ",)),
    ],
)
def test_menu_invalido(campo: str, valor) -> None:
    with pytest.raises(MenuInvalido):
        _menu_valido(**{campo: valor})


def test_menu_recomendaciones_vacias_es_valido() -> None:
    assert _menu_valido(recomendaciones=()).recomendaciones == ()
