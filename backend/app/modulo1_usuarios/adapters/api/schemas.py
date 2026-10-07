from __future__ import annotations

from pydantic import BaseModel, Field

from app.modulo1_usuarios.domain.enums import NivelActividadFisica, Sexo


class PerfilInfantilCreateSchema(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=60)
    edad: int = Field(..., ge=6, le=14)
    sexo: Sexo
    peso_kg: float = Field(..., gt=0, le=200.0)
    estatura_cm: float = Field(..., gt=0, le=250.0)
    nivel_actividad_fisica: NivelActividadFisica
    habitos_alimenticios: str | None = Field(None, max_length=500)
    alergias: list[str] = Field(default_factory=list)
    objetivos: str | None = Field(None, max_length=500)


class PerfilInfantilUpdateSchema(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=60)
    edad: int | None = Field(None, ge=6, le=14)
    sexo: Sexo | None = None
    peso_kg: float | None = Field(None, gt=0, le=200.0)
    estatura_cm: float | None = Field(None, gt=0, le=250.0)
    nivel_actividad_fisica: NivelActividadFisica | None = None
    habitos_alimenticios: str | None = Field(None, max_length=500)
    alergias: list[str] | None = None
    objetivos: str | None = Field(None, max_length=500)


class PerfilInfantilResponseSchema(BaseModel):
    id: str
    tutor_id: str
    nombre: str
    edad: int
    sexo: Sexo
    peso_kg: float
    estatura_cm: float
    nivel_actividad_fisica: NivelActividadFisica
    habitos_alimenticios: str | None = None
    alergias: list[str] = []
    objetivos: str | None = None
