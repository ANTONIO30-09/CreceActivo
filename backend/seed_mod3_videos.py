"""Carga metadatos de videos del Modulo 3 en MongoDB Atlas.

Uso:
    cd backend
    python seed_mod3_videos.py

Requiere el .env real en la raiz del repo.
Idempotente: borra y vuelve a insertar.
"""
from __future__ import annotations

import asyncio
import sys
from datetime import datetime, timezone
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings
from app.modulo3_ejercicios.adapters.db.validadores import (
    COLLECTION_VIDEOS_META,
    asegurar_colecciones_modulo3,
)


VIDEOS = [
    # ---- 6-8 ----
    dict(titulo="Saltos de rana", grupo_edad="6-8", duracion_seg=180, dificultad="facil",
         descripcion="Serie corta de saltos imitando a una rana. Ideal para empezar el dia con energia y coordinacion.",
         materiales=["Espacio libre", "Ropa comoda"],
         recomendaciones_seguridad=["Calentar 2 minutos antes", "Superficie antideslizante", "Hacer pausas si se cansa"]),
    dict(titulo="Bailar congelados", grupo_edad="6-8", duracion_seg=300, dificultad="facil",
         descripcion="Juego de bailar y congelarse cuando la musica para. Mejora equilibrio y atencion.",
         materiales=["Musica", "Parlante"],
         recomendaciones_seguridad=["Volumen moderado", "Piso sin obstaculos"]),
    dict(titulo="Circuito de cojines", grupo_edad="6-8", duracion_seg=420, dificultad="media",
         descripcion="Armar un circuito con cojines para saltar, gatear y esquivar. Desarrolla motricidad gruesa.",
         materiales=["Cojines", "Sillas", "Cuerda"],
         recomendaciones_seguridad=["Quitar objetos fragiles", "Adulto presente"]),
    # ---- 9-11 ----
    dict(titulo="Rutina de abdominales infantiles", grupo_edad="9-11", duracion_seg=480, dificultad="media",
         descripcion="Serie guiada de ejercicios de core adaptados para ninos. Mejora postura y fuerza.",
         materiales=["Colchoneta"],
         recomendaciones_seguridad=["No forzar el cuello", "Pausas cada 30 segundos"]),
    dict(titulo="Zumba kids", grupo_edad="9-11", duracion_seg=900, dificultad="media",
         descripcion="Coreografia sencilla con ritmos latinos. Trabaja resistencia cardiovascular.",
         materiales=["Musica", "Espacio amplio"],
         recomendaciones_seguridad=["Hidratarse a mitad", "Calzado deportivo"]),
    dict(titulo="Saltar la cuerda basico", grupo_edad="9-11", duracion_seg=600, dificultad="media",
         descripcion="Progresion de saltos: individual, pies juntos, alternado. Mejora coordinacion y ritmo.",
         materiales=["Cuerda", "Espacio libre"],
         recomendaciones_seguridad=["Techo alto", "Piso firme"]),
    # ---- 12-14 ----
    dict(titulo="Yoga para adolescentes", grupo_edad="12-14", duracion_seg=1200, dificultad="media",
         descripcion="Secuencia de posturas basicas de yoga para flexibilidad y relajacion.",
         materiales=["Mat de yoga", "Ropa comoda"],
         recomendaciones_seguridad=["No forzar posturas", "Respirar profundo"]),
    dict(titulo="HIIT adaptado", grupo_edad="12-14", duracion_seg=900, dificultad="dificil",
         descripcion="Intervalos de alta intensidad con ejercicios adaptados. Mejora resistencia y fuerza.",
         materiales=["Colchoneta", "Cronometro"],
         recomendaciones_seguridad=["Calentamiento 5 min", "Hidratarse", "Parar si hay mareo"]),
    dict(titulo="Fuerza con peso corporal", grupo_edad="12-14", duracion_seg=1080, dificultad="dificil",
         descripcion="Sentadillas, planchas y flexiones adaptadas. Desarrolla fuerza general sin pesas.",
         materiales=["Colchoneta", "Silla"],
         recomendaciones_seguridad=["Tecnica antes que repeticiones", "Descanso entre series"]),
]


async def cargar() -> int:
    settings = get_settings()
    host = settings.mongodb_uri.split("@")[-1] if "@" in settings.mongodb_uri else settings.mongodb_uri
    print(f"Conectando a: {host}")
    print(f"Base de datos: {settings.mongodb_db_name}\n")

    client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=8000)
    try:
        db = client[settings.mongodb_db_name]
        await asegurar_colecciones_modulo3(db)

        r = await db[COLLECTION_VIDEOS_META].delete_many({})
        print(f"OK: borrados {r.deleted_count} de {COLLECTION_VIDEOS_META}")

        ahora = datetime.now(timezone.utc)
        for v in VIDEOS:
            await db[COLLECTION_VIDEOS_META].insert_one({
                "_id": str(uuid4()),
                "titulo": v["titulo"],
                "descripcion": v["descripcion"],
                "grupo_edad": v["grupo_edad"],
                "duracion_seg": v["duracion_seg"],
                "dificultad": v["dificultad"],
                "materiales": list(v["materiales"]),
                "recomendaciones_seguridad": list(v["recomendaciones_seguridad"]),
                "activo": True,
                "creado_en": ahora,
            })
        print(f"OK: {len(VIDEOS)} videos insertados")
        print("\nCatalogo del Modulo 3 cargado correctamente.")
        return 0
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(cargar()))
