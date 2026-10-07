
from __future__ import annotations
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from app.modulo1_usuarios.domain.enums import NivelActividadFisica, Sexo
from app.modulo1_usuarios.domain.perfil_infantil import PerfilInfantil
from app.modulo1_usuarios.ports.perfil_infantil_port import PerfilInfantilDTO

from .perfiles_infantiles import COLLECTION_NAME

__all__ = ["PerfilInfantilRepository"]


def _a_utc(valor: datetime) -> datetime:
    """Mongo devuelve fechas sin zona horaria; la entidad exige UTC."""
    if valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor


def _entidad_a_doc(perfil: PerfilInfantil) -> dict[str, Any]:
    """Entidad -> documento Mongo (el `id` pasa a ser `_id`)."""
    return {
        "_id": perfil.id,
        "tutor_id": perfil.tutor_id,
        "nombre": perfil.nombre,
        "edad": perfil.edad,
        "sexo": perfil.sexo.value,
        "peso_kg": perfil.peso_kg,
        "estatura_cm": perfil.estatura_cm,
        "nivel_actividad_fisica": perfil.nivel_actividad_fisica.value,
        "habitos_alimenticios": perfil.habitos_alimenticios,
        "alergias": list(perfil.alergias),  # Mongo guarda listas, no tuplas
        "objetivos": perfil.objetivos,
        "activo": perfil.activo,
        "creado_en": perfil.creado_en,
        "actualizado_en": perfil.actualizado_en,
    }


def _doc_a_entidad(doc: dict[str, Any]) -> PerfilInfantil:
    """Documento Mongo -> entidad (valida de nuevo las reglas del dominio)."""
    return PerfilInfantil(
        id=doc["_id"],
        tutor_id=doc["tutor_id"],
        nombre=doc["nombre"],
        edad=doc["edad"],
        sexo=Sexo(doc["sexo"]),
        peso_kg=doc["peso_kg"],
        estatura_cm=doc["estatura_cm"],
        nivel_actividad_fisica=NivelActividadFisica(doc["nivel_actividad_fisica"]),
        habitos_alimenticios=doc.get("habitos_alimenticios"),
        alergias=tuple(doc.get("alergias", [])),
        objetivos=doc.get("objetivos"),
        activo=doc["activo"],
        creado_en=_a_utc(doc["creado_en"]),
        actualizado_en=_a_utc(doc["actualizado_en"]),
    )


class PerfilInfantilRepository:
    """Acceso a la coleccion `perfiles_infantiles`."""

    def __init__(self, db: Any) -> None:
        self._col = db[COLLECTION_NAME]

    # ---- Puerto publico (PerfilInfantilPort) ----

    async def obtener_por_id(self, perfil_id: str) -> PerfilInfantilDTO | None:
        doc = await self._col.find_one({"_id": perfil_id, "activo": True})
        if doc is None:
            return None
        return PerfilInfantilDTO.desde_entidad(_doc_a_entidad(doc))

    async def listar_por_tutor(self, tutor_id: str) -> list[PerfilInfantilDTO]:
        cursor = self._col.find({"tutor_id": tutor_id, "activo": True})
        docs = await cursor.to_list(length=None)
        return [PerfilInfantilDTO.desde_entidad(_doc_a_entidad(d)) for d in docs]

    async def existe(self, perfil_id: str) -> bool:
        total = await self._col.count_documents(
            {"_id": perfil_id, "activo": True}, limit=1
        )
        return total > 0

    # ---- Metodos internos del Modulo 1 (no son parte del puerto) ----

    async def obtener_entidad(self, perfil_id: str) -> PerfilInfantil | None:
        """Uso interno del Modulo 1: devuelve la entidad completa, no el DTO."""
        doc = await self._col.find_one({"_id": perfil_id, "activo": True})
        return None if doc is None else _doc_a_entidad(doc)

    async def insertar(self, perfil: PerfilInfantil) -> None:
        """Guarda un perfil nuevo. El validador de Mongo es la segunda barrera."""
        await self._col.insert_one(_entidad_a_doc(perfil))

    async def actualizar(self, perfil: PerfilInfantil) -> None:
        """Actualiza un perfil existente."""
        await self._col.replace_one({"_id": perfil.id}, _entidad_a_doc(perfil))

    async def desactivar(self, perfil_id: str) -> bool:
        """Borrado suave: marca activo=False."""
        res = await self._col.update_one(
            {"_id": perfil_id},
            {"$set": {"activo": False, "actualizado_en": datetime.now(timezone.utc)}}
        )
        return res.modified_count > 0