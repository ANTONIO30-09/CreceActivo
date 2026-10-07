from pydantic import BaseModel, Field
from typing import List, Optional

class Plato(BaseModel):
    nombre: str
    descripcion: str
    calorias_aprox: int
    ingredientes: List[str]

class MenuInfantil(BaseModel):
    titulo: str
    rango_edad: str  # Ej: "6-8 años", "9-11 años", "12-14 años"
    tipo_comida: str  # Desayuno, Almuerzo, Cena, Merienda
    platos: List[Plato]
    recomendaciones: List[str]

class GuiaNutricional(BaseModel):
    titulo: str
    categoria: str
    rango_edad: str
    contenido: str
    habitos_clave: List[str]

class Especialista(BaseModel):
    nombre_completo: str
    rol: str  # Nutricionista o Entrenador
    especialidad: str
    experiencia_anios: int
    biografia: str
    contacto_email: str
    disponible: bool = True
