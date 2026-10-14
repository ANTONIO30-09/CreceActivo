"""[DEPRECATED] Modelos Pydantic iniciales del Modulo 2.

Aporte historico de Misael Patrick Ramos Torrez (commit c7f57b3).
Estos modelos fueron el primer esqueleto de datos del modulo, pero la
arquitectura hexagonica del proyecto los reemplazo por:

- domain/entidades.py           -> Plato, MenuInfantil (dataclasses puras)
- domain/enums.py               -> RangoEdad, TipoComida
- ports/dto.py                  -> GuiaDTO, PlatoDTO, MenuDTO, EspecialistaDTO
- adapters/api/schemas.py       -> GuiaResponse, MenuResponse, ...

Este archivo se mantiene como referencia historica. No debe importarse.
El seed_mod2.py y el router del modulo usan los modulos correctos.

Deprecado desde: 2026-10-14.
"""
from __future__ import annotations
