"""Infraestructura transversal del backend (config, db, seguridad)."""
from .config import Settings, get_settings

__all__ = ["Settings", "get_settings"]
