import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

async def cargar_datos_prueba():
    if not MONGODB_URI or "usuario:password" in MONGODB_URI:
        print("ATENCIÓN: Configura una URI real de MongoDB Atlas en el archivo .env antes de ejecutar este script.")
        return

    client = AsyncIOMotorClient(MONGODB_URI)
    db = client.get_database("creceactivo")

    # Datos de prueba ficticios
    menus_sample = [
        {
            "titulo": "Menú Energético Infantil",
            "rango_edad": "6-8 años",
            "tipo_comida": "Desayuno",
            "platos": [
                {"nombre": "Avena con plátano", "descripcion": "Avena cocida con leche y frutas", "calorias_aprox": 250, "ingredientes": ["Avena", "Leche", "Plátano"]}
            ],
            "recomendaciones": ["Acompañar con un vaso de agua"]
        }
    ]

    especialistas_sample = [
        {
            "nombre_completo": "Dra. Laura Gómez",
            "rol": "Nutricionista",
            "especialidad": "Nutrición Infantil",
            "experiencia_anios": 7,
            "biografia": "Especialista en hábitos saludables para niños de 6 a 14 años.",
            "contacto_email": "laura.gomez@example.com",
            "disponible": True
        }
    ]

    await db.menus.insert_many(menus_sample)
    await db.specialists.insert_many(especialistas_sample)
    print("Datos sintéticos del Módulo 2 insertados correctamente en MongoDB Atlas.")

if __name__ == "__main__":
    asyncio.run(cargar_datos_prueba())
