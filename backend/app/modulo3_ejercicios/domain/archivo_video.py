"""Identidad y validaciones de archivos; sin dependencias de Firebase."""
from enum import Enum
from pathlib import Path
from uuid import UUID

MAX_VIDEO_BYTES = 100 * 1024 * 1024


class GrupoEdad(str, Enum):
    INFANTIL = "6-8"
    INTERMEDIO = "9-11"
    MAYOR = "12-14"


def ruta_video(grupo: GrupoEdad, video_id: UUID) -> str:
    return f"modulo3/videos/{GrupoEdad(grupo).value}/{UUID(str(video_id))}.mp4"


def validar_video(archivo: Path) -> None:
    if not archivo.is_file():
        raise ValueError("El archivo de video no existe")
    if archivo.suffix.lower() != ".mp4":
        raise ValueError("Solo se admiten archivos .mp4")
    if not 12 <= archivo.stat().st_size <= MAX_VIDEO_BYTES:
        raise ValueError("El video debe tener entre 12 bytes y 100 MiB")
    with archivo.open("rb") as stream:
        cabecera = stream.read(12)
    if cabecera[4:8] != b"ftyp":
        raise ValueError("El archivo no tiene la cabecera MP4 esperada")
