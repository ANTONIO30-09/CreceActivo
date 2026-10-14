"""Carga datos de prueba del Modulo 2 en MongoDB Atlas.

Uso:
    cd backend
    python seed_mod2.py

Requiere .env real en la raiz del repo (MONGODB_URI apuntando a Atlas).
Primero asegura las colecciones y luego inserta datos sinteticos.
"""
from __future__ import annotations

import asyncio
import sys

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import get_settings
from app.modulo2_nutricion.adapters.db import (
    NutricionRepository,
    asegurar_colecciones_modulo2,
)
from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida


async def cargar_datos() -> int:
    settings = get_settings()
    host = settings.mongodb_uri.split("@")[-1] if "@" in settings.mongodb_uri else settings.mongodb_uri
    print(f"Conectando a: {host}")
    print(f"Base de datos: {settings.mongodb_db_name}")
    print()

    client: AsyncIOMotorClient = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=8000,
    )
    try:
        db = client[settings.mongodb_db_name]

        # 1. Asegurar validadores e indices
        await asegurar_colecciones_modulo2(db)
        print("OK: colecciones aseguradas (validadores + indices)")

        repo = NutricionRepository(db)

        # 2. Guias
        guias = await _cargar_guias(repo)
        print(f"OK: {guias} guias insertadas")

        # 3. Menus
        menus = await _cargar_menus(repo)
        print(f"OK: {menus} menus insertados")

        # 4. Especialistas
        especialistas = await _cargar_especialistas(repo)
        print(f"OK: {especialistas} especialistas insertados")

        print()
        print("Datos sinteticos del Modulo 2 cargados correctamente.")
        return 0
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    finally:
        client.close()


async def _cargar_guias(repo: NutricionRepository) -> int:
    """Inserta guias de prueba. Devuelve cuantas inserto."""
    guias = [
        {
            "titulo": "Habitos saludables en casa",
            "categoria": "Habitos",
            "rango_edad": RangoEdad.DE_6_A_8,
            "contenido": (
                "Mantener horarios regulares de comida, dormir 9-10 horas "
                "y limitar pantallas a menos de 2 horas al dia."
            ),
            "habitos_clave": [
                "Desayunar todos los dias",
                "Dormir 9-10 horas",
                "Menos de 2 horas de pantalla",
            ],
        },
        {
            "titulo": "Meriendas escolares saludables",
            "categoria": "Meriendas",
            "rango_edad": RangoEdad.DE_9_A_11,
            "contenido": (
                "La merienda debe incluir una fruta, un cereal integral "
                "y una fuente de proteina. Evitar bebidas azucaradas."
            ),
            "habitos_clave": [
                "Fruta diaria",
                "Cereal integral",
                "Sin bebidas azucaradas",
            ],
        },
        {
            "titulo": "Alimentacion en la adolescencia temprana",
            "categoria": "Alimentacion",
            "rango_edad": RangoEdad.DE_12_A_14,
            "contenido": (
                "Aumentar el consumo de hierro y calcio por el crecimiento. "
                "Incluir vegetales de hoja verde y lacteos."
            ),
            "habitos_clave": [
                "Hierro y calcio diarios",
                "Vegetales de hoja verde",
                "Lacteos en el desayuno",
            ],
        },
    ]
    for g in guias:
        await repo.insertar_guia(
            titulo=g["titulo"],
            categoria=g["categoria"],
            rango_edad=g["rango_edad"],
            contenido=g["contenido"],
            habitos_clave=g["habitos_clave"],
        )
    return len(guias)


async def _cargar_menus(repo: NutricionRepository) -> int:
    """Inserta menus de prueba. Devuelve cuantos inserto."""
    menus = [
        {
            "titulo": "Desayuno energetico",
            "rango_edad": RangoEdad.DE_6_A_8,
            "tipo_comida": TipoComida.DESAYUNO,
            "platos": [
                {
                    "nombre": "Avena con platano",
                    "descripcion": "Avena cocida con leche y platano en rodajas",
                    "calorias_aprox": 250,
                    "ingredientes": ["Avena", "Leche", "Platano"],
                },
                {
                    "nombre": "Jugo de naranja natural",
                    "descripcion": "Jugo recien exprimido sin azucar anadida",
                    "calorias_aprox": 90,
                    "ingredientes": ["Naranja"],
                },
            ],
            "recomendaciones": [
                "Acompanar con un vaso de agua",
                "Evitar azucar anadida",
            ],
        },
        {
            "titulo": "Almuerzo balanceado",
            "rango_edad": RangoEdad.DE_9_A_11,
            "tipo_comida": TipoComida.ALMUERZO,
            "platos": [
                {
                    "nombre": "Pollo con arroz y verduras",
                    "descripcion": "Pechuga de pollo a la plancha con arroz y verduras al vapor",
                    "calorias_aprox": 420,
                    "ingredientes": ["Pollo", "Arroz", "Zanahoria", "Brocoli"],
                },
            ],
            "recomendaciones": [
                "Servir una porcion de fruta de postre",
            ],
        },
        {
            "titulo": "Merienda escolar",
            "rango_edad": RangoEdad.DE_6_A_8,
            "tipo_comida": TipoComida.MERIENDA,
            "platos": [
                {
                    "nombre": "Yogur con frutas",
                    "descripcion": "Yogur natural con fresas y arandanos",
                    "calorias_aprox": 150,
                    "ingredientes": ["Yogur", "Fresas", "Arandanos"],
                },
            ],
            "recomendaciones": [
                "Preferir yogur sin azucar anadida",
            ],
        },
    ]
    for m in menus:
        await repo.insertar_menu(
            titulo=m["titulo"],
            rango_edad=m["rango_edad"],
            tipo_comida=m["tipo_comida"],
            platos=m["platos"],
            recomendaciones=m["recomendaciones"],
        )
    return len(menus)


async def _cargar_especialistas(repo: NutricionRepository) -> int:
    """Inserta especialistas de prueba. Devuelve cuantos inserto."""
    especialistas = [
        {
            "nombre_completo": "Dra. Laura Gomez",
            "rol": "Nutricionista",
            "especialidad": "Nutricion Infantil",
            "experiencia_anios": 7,
            "biografia": "Especialista en habitos saludables para ninos de 6 a 14 anos.",
            "contacto_email": "laura.gomez@example.com",
        },
        {
            "nombre_completo": "Dr. Carlos Rojas",
            "rol": "Pediatra",
            "especialidad": "Pediatria general",
            "experiencia_anios": 12,
            "biografia": "Pediatra con enfoque en prevencion de obesidad infantil.",
            "contacto_email": "carlos.rojas@example.com",
        },
        {
            "nombre_completo": "Prof. Maria Lopez",
            "rol": "Entrenador",
            "especialidad": "Actividad fisica infantil",
            "experiencia_anios": 5,
            "biografia": "Entrenadora certificada en ejercicio para ninos y adolescentes.",
            "contacto_email": "maria.lopez@example.com",
        },
    ]
    for e in especialistas:
        await repo.insertar_especialista(
            nombre_completo=e["nombre_completo"],
            rol=e["rol"],
            especialidad=e["especialidad"],
            experiencia_anios=e["experiencia_anios"],
            biografia=e["biografia"],
            contacto_email=e["contacto_email"],
            disponible=True,
        )
    return len(especialistas)


if __name__ == "__main__":
    sys.exit(asyncio.run(cargar_datos()))
