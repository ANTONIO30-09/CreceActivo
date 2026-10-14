"""Tests del filtrado por meta_id y 422 por fecha invalida (fix/progreso-meta)."""
from __future__ import annotations
from datetime import date, datetime, timezone
import pytest
from pydantic import ValidationError
from app.modulo3_ejercicios.adapters.api.schemas import MarcarMetaRequest
from app.modulo3_ejercicios.adapters.db.progreso_repository import ProgresoRepository


class _Col:
    def __init__(self, docs=None):
        self.docs = list(docs or [])
    async def find_one(self, q):
        for d in self.docs:
            if all(d.get(k) == v for k, v in q.items()):
                return d
        return None
    async def insert_one(self, doc):
        self.docs.append(doc)
    def count_documents(self, q):
        async def _run():
            n = 0
            for d in self.docs:
                if "perfil_id" in q and d.get("perfil_id") != q["perfil_id"]:
                    continue
                if "meta_id" in q and d.get("meta_id") != q["meta_id"]:
                    continue
                n += 1
            return n
        return _run()


def _meta(meta_id: str) -> dict:
    a = datetime.now(timezone.utc)
    return {"_id": meta_id, "perfil_id": "p1", "tutor_id": "t1",
            "titulo": "x", "descripcion": "", "objetivo_semanal": 5,
            "estado": "activa", "creado_en": a, "actualizado_en": a}


@pytest.mark.asyncio
async def test_completado_semana_filtra_por_meta_id():
    metas = _Col([_meta("m1")])
    registros = _Col([
        {"_id": "r0", "perfil_id": "p1", "tutor_id": "t1", "tipo": "rutina",
         "valor": 1, "meta_id": "m2", "fecha": datetime.now(timezone.utc),
         "creado_en": datetime.now(timezone.utc),
         "actualizado_en": datetime.now(timezone.utc)},
    ])
    repo = ProgresoRepository({"metas_familiares": metas,
                               "registros_actividad": registros})
    dto = await repo.marcar_meta("m1", date.today())
    assert dto is not None
    assert dto.completado_semana == 1, "solo debe contar el registro de m1"
    assert any(r.get("meta_id") == "m1" for r in registros.docs)


def test_marcar_meta_request_rechaza_fecha_invalida():
    with pytest.raises(ValidationError):
        MarcarMetaRequest(fecha="2024-13-45")
    with pytest.raises(ValidationError):
        MarcarMetaRequest(fecha="no-es-fecha")
