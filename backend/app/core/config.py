"""
Configuración central de la aplicación.
Lee las variables desde el archivo .env (nunca hardcodear secretos aquí).
"""
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
