# Progreso del proyecto — CreceActivo

## Estado actual

Backend del Módulo 1 funcional: contrato público, auth con Firebase, esquema Mongo, repositorio y CRUD de perfiles infantiles (44 tests pasando). Módulo 2 con modelos, seed y frontend inicial de nutrición. Módulo 3 con la base de la biblioteca de videos (frontend). Detalle por módulo y por integrante en `docs/AVANCES.md`.

## Decisiones tomadas

- Arquitectura: monolito modular con arquitectura hexagonal (puertos y adaptadores).
- Stack: React + Tailwind (frontend), Python + FastAPI (backend), MongoDB Atlas (BD), Firebase Auth + Storage, Google Gemini API (chatbot), Vercel (hosting frontend), Google Cloud Run (hosting backend).
- Estrategia de ramas: `main` protegida, `dev` como integración, ramas `feat/mod{N}-...` por tarea.

## Próximos pasos

- [ ] Módulo 1: frontend de registro, login y perfiles; tests de POST exitoso, GET y DELETE; probar el repositorio contra un Mongo real.
- [ ] Módulo 2: guías y menús, IMC infantil con percentiles, chatbot con respuestas validadas, solicitud a especialistas y endpoints del módulo; verificar que `seed_mod2.py` carga datos.
- [ ] Módulo 3: backend, storage de videos, registro de rutinas/agua/minutos, rachas e insignias y metas familiares.
- [ ] Completar `.env.example` con todas las variables de `config.py` (hoy solo trae `MONGODB_URI`).
- [ ] Configurar Firebase Storage y la conexión real a MongoDB Atlas para el equipo (credenciales por canal privado, nunca en el repo).

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
- Módulo 3: Se inició la estructuración de componentes para la biblioteca de videos. 

## 2026-09-22 — Módulo 1, esquema Mongo de perfiles_infantiles

- [x] Validador `$jsonSchema` de `perfiles_infantiles` (strict / error), alineado al dominio.
- [x] Índice parcial `idx_perfiles_tutor_activo` sobre `tutor_id` con `activo: true`.
- [x] Tope de 30 alergias y tope de 128 caracteres en `tutor_id`, en dominio y en Mongo.
- [x] `edad` se mantiene como entero 6-14 declarado por el tutor (sin `fecha_nacimiento`).
- [x] Persistencia y convención para colecciones futuras documentadas en `docs/contratos.md`.
- [ ] Fase 3: CRUD de `PerfilInfantil` + repositorio Mongo que implemente `PerfilInfantilPort` (pendiente).

**Módulos 2 y 3:** el puerto no cambió. La colección no se importa; se consume por `PerfilInfantilPort`.

### Módulo 2 - Nutrición (Base de Datos)

- [x] Definición de modelos Pydantic para Menús, Guías y Especialistas (`backend/app/modulo2_nutricion/models.py`).
- [x] Creación de script de carga inicial de datos sintéticos de prueba (`backend/seed_mod2.py`).

## 2026-10-07 — Integración y correcciones (Módulo 1)
- [x] Integradas en `dev` las ramas de Nicolás (esquema Mongo), Natalia (repositorio), David (CRUD), Patrick (modelos y seed), Matt (frontend de nutrición) y el módulo 3 (biblioteca de videos).
- [x] Corregido `PATCH /modulo1/perfiles/{id}` (PR #7): usaba campos que el DTO no expone y devolvía 500; los errores de dominio ahora responden 422.
- [x] Respuesta de perfiles alineada con el DTO público: ya no incluye `activo`, `creado_en` ni `actualizado_en`.
- [x] README con nombres completos, módulos y roles (PR #8) y `docs/AVANCES.md` (PR #10).
- Tests del backend: 44 pasando. El frontend compila con `npm run build`.

## 2026-10-07 — Módulo 3: Storage y bucket — Kevin
- Puerto y adaptador Firebase Storage para videos por rango de edad.
- Script de carga MP4 sin sobrescritura y endpoint autenticado para URLs temporales.
- Reglas de acceso y documentación de integración.
- Pendiente: configurar el bucket real y probar con Firebase.
