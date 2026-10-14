"""Repositorio Mongo del Modulo 2.

Implementa ContenidoNutricionalPort sobre las 4 colecciones del modulo.
Uso interno: crear (seed) e implementar el puerto publico.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida
from app.modulo2_nutricion.ports.dto import (
    EspecialistaDTO,
    GuiaDTO,
    MenuDTO,
    PlatoDTO,
)

from .validadores import (
    COLLECTION_ESPECIALISTAS,
    COLLECTION_GUIAS,
    COLLECTION_MENUS,
    COLLECTION_SOLICITUDES,
)

__all__ = ["NutricionRepository"]


def _a_utc(valor: datetime | None) -> datetime:
    """Mongo devuelve fechas sin zona horaria; normalizamos a UTC."""
    if valor is None:
        return datetime.now(timezone.utc)
    if valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor


def _doc_a_guia(doc: dict[str, Any]) -> GuiaDTO:
    return GuiaDTO(
        id=doc["_id"],
        titulo=doc["titulo"],
        categoria=doc["categoria"],
        rango_edad=RangoEdad(doc["rango_edad"]),
        contenido=doc["contenido"],
        habitos_clave=tuple(doc.get("habitos_clave", [])),
    )


def _doc_a_menu(doc: dict[str, Any]) -> MenuDTO:
    platos = tuple(
        PlatoDTO(
            nombre=p["nombre"],
            descripcion=p["descripcion"],
            calorias_aprox=p["calorias_aprox"],
            ingredientes=tuple(p.get("ingredientes", [])),
        )
        for p in doc.get("platos", [])
    )
    return MenuDTO(
        id=doc["_id"],
        titulo=doc["titulo"],
        rango_edad=RangoEdad(doc["rango_edad"]),
        tipo_comida=TipoComida(doc["tipo_comida"]),
        platos=platos,
        recomendaciones=tuple(doc.get("recomendaciones", [])),
    )


def _doc_a_especialista(doc: dict[str, Any]) -> EspecialistaDTO:
    return EspecialistaDTO(
        id=doc["_id"],
        nombre_completo=doc["nombre_completo"],
        rol=doc["rol"],
        especialidad=doc["especialidad"],
        experiencia_anios=doc["experiencia_anios"],
        biografia=doc["biografia"],
        contacto_email=doc["contacto_email"],
        disponible=doc["disponible"],
    )


class NutricionRepository:
    """Acceso a las 4 colecciones del Modulo 2.

    Implementa ContenidoNutricionalPort. Tambien ofrece metodos internos
    (insertar_*) para que el seed cargue datos sin pasar por el puerto.
    """

    def __init__(self, db: Any) -> None:
        self._guias = db[COLLECTION_GUIAS]
        self._menus = db[COLLECTION_MENUS]
        self._especialistas = db[COLLECTION_ESPECIALISTAS]
        self._solicitudes = db[COLLECTION_SOLICITUDES]

    # ---- Puerto publico: guias ----

    async def listar_guias(
        self, rango_edad: RangoEdad | None = None
    ) -> list[GuiaDTO]:
        filtro: dict[str, Any] = {"activo": True}
        if rango_edad is not None:
            filtro["rango_edad"] = rango_edad.value
        cursor = self._guias.find(filtro)
        docs = await cursor.to_list(length=None)
        return [_doc_a_guia(d) for d in docs]

    async def obtener_guia(self, guia_id: str) -> GuiaDTO | None:
        doc = await self._guias.find_one({"_id": guia_id, "activo": True})
        return None if doc is None else _doc_a_guia(doc)

    # ---- Puerto publico: menus ----

    async def listar_menus(
        self,
        rango_edad: RangoEdad | None = None,
        tipo_comida: TipoComida | None = None,
    ) -> list[MenuDTO]:
        filtro: dict[str, Any] = {"activo": True}
        if rango_edad is not None:
            filtro["rango_edad"] = rango_edad.value
        if tipo_comida is not None:
            filtro["tipo_comida"] = tipo_comida.value
        cursor = self._menus.find(filtro)
        docs = await cursor.to_list(length=None)
        return [_doc_a_menu(d) for d in docs]

    async def obtener_menu(self, menu_id: str) -> MenuDTO | None:
        doc = await self._menus.find_one({"_id": menu_id, "activo": True})
        return None if doc is None else _doc_a_menu(doc)

    # ---- Puerto publico: especialistas ----

    async def listar_especialistas(self) -> list[EspecialistaDTO]:
        cursor = self._especialistas.find({"disponible": True})
        docs = await cursor.to_list(length=None)
        return [_doc_a_especialista(d) for d in docs]

    # ---- Puerto publico: solicitudes ----

    async def crear_solicitud_orientacion(
        self,
        tutor_id: str,
        perfil_id: str,
        especialista_id: str,
        mensaje: str,
    ) -> str:
        solicitud_id = str(uuid4())
        ahora = datetime.now(timezone.utc)
        await self._solicitudes.insert_one(
            {
                "_id": solicitud_id,
                "tutor_id": tutor_id,
                "perfil_id": perfil_id,
                "especialista_id": especialista_id,
                "mensaje": mensaje,
                "estado": "pendiente",
                "creado_en": ahora,
                "actualizado_en": ahora,
            }
        )
        return solicitud_id

    # ---- Metodos internos (uso del seed, no del puerto) ----

    async def insertar_guia(
        self,
        titulo: str,
        categoria: str,
        rango_edad: RangoEdad,
        contenido: str,
        habitos_clave: list[str],
    ) -> str:
        guia_id = str(uuid4())
        ahora = datetime.now(timezone.utc)
        await self._guias.insert_one(
            {
                "_id": guia_id,
                "titulo": titulo,
                "categoria": categoria,
                "rango_edad": rango_edad.value,
                "contenido": contenido,
                "habitos_clave": list(habitos_clave),
                "activo": True,
                "creado_en": ahora,
                "actualizado_en": ahora,
            }
        )
        return guia_id

    async def insertar_menu(
        self,
        titulo: str,
        rango_edad: RangoEdad,
        tipo_comida: TipoComida,
        platos: list[dict[str, Any]],
        recomendaciones: list[str],
    ) -> str:
        menu_id = str(uuid4())
        ahora = datetime.now(timezone.utc)
        await self._menus.insert_one(
            {
                "_id": menu_id,
                "titulo": titulo,
                "rango_edad": rango_edad.value,
                "tipo_comida": tipo_comida.value,
                "platos": platos,
                "recomendaciones": list(recomendaciones),
                "activo": True,
                "creado_en": ahora,
                "actualizado_en": ahora,
            }
        )
        return menu_id

    async def insertar_especialista(
        self,
        nombre_completo: str,
        rol: str,
        especialidad: str,
        experiencia_anios: int,
        biografia: str,
        contacto_email: str,
        disponible: bool = True,
    ) -> str:
        esp_id = str(uuid4())
        ahora = datetime.now(timezone.utc)
        await self._especialistas.insert_one(
            {
                "_id": esp_id,
                "nombre_completo": nombre_completo,
                "rol": rol,
                "especialidad": especialidad,
                "experiencia_anios": experiencia_anios,
                "biografia": biografia,
                "contacto_email": contacto_email,
                "disponible": disponible,
                "creado_en": ahora,
                "actualizado_en": ahora,
            }
        )
        return esp_id
