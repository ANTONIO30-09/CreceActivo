"""Entidad de dominio PerfilInfantil (Modulo 1).

Reglas de negocio puras: sin dependencias de FastAPI, MongoDB ni Firebase.
Las invariantes se validan al construir la entidad para fallar temprano y
evitar persistir datos invalidos.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .enums import NivelActividadFisica, Sexo

__all__ = [
    "PerfilInfantil",
    "PerfilInfantilInvalido",
    "EDAD_MINIMA",
    "EDAD_MAXIMA",
    "NOMBRE_MAX_LEN",
    "HABITOS_MAX_LEN",
    "OBJETIVOS_MAX_LEN",
    "ALERGIA_MAX_LEN",
    "PESO_MAX_KG",
    "ESTATURA_MAX_CM",
]

EDAD_MINIMA: int = 6
EDAD_MAXIMA: int = 14
NOMBRE_MAX_LEN: int = 60
HABITOS_MAX_LEN: int = 500
OBJETIVOS_MAX_LEN: int = 500
ALERGIA_MAX_LEN: int = 50
PESO_MAX_KG: float = 200.0
ESTATURA_MAX_CM: float = 250.0


class PerfilInfantilInvalido(ValueError):
    """Se lanza cuando los datos violan una invariante de PerfilInfantil."""


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class PerfilInfantil:
    """Entidad de dominio de un perfil infantil.

    Inmutable. Para "modificar" se construye una nueva instancia.
    """

    id: str
    tutor_id: str
    nombre: str
    edad: int
    sexo: Sexo
    peso_kg: float
    estatura_cm: float
    nivel_actividad_fisica: NivelActividadFisica
    habitos_alimenticios: str | None = None
    alergias: tuple[str, ...] = ()
    objetivos: str | None = None
    activo: bool = True
    creado_en: datetime = field(default_factory=_utc_now)
    actualizado_en: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        _validar_id(self.id, "id")
        _validar_id(self.tutor_id, "tutor_id")

        object.__setattr__(
            self,
            "nombre",
            _validar_texto_obligatorio(self.nombre, "nombre", NOMBRE_MAX_LEN),
        )
        _validar_edad(self.edad)
        _validar_enum(self.sexo, Sexo, "sexo")

        object.__setattr__(
            self,
            "peso_kg",
            _validar_numero_rango(
                self.peso_kg, "peso_kg", minimo_exclusivo=0.0, maximo=PESO_MAX_KG
            ),
        )
        object.__setattr__(
            self,
            "estatura_cm",
            _validar_numero_rango(
                self.estatura_cm,
                "estatura_cm",
                minimo_exclusivo=0.0,
                maximo=ESTATURA_MAX_CM,
            ),
        )

        _validar_enum(
            self.nivel_actividad_fisica,
            NivelActividadFisica,
            "nivel_actividad_fisica",
        )

        object.__setattr__(
            self,
            "habitos_alimenticios",
            _validar_texto_opcional(
                self.habitos_alimenticios, "habitos_alimenticios", HABITOS_MAX_LEN
            ),
        )
        object.__setattr__(self, "alergias", _validar_alergias(self.alergias))
        object.__setattr__(
            self,
            "objetivos",
            _validar_texto_opcional(self.objetivos, "objetivos", OBJETIVOS_MAX_LEN),
        )

        if not isinstance(self.activo, bool):
            raise PerfilInfantilInvalido("activo debe ser booleano")
        _validar_datetime(self.creado_en, "creado_en")
        _validar_datetime(self.actualizado_en, "actualizado_en")

    @classmethod
    def crear(
        cls,
        *,
        tutor_id: str,
        nombre: str,
        edad: int,
        sexo: Sexo,
        peso_kg: float,
        estatura_cm: float,
        nivel_actividad_fisica: NivelActividadFisica,
        habitos_alimenticios: str | None = None,
        alergias: list[str] | tuple[str, ...] | None = None,
        objetivos: str | None = None,
    ) -> "PerfilInfantil":
        """Fabrica para nuevos perfiles: genera id, timestamps y activo=True."""
        ahora = _utc_now()
        return cls(
            id=str(uuid4()),
            tutor_id=tutor_id,
            nombre=nombre,
            edad=edad,
            sexo=sexo,
            peso_kg=peso_kg,
            estatura_cm=estatura_cm,
            nivel_actividad_fisica=nivel_actividad_fisica,
            habitos_alimenticios=habitos_alimenticios,
            alergias=tuple(alergias) if alergias else (),
            objetivos=objetivos,
            activo=True,
            creado_en=ahora,
            actualizado_en=ahora,
        )


# ---------- helpers de validacion ----------


def _validar_id(valor: object, campo: str) -> None:
    if not isinstance(valor, str) or not valor.strip():
        raise PerfilInfantilInvalido(f"{campo} es obligatorio y no puede estar vacio")


def _validar_texto_obligatorio(valor: object, campo: str, max_len: int) -> str:
    if not isinstance(valor, str):
        raise PerfilInfantilInvalido(f"{campo} debe ser texto")
    limpio = valor.strip()
    if not limpio:
        raise PerfilInfantilInvalido(f"{campo} es obligatorio")
    if len(limpio) > max_len:
        raise PerfilInfantilInvalido(
            f"{campo} no puede superar {max_len} caracteres"
        )
    return limpio


def _validar_texto_opcional(valor: object, campo: str, max_len: int) -> str | None:
    if valor is None:
        return None
    if not isinstance(valor, str):
        raise PerfilInfantilInvalido(f"{campo} debe ser texto o None")
    limpio = valor.strip()
    if not limpio:
        return None
    if len(limpio) > max_len:
        raise PerfilInfantilInvalido(
            f"{campo} no puede superar {max_len} caracteres"
        )
    return limpio


def _validar_edad(edad: object) -> None:
    if isinstance(edad, bool) or not isinstance(edad, int):
        raise PerfilInfantilInvalido("edad debe ser un entero")
    if not (EDAD_MINIMA <= edad <= EDAD_MAXIMA):
        raise PerfilInfantilInvalido(
            f"edad debe estar entre {EDAD_MINIMA} y {EDAD_MAXIMA} anios"
        )


def _validar_enum(valor: object, tipo: type, campo: str) -> None:
    if not isinstance(valor, tipo):
        raise PerfilInfantilInvalido(f"{campo} debe ser un valor de {tipo.__name__}")


def _validar_numero_rango(
    valor: object, campo: str, *, minimo_exclusivo: float, maximo: float
) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise PerfilInfantilInvalido(f"{campo} debe ser numerico")
    numero = float(valor)
    if not (minimo_exclusivo < numero <= maximo):
        raise PerfilInfantilInvalido(
            f"{campo} debe ser mayor a {minimo_exclusivo} y menor o igual a {maximo}"
        )
    return numero


def _validar_alergias(valor: object) -> tuple[str, ...]:
    if not isinstance(valor, tuple):
        raise PerfilInfantilInvalido("alergias debe ser una tupla de strings")
    limpias: list[str] = []
    for item in valor:
        if not isinstance(item, str):
            raise PerfilInfantilInvalido("cada alergia debe ser texto")
        limpia = item.strip()
        if not limpia:
            raise PerfilInfantilInvalido("las alergias no pueden estar vacias")
        if len(limpia) > ALERGIA_MAX_LEN:
            raise PerfilInfantilInvalido(
                f"cada alergia no puede superar {ALERGIA_MAX_LEN} caracteres"
            )
        limpias.append(limpia)
    return tuple(limpias)


def _validar_datetime(valor: object, campo: str) -> None:
    if not isinstance(valor, datetime):
        raise PerfilInfantilInvalido(f"{campo} debe ser datetime")
    if valor.tzinfo is None:
        raise PerfilInfantilInvalido(f"{campo} debe incluir zona horaria (UTC)")
