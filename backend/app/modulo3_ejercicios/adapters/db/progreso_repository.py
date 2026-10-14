"""Repositorio Mongo del Modulo 3. Implementa ProgresoPort."""
from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any

from app.modulo3_ejercicios.domain.enums import EstadoMeta, TipoActividad
from app.modulo3_ejercicios.domain.entidades import (
    MetaFamiliar,
    RegistroActividad,
    ahora_utc,
    nuevo_id,
)
from app.modulo3_ejercicios.domain.reglas import (
    evaluar_insignias,
    mejor_racha,
    porcentaje_meta,
    racha_actual,
    semana_actual,
)
from app.modulo3_ejercicios.ports.dto import (
    InsigniaDTO,
    MetaDTO,
    ProgresoDTO,
    RegistroDTO,
)

from .validadores import COLLECTION_METAS, COLLECTION_REGISTROS

__all__ = ["ProgresoRepository"]


def _a_utc(valor: datetime | None) -> datetime:
    if valor is None:
        return ahora_utc()
    if valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor


def _a_date(valor: Any) -> date:
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    return date.fromisoformat(str(valor))


def _doc_a_registro(doc: dict[str, Any]) -> RegistroActividad:
    return RegistroActividad(
        id=doc["_id"],
        perfil_id=doc["perfil_id"],
        tutor_id=doc["tutor_id"],
        tipo=TipoActividad(doc["tipo"]),
        valor=int(doc["valor"]),
        fecha=_a_date(doc["fecha"]),
        creado_en=_a_utc(doc.get("creado_en")),
        meta_id=doc.get("meta_id"),
    )


def _doc_a_meta(doc: dict[str, Any]) -> MetaFamiliar:
    return MetaFamiliar(
        id=doc["_id"],
        perfil_id=doc["perfil_id"],
        tutor_id=doc["tutor_id"],
        titulo=doc["titulo"],
        descripcion=doc.get("descripcion") or "",
        objetivo_semanal=int(doc["objetivo_semanal"]),
        estado=EstadoMeta(doc["estado"]),
        creado_en=_a_utc(doc.get("creado_en")),
    )


def _registro_a_dto(r: RegistroActividad) -> RegistroDTO:
    return RegistroDTO(
        id=r.id, perfil_id=r.perfil_id, tutor_id=r.tutor_id,
        tipo=r.tipo, valor=r.valor, fecha=r.fecha,
    )


