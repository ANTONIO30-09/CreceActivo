# Progreso del proyecto — CreceActivo

## Estado actual

Backend completo de los 3 modulos funcionando end-to-end contra MongoDB Atlas real. Total: 146 tests pasando.

- Modulo 1: CRUD de perfiles infantiles con auth Firebase (44 tests).
- Modulo 2: puerto `ContenidoNutricionalPort`, adaptador Mongo con 4 colecciones (guias_nutricionales, menus_infantiles, especialistas, solicitudes_orientacion), endpoints de guias/menus/especialistas/solicitudes, seed cargado en Atlas (55 tests).
- Modulo 3: storage de videos (Kevin), puerto `ProgresoPort`, adaptador Mongo con 2 colecciones (registros_actividad, metas_familiares), endpoints de registros/progreso/insignias/metas (25 tests).

Detalle por modulo y por integrante en `docs/AVANCES.md`.

## Decisiones tomadas

- Arquitectura: monolito modular con arquitectura hexagonal (puertos y adaptadores).
- Stack: React + Tailwind (frontend), Python + FastAPI (backend), MongoDB Atlas (BD), Firebase Auth + Storage, Google Gemini API (chatbot), Vercel (hosting frontend), Google Cloud Run (hosting backend).
- Estrategia de ramas: `main` protegida, `dev` como integración, ramas `feat/mod{N}-...` por tarea.

## Próximos pasos

- [ ] Módulo 1: frontend de registro, login y perfiles (Natalia).
- [ ] Módulo 2: IMC infantil con percentiles (RF-06, RF-07); chatbot con respuestas validadas (RF-08, diferido hasta tener API key de Gemini).
- [ ] Módulo 3: catalogo de videos con metadatos (RF-11) y frontend de progreso/metas.
- [ ] Configurar Firebase Storage real (bucket) y probar la subida de videos.
- [ ] Frontend completo de los tres modulos y despliegue (Vercel + Cloud Run).

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
- Tests del backend: 66 pasando (44 + 22 de storage del módulo 3). El frontend compila con `npm run build`.

## 2026-10-07 — Módulo 3: Storage y bucket — Kevin
- Puerto y adaptador Firebase Storage para videos por rango de edad.
- Script de carga MP4 sin sobrescritura y endpoint autenticado para URLs temporales.
- Reglas de acceso y documentación de integración.
- Pendiente: configurar el bucket real y probar con Firebase.

## 2026-10-07 — Módulo 2: dominio de nutrición — Juan Pablo (PR #17)
- Entidades `Plato` y `MenuInfantil` inmutables, con validación de invariantes en `__post_init__`.
- Enums `RangoEdad` y `TipoComida`; regla `obtener_rango_edad` en `reglas.py`.
- Excepciones de dominio: `ErrorDominioNutricion`, `EdadFueraDeRango`, `PlatoInvalido`, `MenuInvalido`.
- 40 tests nuevos de dominio puro, sin Mongo ni Firebase. Backend: 106 tests pasando.

## 2026-10-14 — Módulo 2: backend completo (contrato, adaptador, endpoints, seed)

- [x] Contrato público del M2 en `docs/contratos.md`: `ContenidoNutricionalPort` + DTOs (`GuiaDTO`, `PlatoDTO`, `MenuDTO`, `EspecialistaDTO`).
- [x] Adaptador Mongo con 4 colecciones y validadores `$jsonSchema`:
  - `guias_nutricionales` (índice `idx_guias_rango`).
  - `menus_infantiles` (índice `idx_menus_rango_tipo`).
  - `especialistas` (índice `idx_especialistas_disponible`).
  - `solicitudes_orientacion` (índice `idx_solicitudes_tutor`).
- [x] Repositorio `NutricionRepository` que implementa `ContenidoNutricionalPort`.
- [x] Router HTTP: `GET /modulo2/health`, `GET /modulo2/guias` (+ filtro rango_edad), `GET /modulo2/guias/{id}`, `GET /modulo2/menus` (+ filtros), `GET /modulo2/menus/{id}`, `GET /modulo2/especialistas`, `POST /modulo2/solicitudes` (protegido).
- [x] Seed reescrito sobre el repositorio. Cargados 3 guías, 3 menús y 3 especialistas en Mongo Atlas real.
- [x] 15 tests nuevos del router con repo falso. Backend: 121 tests pasando.
- [x] `models.py` (Pydantic paralelo al dominio) marcado como `[DEPRECATED]`; su contenido quedó absorbido por `domain/entidades.py`, `ports/dto.py` y `adapters/api/schemas.py`.
- [x] Verificado end-to-end contra Atlas: `GET /modulo2/guias?rango_edad=6-8 años` devuelve solo las guías del rango.

**Módulos 1 y 3:** el puerto del M2 no se importa directamente. Ninguna dependencia cruzada rota. Los 121 tests previos siguen verdes.

## 2026-10-14 — Módulo 3: backend de progreso, rachas, insignias y metas

- [x] Contrato público del M3 ampliado: además de `VideoStoragePort` (Kevin), se añade `ProgresoPort` en `app.modulo3_ejercicios.ports.progreso_port` con DTOs (`RegistroDTO`, `MetaDTO`, `InsigniaDTO`, `ProgresoDTO`).
- [x] Dominio puro del M3 en `domain/`:
  - Enums `TipoActividad` (rutina, agua, minutos) y `EstadoMeta` (activa, archivada).
  - Entidades inmutables `RegistroActividad` y `MetaFamiliar` con validación en `__post_init__`.
  - Reglas puras `racha_actual`, `mejor_racha`, `semana_actual`, `porcentaje_meta` y `evaluar_insignias` (8 insignias predefinidas). Lógica portada del aporte de Luis David Cespedes Camacho y adaptada al dominio del proyecto.
- [x] Adaptador Mongo con 2 colecciones y validadores `$jsonSchema`:
  - `registros_actividad` (índice `idx_registros_perfil_fecha`).
  - `metas_familiares` (índice `idx_metas_perfil_estado`).
- [x] Repositorio `ProgresoRepository` que implementa `ProgresoPort` con 7 métodos.
- [x] Router HTTP nuevo: `POST /modulo3/registros`, `GET /modulo3/registros/{perfil_id}`, `GET /modulo3/progreso/{perfil_id}`, `GET /modulo3/insignias/catalogo`, `POST /modulo3/metas`, `GET /modulo3/metas/{perfil_id}`, `POST /modulo3/metas/{meta_id}/marcar`, `DELETE /modulo3/metas/{meta_id}`.
- [x] Verificados end-to-end: los 9 endpoints del M3 responden 401 sin token Bearer.
- [x] 25 tests nuevos de dominio puro del M3. Backend: 146 tests pasando.
- [ ] Pendiente: catalogo de videos con metadatos (RF-11) y frontend de progreso/metas.

**Módulos 1 y 2:** sin cambios en sus puertos. Los 121 tests previos siguen verdes.
