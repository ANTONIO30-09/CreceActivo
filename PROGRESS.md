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

## 2026-09-15 — Módulo 1, Fase 1 (mergeado a dev, PR #1)
- [x] Entidad `PerfilInfantil` + enums (`Sexo`, `NivelActividadFisica`).
- [x] DTO `PerfilInfantilDTO` + puerto `PerfilInfantilPort` (Protocol async).
- [x] Contrato público documentado en `docs/contratos.md`.
- [x] 27 tests unitarios (dominio + contrato), todos pasando.
- [ ] Fase 2: esqueleto FastAPI + Mongo Atlas + Firebase Auth (por empezar).

**Módulos 2 y 3:** pueden consumir `app.modulo1_usuarios.ports.perfil_infantil_port`.

## 2026-09-15 — Módulo 1, Fase 2 (esqueleto FastAPI + Mongo Atlas + Firebase Auth)
- [x] Configuracion tipada con `pydantic-settings` (`.env` en la raiz del monorepo).
- [x] Cliente `motor` async con ping en lifespan.
- [x] Verificacion de tokens con Firebase Admin SDK.
- [x] App FastAPI + CORS + router del Modulo 1.
- [x] Endpoints base: `GET /`, `GET /modulo1/health`, `GET /modulo1/whoami`.
- [x] Tests de arranque, health y auth mockeada (32 pasando).
- [ ] Fase 3: CRUD de `PerfilInfantil` + repositorio Mongo (por empezar).

**Modulos 2 y 3:** pueden pegarle al backend en `http://localhost:8000`.
