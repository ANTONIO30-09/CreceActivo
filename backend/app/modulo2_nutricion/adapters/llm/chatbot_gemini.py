"""Adaptador Gemini del ChatbotPort (Modulo 2).

Usa google-genai. La API key se recibe en el constructor y NUNCA se
loguea. El system prompt prohibe diagnosticos y obliga a derivar si la
pregunta no esta cubierta por el contexto.
"""
from __future__ import annotations

from google import genai

from ...ports.chatbot_port import DERIVAR

__all__ = ["ChatbotGemini"]

_MODELOS = (
    "gemini-3.8-flash",      # modelo actual recomendado (2026)
    "gemini-3.5-flash",      # fallback
)

_SYSTEM = (
    "Eres un Asistente Nutricional Avanzado dentro de CreceActivo, una "
    "plataforma para familias con ninos de 6 a 14 anos. Tono empatico, "
    "profesional y estructurado. Nunca des respuestas vagas.\n\n"
    "SEGURIDAD (critico):\n"
    "- Solo informacion nutricional validada por el CONTEXTO que se te da.\n"
    "- Nunca diagnostiques patologias medicas.\n"
    "- Si el usuario menciona sintomas de enfermedad, redirigelo a consulta "
    "presencial con un profesional.\n\n"
    "COMPORTAMIENTO:\n"
    "- Si te piden ideas de comidas (desayuno, merienda, almuerzo, cena) o "
    "habitos (agua, porciones), NO respondas con un solo parrafo.\n"
    "- Desglosa cada opcion con: **Nombre del plato**, ingredientes "
    "principales, metodo de coccion sugerido y beneficio nutricional "
    "especifico para ese momento del dia.\n"
    "- Ofrece 2 o 3 opciones distintas cuando sea posible.\n\n"
    "FORMATO (obligatorio):\n"
    "- Usa Markdown limpio.\n"
    "- Titulos con ### para cada opcion de comida.\n"
    "- Listas con guiones para ingredientes o pasos.\n"
    "- Negritas para macronutrientes y conceptos clave.\n"
    "- Emojis moderados (1 por seccion maximo).\n\n"
    "Responde UNICAMENTE con la frase exacta: '" + DERIVAR + "' si la pregunta "
    "es claramente medica (sintomas, medicamento, diagnostico) o no tiene NADA "
    "que ver con alimentacion, habitos o actividad fisica.\n\n"
    "Escribe siempre en espanol. No menciones la palabra 'contexto' ni 'documento': "
    "habla natural."
)


class ChatbotGemini:
    """Implementacion del ChatbotPort sobre Google Gemini."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("api_key requerida")
        self._client = genai.Client(api_key=api_key)

    async def responder(self, pregunta: str, contexto: str) -> str:
        prompt = (
            "Informacion nutricional validada de CreceActivo:\n\n"
            f"{contexto}\n\n"
            f"Pregunta del tutor: {pregunta}\n\n"
            "Responde aplicando el formato indicado: Markdown, secciones con ###, "
            "listas y negritas. Si te piden ideas de comidas, desglosa 2-3 opciones "
            "con ingredientes, coccion y beneficio."
        )
        ultimo_error: Exception | None = None
        for modelo in _MODELOS:
            for intento in range(3):
                try:
                    resp = await self._client.aio.models.generate_content(
                        model=modelo,
                        contents=prompt,
                        config={"system_instruction": _SYSTEM, "temperature": 0.4},
                    )
                    texto = (getattr(resp, "text", "") or "").strip()
                    return texto or DERIVAR
                except Exception as e:  # noqa: BLE001
                    ultimo_error = e
                    status = getattr(e, "status_code", None) or getattr(e, "code", None)
                    # Solo reintentamos si es 503 (sobrecarga temporal)
                    if status == 503 and intento < 2:
                        import asyncio
                        await asyncio.sleep(1.5 * (intento + 1))
                        continue
                    break
        # Traducir a error HTTP claro
        from fastapi import HTTPException
        status = getattr(ultimo_error, "status_code", None) or getattr(ultimo_error, "code", None)
        if status == 503:
            raise HTTPException(503, "El servicio de IA esta saturado. Intenta de nuevo en unos segundos.")
        if status == 429:
            raise HTTPException(503, "Cuota de IA agotada. Intenta mas tarde.")
        raise HTTPException(502, f"Error del proveedor de IA: {ultimo_error}")
