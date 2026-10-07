"""Capa de persistencia del Modulo 1.

El esquema y los indices de `perfiles_infantiles` viven aqui.
El repositorio que implemente `PerfilInfantilPort` queda para la Fase 3.
"""
from .perfil_repository import PerfilInfantilRepository
from .perfiles_infantiles import asegurar_perfiles_infantiles

__all__ = ["asegurar_perfiles_infantiles"]
