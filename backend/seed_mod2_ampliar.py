"""Amplia y reemplaza los datos del Modulo 2 con un catalogo completo.

Uso:
    cd backend
    python seed_mod2_ampliar.py

Borra guias/menus/especialistas y vuelve a insertar 9+9+6 elementos.
Idempotente: se puede correr varias veces.
Requiere el .env real en la raiz del repo.
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
from app.modulo2_nutricion.adapters.db.validadores import (
    COLLECTION_ESPECIALISTAS,
    COLLECTION_GUIAS,
    COLLECTION_MENUS,
)
from app.modulo2_nutricion.domain.enums import RangoEdad, TipoComida


GUIAS = [
    # ---- 6-8 ----
    dict(titulo="Habitos saludables en casa", categoria="Habitos", rango_edad=RangoEdad.DE_6_A_8,
         contenido="Horarios regulares de comida, 9-10 horas de sueno y menos de 2 horas de pantalla al dia. Rutinas estables para que el cuerpo se acostumbre.",
         habitos_clave=["Desayunar todos los dias", "Dormir 9-10 horas", "Menos de 2 horas de pantalla"]),
    dict(titulo="Meriendas escolares saludables", categoria="Meriendas", rango_edad=RangoEdad.DE_6_A_8,
         contenido="Una merienda completa lleva fruta, un cereal integral y una proteina. Evita bebidas azucaradas y snacks ultraprocesados.",
         habitos_clave=["Fruta diaria", "Cereal integral", "Sin bebidas azucaradas"]),
    dict(titulo="Primeros habitos de alimentacion", categoria="Alimentacion", rango_edad=RangoEdad.DE_6_A_8,
         contenido="Ofrecer variedad de colores en el plato, dejar que el nino elija entre opciones saludables y no usar la comida como premio o castigo.",
         habitos_clave=["Plato de colores", "Sin premios con comida", "Probar alimentos nuevos"]),
    # ---- 9-11 ----
    dict(titulo="Rutinas activas en familia", categoria="Habitos", rango_edad=RangoEdad.DE_9_A_11,
         contenido="Caminar juntos, tareas del hogar activas y limite de pantallas. El ejemplo de los padres es la mejor guia.",
         habitos_clave=["Caminata familiar", "Tareas activas", "Ejemplo de los adultos"]),
    dict(titulo="Meriendas despues del colegio", categoria="Meriendas", rango_edad=RangoEdad.DE_9_A_11,
         contenido="A esta edad la merienda puede incluir fruto seco sin sal, yogur natural y fruta entera. Racionar las golosinas a un dia a la semana.",
         habitos_clave=["Fruto seco sin sal", "Yogur natural", "Golosinas 1 vez por semana"]),
    dict(titulo="Alimentacion en crecimiento", categoria="Alimentacion", rango_edad=RangoEdad.DE_9_A_11,
         contenido="Aumentar el consumo de hierro y calcio por el crecimiento. Incluir legumbres 2-3 veces por semana y lacteos en el desayuno.",
         habitos_clave=["Legumbres 2-3 veces/semana", "Lacteos en el desayuno", "Hierro con vitamina C"]),
    # ---- 12-14 ----
    dict(titulo="Autonomia y buenos habitos", categoria="Habitos", rango_edad=RangoEdad.DE_12_A_14,
         contenido="A esta edad conviene acordar reglas juntos: hora de dormir, uso del celular y actividad fisica. La negociacion funciona mejor que la imposicion.",
         habitos_clave=["Acuerdos familiares", "Sueno regular", "Actividad fisica diaria"]),
    dict(titulo="Meriendas para adolescentes", categoria="Meriendas", rango_edad=RangoEdad.DE_12_A_14,
         contenido="Combinar carbohidrato integral, proteina y fruta para mantener energia estable. Evitar bebidas energeticas.",
         habitos_clave=["Sin bebidas energeticas", "Combinacion completa", "Fruta entera"]),
    dict(titulo="Alimentacion en la adolescencia temprana", categoria="Alimentacion", rango_edad=RangoEdad.DE_12_A_14,
         contenido="Aumentar hierro y calcio por el estiron. Incluir vegetales de hoja verde, lacteos y carnes magras o legumbres.",
         habitos_clave=["Hierro y calcio diarios", "Vegetales de hoja verde", "Lacteos en el desayuno"]),
]


MENUS = [
    # ---- 6-8 ----
    dict(titulo="Desayuno energetico", rango_edad=RangoEdad.DE_6_A_8, tipo_comida=TipoComida.DESAYUNO,
         platos=[
             dict(nombre="Avena con platano", descripcion="Avena cocida con leche y platano en rodajas", calorias_aprox=250, ingredientes=["Avena", "Leche", "Platano"]),
             dict(nombre="Jugo de naranja natural", descripcion="Jugo recien exprimido sin azucar anadida", calorias_aprox=90, ingredientes=["Naranja"]),
         ],
         recomendaciones=["Acompanar con un vaso de agua", "Evitar azucar anadida"]),
    dict(titulo="Merienda escolar", rango_edad=RangoEdad.DE_6_A_8, tipo_comida=TipoComida.MERIENDA,
         platos=[
             dict(nombre="Yogur con frutas", descripcion="Yogur natural con fresas y arandanos", calorias_aprox=150, ingredientes=["Yogur", "Fresas", "Arandanos"]),
         ],
         recomendaciones=["Preferir yogur sin azucar anadida"]),
    dict(titulo="Almuerzo infantil", rango_edad=RangoEdad.DE_6_A_8, tipo_comida=TipoComida.ALMUERZO,
         platos=[
             dict(nombre="Pollo con pure y zanahoria", descripcion="Pechuga de pollo con pure de papa y zanahoria cocida", calorias_aprox=380, ingredientes=["Pollo", "Papa", "Zanahoria"]),
             dict(nombre="Ensalada de tomate", descripcion="Tomate en rodajas con un hilo de aceite de oliva", calorias_aprox=60, ingredientes=["Tomate", "Aceite de oliva"]),
         ],
         recomendaciones=["Servir agua en lugar de refrescos"]),
    # ---- 9-11 ----
    dict(titulo="Desayuno balanceado", rango_edad=RangoEdad.DE_9_A_11, tipo_comida=TipoComida.DESAYUNO,
         platos=[
             dict(nombre="Pan integral con huevo", descripcion="Pan integral con huevo revuelto y palta", calorias_aprox=320, ingredientes=["Pan integral", "Huevo", "Palta"]),
             dict(nombre="Leche con cacao sin azucar", descripcion="Leche tibia con cacao amargo", calorias_aprox=140, ingredientes=["Leche", "Cacao amargo"]),
         ],
         recomendaciones=["Incluir una fruta de estacion"]),
    dict(titulo="Almuerzo balanceado", rango_edad=RangoEdad.DE_9_A_11, tipo_comida=TipoComida.ALMUERZO,
         platos=[
             dict(nombre="Pollo con arroz y verduras", descripcion="Pechuga de pollo a la plancha con arroz y verduras al vapor", calorias_aprox=420, ingredientes=["Pollo", "Arroz", "Zanahoria", "Brocoli"]),
         ],
         recomendaciones=["Servir una porcion de fruta de postre"]),
    dict(titulo="Merienda de media tarde", rango_edad=RangoEdad.DE_9_A_11, tipo_comida=TipoComida.MERIENDA,
         platos=[
             dict(nombre="Tostada con queso fresco", descripcion="Pan integral con queso fresco y tomate", calorias_aprox=210, ingredientes=["Pan integral", "Queso fresco", "Tomate"]),
         ],
         recomendaciones=["Acompanar con fruta entera, no jugo"]),
    # ---- 12-14 ----
    dict(titulo="Desayuno para crecer", rango_edad=RangoEdad.DE_12_A_14, tipo_comida=TipoComida.DESAYUNO,
         platos=[
             dict(nombre="Bowl de yogur con granola y frutos rojos", descripcion="Yogur natural, granola sin azucar y frutos rojos", calorias_aprox=340, ingredientes=["Yogur", "Granola", "Frutos rojos"]),
         ],
         recomendaciones=["Evitar cereales azucarados de caja"]),
    dict(titulo="Almuerzo completo", rango_edad=RangoEdad.DE_12_A_14, tipo_comida=TipoComida.ALMUERZO,
         platos=[
             dict(nombre="Lentejas guisadas con arroz", descripcion="Lentejas con verduras y arroz integral", calorias_aprox=450, ingredientes=["Lentejas", "Arroz integral", "Cebolla", "Zanahoria"]),
             dict(nombre="Ensalada verde", descripcion="Lechuga, tomate y pepino con aceite de oliva", calorias_aprox=80, ingredientes=["Lechuga", "Tomate", "Pepino", "Aceite de oliva"]),
         ],
         recomendaciones=["Incluir una fruta citrica de postre para absorber el hierro"]),
    dict(titulo="Merienda post-entreno", rango_edad=RangoEdad.DE_12_A_14, tipo_comida=TipoComida.MERIENDA,
         platos=[
             dict(nombre="Sandwich de pavo", descripcion="Pan integral con pavo y lechuga", calorias_aprox=280, ingredientes=["Pan integral", "Pavo", "Lechuga"]),
             dict(nombre="Batido de frutas", descripcion="Leche con banana y fresas", calorias_aprox=180, ingredientes=["Leche", "Banana", "Fresas"]),
         ],
         recomendaciones=["Consumir dentro de la hora posterior al ejercicio"]),
]


ESPECIALISTAS = [
    dict(nombre_completo="Dra. Laura Gomez", rol="Nutricionista", especialidad="Nutricion Infantil", experiencia_anios=7,
         biografia="Especialista en habitos saludables para ninos de 6 a 14 anos.", contacto_email="laura.gomez@example.com"),
    dict(nombre_completo="Lic. Sofia Vargas", rol="Nutricionista", especialidad="Alimentacion familiar", experiencia_anios=5,
         biografia="Acompana a familias en el cambio de habitos sin dietas restrictivas.", contacto_email="sofia.vargas@example.com"),
    dict(nombre_completo="Dr. Carlos Rojas", rol="Pediatra", especialidad="Pediatria general", experiencia_anios=12,
         biografia="Pediatra con enfoque en prevencion de obesidad infantil.", contacto_email="carlos.rojas@example.com"),
    dict(nombre_completo="Dra. Andrea Salinas", rol="Pediatra", especialidad="Crecimiento y desarrollo", experiencia_anios=9,
         biografia="Seguimiento del crecimiento y la nutricion en edad escolar.", contacto_email="andrea.salinas@example.com"),
    dict(nombre_completo="Prof. Maria Lopez", rol="Entrenador", especialidad="Actividad fisica infantil", experiencia_anios=5,
         biografia="Entrenadora certificada en ejercicio para ninos y adolescentes.", contacto_email="maria.lopez@example.com"),
    dict(nombre_completo="Prof. Diego Castro", rol="Entrenador", especialidad="Deporte recreativo", experiencia_anios=8,
         biografia="Especialista en juegos activos y rutinas seguras por edad.", contacto_email="diego.castro@example.com"),
]


async def cargar() -> int:
    settings = get_settings()
    host = settings.mongodb_uri.split("@")[-1] if "@" in settings.mongodb_uri else settings.mongodb_uri
    print(f"Conectando a: {host}")
    print(f"Base de datos: {settings.mongodb_db_name}\n")

    client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=8000)
    try:
        db = client[settings.mongodb_db_name]
        await asegurar_colecciones_modulo2(db)

        # Borrar catalogo previo (idempotente)
        for col in (COLLECTION_GUIAS, COLLECTION_MENUS, COLLECTION_ESPECIALISTAS):
            r = await db[col].delete_many({})
            print(f"OK: borrados {r.deleted_count} de {col}")

        repo = NutricionRepository(db)

        for g in GUIAS:
            await repo.insertar_guia(**g)
        print(f"OK: {len(GUIAS)} guias insertadas")

        for m in MENUS:
            await repo.insertar_menu(**m)
        print(f"OK: {len(MENUS)} menus insertados")

        for e in ESPECIALISTAS:
            await repo.insertar_especialista(**e, disponible=True)
        print(f"OK: {len(ESPECIALISTAS)} especialistas insertados")

        print("\nCatalogo del Modulo 2 ampliado correctamente.")
        return 0
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(asyncio.run(cargar()))
