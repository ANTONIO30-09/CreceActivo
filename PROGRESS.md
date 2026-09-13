# Progreso del proyecto — CreceActivo

## Estado actual
Inicialización del repositorio. Estructura base creada siguiendo arquitectura hexagonal (monolito modular). Sin funcionalidad implementada todavía.

## Decisiones tomadas
- Arquitectura: monolito modular con arquitectura hexagonal (puertos y adaptadores).
- Stack: React + Tailwind (frontend), Python + FastAPI (backend), MongoDB Atlas (BD), Firebase Auth + Storage, Google Gemini API (chatbot), Vercel (hosting frontend), Google Cloud Run (hosting backend).
- Estrategia de ramas: `main` protegida, `dev` como integración, ramas `feat/mod{N}-...` por tarea.

## Próximos pasos
- [ ] Definir el primer `port` de Módulo 1 (perfil infantil) para que Módulo 2 y 3 puedan empezar a construir contra ese contrato.
- [ ] Configurar conexión real a MongoDB Atlas (con `.env`, no subir credenciales).
- [ ] Configurar proyecto de Firebase (Auth + Storage).
- [ ] Documentar los primeros contratos en `docs/contratos.md`.