class ProgresoRepository:
    """Acceso a las colecciones de progreso del Modulo 3."""

    def __init__(self, db: Any) -> None:
        self._registros = db[COLLECTION_REGISTROS]
        self._metas = db[COLLECTION_METAS]

    # ---- Registros ----

    async def registrar_actividad(
        self, perfil_id: str, tutor_id: str,
        tipo: TipoActividad, valor: int,
    ) -> RegistroDTO:
        hoy = date.today()
        ahora = ahora_utc()
        nuevo = RegistroActividad(
            id=nuevo_id(),
            perfil_id=perfil_id,
            tutor_id=tutor_id,
            tipo=tipo,
            valor=valor,
            fecha=hoy,
            creado_en=ahora,
        )
        doc = {
            "_id": nuevo.id,
            "perfil_id": nuevo.perfil_id,
            "tutor_id": nuevo.tutor_id,
            "tipo": nuevo.tipo.value,
            "valor": nuevo.valor,
            "fecha": datetime.combine(nuevo.fecha, datetime.min.time()).replace(tzinfo=timezone.utc),
            "creado_en": nuevo.creado_en,
            "actualizado_en": nuevo.creado_en,
        }
        await self._registros.insert_one(doc)
        return _registro_a_dto(nuevo)

    async def listar_registros(self, perfil_id: str) -> list[RegistroDTO]:
        cursor = self._registros.find({"perfil_id": perfil_id})
        docs = await cursor.to_list(length=None)
        return [_registro_a_dto(_doc_a_registro(d)) for d in docs]

    # ---- Metas ----

    async def _completado_semana(self, meta_id: str, perfil_id: str) -> int:
        """Cuenta registros de la meta en la semana actual."""
        lunes, domingo = semana_actual()
        inicio = datetime.combine(lunes, datetime.min.time()).replace(tzinfo=timezone.utc)
        fin = datetime.combine(domingo, datetime.max.time()).replace(tzinfo=timezone.utc)
        total = await self._registros.count_documents({
            "perfil_id": perfil_id,
            "meta_id": meta_id,
            "fecha": {"$gte": inicio, "$lte": fin},
        })
        return total

    async def crear_meta(
        self, perfil_id: str, tutor_id: str, titulo: str,
        descripcion: str, objetivo_semanal: int,
    ) -> MetaDTO:
        nueva = MetaFamiliar(
            id=nuevo_id(), perfil_id=perfil_id, tutor_id=tutor_id,
            titulo=titulo, descripcion=descripcion,
            objetivo_semanal=objetivo_semanal,
            estado=EstadoMeta.ACTIVA, creado_en=ahora_utc(),
        )
        doc = {
            "_id": nueva.id,
            "perfil_id": nueva.perfil_id,
            "tutor_id": nueva.tutor_id,
            "titulo": nueva.titulo,
            "descripcion": nueva.descripcion,
            "objetivo_semanal": nueva.objetivo_semanal,
            "estado": nueva.estado.value,
            "creado_en": nueva.creado_en,
            "actualizado_en": nueva.creado_en,
        }
        await self._metas.insert_one(doc)
        return MetaDTO(
            id=nueva.id, perfil_id=nueva.perfil_id, tutor_id=nueva.tutor_id,
            titulo=nueva.titulo, descripcion=nueva.descripcion,
            objetivo_semanal=nueva.objetivo_semanal, estado=nueva.estado,
            completado_semana=0, porcentaje=0,
        )

    async def listar_metas(self, perfil_id: str) -> list[MetaDTO]:
        cursor = self._metas.find({"perfil_id": perfil_id, "estado": EstadoMeta.ACTIVA.value})
        docs = await cursor.to_list(length=None)
        resultado: list[MetaDTO] = []
        for d in docs:
            meta = _doc_a_meta(d)
            completado = await self._completado_semana(meta.id, meta.perfil_id)
            resultado.append(MetaDTO(
                id=meta.id, perfil_id=meta.perfil_id, tutor_id=meta.tutor_id,
                titulo=meta.titulo, descripcion=meta.descripcion,
                objetivo_semanal=meta.objetivo_semanal, estado=meta.estado,
                completado_semana=completado,
                porcentaje=porcentaje_meta(completado, meta.objetivo_semanal),
            ))
        return resultado

    async def obtener_meta(self, meta_id: str):
        """Uso interno: meta activa (entidad) o None. Sirve para comprobar al tutor."""
        doc = await self._metas.find_one(
            {"_id": meta_id, "estado": EstadoMeta.ACTIVA.value}
        )
        return None if doc is None else _doc_a_meta(doc)

    async def marcar_meta(self, meta_id: str, fecha: date) -> MetaDTO | None:
        doc = await self._metas.find_one({"_id": meta_id, "estado": EstadoMeta.ACTIVA.value})
        if doc is None:
            return None
        meta = _doc_a_meta(doc)

        registro_id = nuevo_id()
        ahora = ahora_utc()
        await self._registros.insert_one({
            "_id": registro_id,
            "perfil_id": meta.perfil_id,
            "tutor_id": meta.tutor_id,
            "tipo": TipoActividad.RUTINA.value,
            "valor": 1,
            "meta_id": meta.id,
            "fecha": datetime.combine(fecha, datetime.min.time()).replace(tzinfo=timezone.utc),
            "creado_en": ahora,
            "actualizado_en": ahora,
        })

        completado = await self._completado_semana(meta.id, meta.perfil_id)
        return MetaDTO(
            id=meta.id, perfil_id=meta.perfil_id, tutor_id=meta.tutor_id,
            titulo=meta.titulo, descripcion=meta.descripcion,
            objetivo_semanal=meta.objetivo_semanal, estado=meta.estado,
            completado_semana=completado,
            porcentaje=porcentaje_meta(completado, meta.objetivo_semanal),
        )

    async def archivar_meta(self, meta_id: str) -> bool:
        res = await self._metas.update_one(
            {"_id": meta_id},
            {"$set": {"estado": EstadoMeta.ARCHIVADA.value, "actualizado_en": ahora_utc()}},
        )
        return res.modified_count > 0

    # ---- Progreso agregado ----

    async def obtener_progreso(self, perfil_id: str) -> ProgresoDTO:
        cursor = self._registros.find({"perfil_id": perfil_id})
        docs = await cursor.to_list(length=None)
        registros = [_doc_a_registro(d) for d in docs]

        fechas = [r.fecha for r in registros]
        total = len(registros)
        racha = racha_actual(fechas)
        mejor = mejor_racha(fechas)

        # Insignias ganadas por variedad de tipos en un mismo dia
        por_dia: dict[date, set[str]] = {}
        for r in registros:
            por_dia.setdefault(r.fecha, set()).add(r.tipo.value)
        variedad = max((len(v) for v in por_dia.values()), default=0)

        nuevas = evaluar_insignias(
            total=total, mejor=mejor, variedad=variedad, ya_ganadas=set(),
        )
        ganadas = tuple(i["id"] for i in nuevas)

        return ProgresoDTO(
            perfil_id=perfil_id,
            racha_actual=racha,
            mejor_racha=mejor,
            total_registros=total,
            insignias_ganadas=ganadas,
        )

    async def catalogo_insignias(self) -> list[InsigniaDTO]:
        from app.modulo3_ejercicios.domain.reglas import INSIGNIAS
        return [
            InsigniaDTO(id=i["id"], nombre=i["nombre"], tipo=i["tipo"], meta=i["meta"])
            for i in INSIGNIAS
        ]
