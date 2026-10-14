"""Puerto del chatbot nutricional (Modulo 2).

El chatbot SOLO responde con informacion validada del propio Modulo 2
(guias y menus). Si no hay base, deriva a un profesional. Nunca diagnostica.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

__all__ = ["ChatbotPort", "DERIVAR"]


DERIVAR = (
    "No tengo informacion validada para responder a eso. "
    "Te recomiendo consultar con un profesional de la salud."
)


@runtime_checkable
class ChatbotPort(Protocol):
    """Contrato que el Modulo 2 OFRECE al frontend."""

    async def responder(self, pregunta: str, contexto: str) -> str:
        ...
