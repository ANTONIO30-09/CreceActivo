"""Adaptador Gemini del ChatbotPort (Modulo 2).

Usa google-genai. La API key se recibe en el constructor y NUNCA se
loguea. El system prompt prohibe diagnosticos y obliga a derivar si la
pregunta no esta cubierta por el contexto.
"""
from __future__ import annotations

from google import genai

from ...ports.chatbot_port import DERIVAR

__all__ = ["ChatbotGemini"]

_MODELO = "gemini-2.0-flash"

_SYSTEM = (
    "Eres un asistente nutricional para familias con ninos de 6 a 14 anos. "
    "Responde SOLO usando el CONTEXTO proporcionado. "
    "Prohibido dar diagnosticos, dosis, tratamientos o consejos medicos. "
    "Si la pregunta es medica, requiere diagnostico, o no esta cubierta por "
    "el contexto, responde exactamente: '" + DERIVAR + "'. "
    "Tono neutro, claro, en espanol, sin alarmismo. No etiquetes al nino."
)


class ChatbotGemini:
    """Implementacion del ChatbotPort sobre Google Gemini."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("api_key requerida")
        self._client = genai.Client(api_key=api_key)

    async def responder(self, pregunta: str, contexto: str) -> str:
        prompt = f"CONTEXTO:\n{contexto}\n\nPREGUNTA:\n{pregunta}"
        resp = await self._client.aio.models.generate_content(
            model=_MODELO,
            contents=prompt,
            config={"system_instruction": _SYSTEM, "temperature": 0.2},
        )
        texto = (getattr(resp, "text", "") or "").strip()
        return texto or DERIVAR
