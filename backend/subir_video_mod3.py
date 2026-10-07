"""Carga administrativa: ejecutar desde backend con credenciales del equipo."""
import argparse
import asyncio
import json
from dataclasses import asdict
from pathlib import Path
from uuid import UUID, uuid4

from app.core.config import get_settings
from app.core.security import inicializar_firebase
from app.modulo3_ejercicios.adapters.storage.firebase_video_storage import FirebaseVideoStorage
from app.modulo3_ejercicios.ports.video_storage_port import (
    GrupoEdad, StorageNoDisponibleError, VideoYaExisteError,
)


def main():
    parser = argparse.ArgumentParser(description="Subir un MP4 educativo al bucket privado")
    parser.add_argument("archivo", type=Path)
    parser.add_argument("--grupo-edad", choices=[g.value for g in GrupoEdad], required=True)
    parser.add_argument("--video-id", type=UUID, default=None)
    args = parser.parse_args()
    try:
        settings = get_settings()
        inicializar_firebase()
        storage = FirebaseVideoStorage(settings.firebase_storage_bucket,
                                       settings.video_url_ttl_seconds)
        resultado = asyncio.run(storage.subir_video(
            args.archivo, GrupoEdad(args.grupo_edad), args.video_id or uuid4(),
        ))
    except (ValueError, RuntimeError, StorageNoDisponibleError, VideoYaExisteError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(json.dumps(asdict(resultado), default=str, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
