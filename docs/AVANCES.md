# Avances de CreceActivo

Estado al 14 de octubre de 2026, reconstruido a partir del historial de Git.

Estado general: `dev` con 146 tests pasando, backend de los 3 modulos funcionando
end-to-end contra MongoDB Atlas real.

## Resumen por modulo

| Modulo | Estado | Entregado | Pendiente |
| --- | --- | --- | --- |
| 1 · Usuarios y perfil infantil | Backend completo | Contrato publico, API base, auth Firebase, esquema Mongo, repositorio, CRUD de perfiles, 44 tests | Frontend (registro, login, perfiles) |
| 2 · Nutricion y orientacion profesional | Backend completo | Dominio de nutricion, puerto `ContenidoNutricionalPort`, adaptador Mongo con 4 colecciones, endpoints de guias/menus/especialistas/solicitudes, seed cargado en Atlas, 55 tests | IMC con percentiles, chatbot Gemini (diferido), frontend completo |
| 3 · Ejercicios, progreso y motivacion | Backend completo | Storage de videos, puerto `ProgresoPort`, adaptador Mongo con 2 colecciones, endpoints de registros/progreso/insignias/metas, 25 tests | Catalogo de videos con metadatos, frontend de progreso/metas |

## Modulo 1 — Usuarios y perfil infantil

**Contrato y dominio (Antonio)**
- Enums de dominio `Sexo` y `NivelActividadFisica`.
- Entidad `PerfilInfantil` inmutable, con validacion de invariantes (edad 6-14, limites de texto, alergias, UTC).
- `PerfilInfantilDTO` y `PerfilInfantilPort` (`obtener_por_id`, `listar_por_tutor`, `existe`): es lo unico que los modulos 2 y 3 pueden importar.
- Tests unitarios de validaciones y de contrato (PR #1).

**Infraestructura del backend (Antonio)**
- Configuracion por entorno con `pydantic-settings` (PR #2).
- Cliente Mongo asincrono (`motor`) con ciclo de conexion.
- Verificacion de tokens de Firebase como dependencia de FastAPI.
- App FastAPI con `/health` y `/whoami`, con tests de arranque y seguridad.
- Documentacion de endpoints base y del contrato.

**Base de datos (Nicolas Villazon)**
- Validador de esquema de la coleccion `perfiles_infantiles` en Mongo.
- Indice parcial por tutor activo.
- Funcion que crea la coleccion o actualiza el validador sin borrar documentos.
- 7 tests propios (`test_esquema_perfiles.py`).

**Repositorio (Natalia Camacho)**
- `PerfilInfantilRepository`, que implementa `PerfilInfantilPort` sobre Mongo.
- Conversion documento ↔ entidad (`id` ↔ `_id`, tupla ↔ lista, fechas a UTC).
- Metodos internos `insertar`, `actualizar` y `desactivar` (borrado suave).

**Esquemas y endpoints (David Bazoberry, commits firmados "Mateo Bazoberry")**
- Esquemas Pydantic de creacion, actualizacion y respuesta.
- CRUD bajo `/modulo1/perfiles`: `POST`, `GET` (lista), `GET /{id}`, `PATCH /{id}`, `DELETE /{id}`.
- Un tutor solo puede ver y modificar sus propios perfiles (404 si no le pertenece).

**Integracion y correcciones (Antonio)**
- Merge de todas las ramas del modulo en `dev`.
- Fix del PR #7: `PATCH` fallaba con `AttributeError` por usar campos que el DTO no expone; el schema de respuesta exigia `activo`, `creado_en` y `actualizado_en`; `POST` y `PATCH` devolvian 500 en vez de 422 ante datos invalidos del dominio.
- Nuevo `repo.obtener_entidad()` (uso interno) y 3 tests del router sin Mongo ni Firebase.
- Cambio visible en la API: la respuesta ya no incluye `activo`, `creado_en` ni `actualizado_en`.

**Pendiente:** frontend de registro/login/perfiles; tests de POST exitoso, GET y DELETE; pruebas del repositorio contra un Mongo real.

## Modulo 2 — Nutricion y orientacion profesional

**Base de datos (Misael Patrick Ramos)**
- Modelos Pydantic iniciales (`models.py`, hoy deprecado).
- Script `seed_mod2.py` para cargar datos iniciales (PR #3).
- Actualizacion de `PROGRESS.md` con el avance de la base de datos.

**Frontend (Matthew Gomez)**
- Frontend inicial de nutricion (PR #4).

**Dominio (Juan Pablo Villca, usuario `juanw21`, PR #17)**
- Entidades `Plato` y `MenuInfantil` inmutables, con validacion de invariantes en `__post_init__`.
- Enums `RangoEdad` (6-8, 9-11, 12-14) y `TipoComida`.
- Regla de dominio `obtener_rango_edad` en `reglas.py`, con excepcion propia `EdadFueraDeRango`.
- Excepciones de dominio (`ErrorDominioNutricion`, `PlatoInvalido`, `MenuInvalido`).
- 40 tests nuevos de dominio puro, sin Mongo ni Firebase.

**Backend y migraciones (Franco Guerra — cubierto en su totalidad por Antonio)**
- Contrato publico del modulo en `docs/contratos.md`: `ContenidoNutricionalPort` con 6 metodos y 4 DTOs (`GuiaDTO`, `PlatoDTO`, `MenuDTO`, `EspecialistaDTO`).
- Adaptador Mongo con 4 colecciones y validadores `$jsonSchema`: `guias_nutricionales`, `menus_infantiles`, `especialistas`, `solicitudes_orientacion`.
- Indices: `idx_guias_rango`, `idx_menus_rango_tipo`, `idx_especialistas_disponible`, `idx_solicitudes_tutor`.
- Repositorio `NutricionRepository` que implementa `ContenidoNutricionalPort`.
- Router HTTP: `GET /modulo2/health`, `GET /modulo2/guias` (con filtro `rango_edad`), `GET /modulo2/guias/{id}`, `GET /modulo2/menus` (con filtros `rango_edad` y `tipo_comida`), `GET /modulo2/menus/{id}`, `GET /modulo2/especialistas`, `POST /modulo2/solicitudes` (protegido por Firebase).
- Seed reescrito sobre el repositorio. 3 guias, 3 menus y 3 especialistas cargados en Mongo Atlas real.
- 15 tests nuevos del router con repositorio falso.
- `models.py` marcado como `[DEPRECATED]`; su contenido fue absorbido por `domain/entidades.py`, `ports/dto.py` y `adapters/api/schemas.py`.

**Pendiente:** IMC infantil con percentiles (RF-06, RF-07); chatbot con respuestas validadas (RF-08, diferido sin API key de Gemini); frontend completo del modulo.

## Modulo 3 — Ejercicios, progreso y motivacion

**Frontend (Allen Requena, usuario `jhonesde`)**
- Inicializacion de Vite y Tailwind para el modulo (PR #5).
- Componentes `VideoCard` y `VideoLibrary` (biblioteca de videos).
- Reubicacion de componentes en `frontend/` (PR #6).

**Storage de videos (Kevin Pena, usuario `kpena6532-commits`, PR #13)**
- Puerto `VideoStoragePort` y adaptador `FirebaseVideoStorage` (bucket privado, operaciones fuera del event loop).
- Endpoint `GET /modulo3/videos/{grupo_edad}/{video_id}/url`: entrega URL firmada temporal (900 s por defecto) solo a tutores autenticados.
- Script administrativo `backend/subir_video_mod3.py`.
- `storage.rules` que niega acceso directo al bucket y `docs/modulo3_storage.md`.
- 22 tests nuevos, sin Firebase real.

**Backend y base de datos (Luis David Cespedes — logica rescatada por Antonio)**
- Contrato publico ampliado: ademas de `VideoStoragePort`, se anade `ProgresoPort` en `app.modulo3_ejercicios.ports.progreso_port` con 4 DTOs (`RegistroDTO`, `MetaDTO`, `InsigniaDTO`, `ProgresoDTO`).
- Dominio puro del M3 en `domain/`:
  - Enums `TipoActividad` (rutina, agua, minutos) y `EstadoMeta` (activa, archivada).
  - Entidades inmutables `RegistroActividad` y `MetaFamiliar` con validacion en `__post_init__`.
  - Reglas puras `racha_actual`, `mejor_racha`, `semana_actual`, `porcentaje_meta` y `evaluar_insignias` (8 insignias predefinidas).
- Adaptador Mongo con 2 colecciones y validadores `$jsonSchema`:
  - `registros_actividad` (indice `idx_registros_perfil_fecha`).
  - `metas_familiares` (indice `idx_metas_perfil_estado`).
- Repositorio `ProgresoRepository` que implementa `ProgresoPort` con 7 metodos.
- Router HTTP nuevo: `POST /modulo3/registros`, `GET /modulo3/registros/{perfil_id}`, `GET /modulo3/progreso/{perfil_id}`, `GET /modulo3/insignias/catalogo`, `POST /modulo3/metas`, `GET /modulo3/metas/{perfil_id}`, `POST /modulo3/metas/{meta_id}/marcar`, `DELETE /modulo3/metas/{meta_id}`.
- 25 tests nuevos de dominio puro del M3.

**Nota sobre el aporte de Luis David:** entrego dos ZIPs (`habitos_saludables.zip` y `SistemaMetasFamiliares.zip`) con stack distinto al del proyecto (CLI + JSON local + Flask + SQLite). Se rescato exclusivamente la logica de rachas, insignias y metas familiares, reescribiendola dentro de la arquitectura hexagonal (FastAPI + MongoDB). El resto fue descartado por incompatibilidad con el stack acordado.

**Pendiente:** catalogo de videos con metadatos (RF-11) y su listado por rango de edad (RF-10); frontend de progreso y metas.

## Aportes por integrante

| Integrante | Modulo / rol | Aporte visible |
| --- | --- | --- |
| Antonio Vicente Garcia Corrales | M1 · Backend · Lider | Contrato publico, dominio, infraestructura, tests, integracion, fix de PATCH, README. Ademas cubrio el backend completo de M2 (adaptador Mongo, endpoints, seed) y M3 (dominio de progreso, adaptador, endpoints, tests) ante la ausencia de Franco y el stack incompatible de Luis David. |
| Pablo Nicolas Villazon Quiroga | M1 · Base de datos | Esquema y validador de Mongo, indice parcial, 7 tests |
| Natalia Camacho Cardozo | M1 · Frontend | Repositorio Mongo del puerto |
| David Ignacio Bazoberry Grigoriu | M1 · Backend y API | Esquemas Pydantic y CRUD de perfiles |
| Juan Pablo Villca Revollo | M2 · Backend | Dominio de nutricion (entidades, enums, reglas, excepciones, 40 tests) |
| Matthew Alejandro Gomez Torrez | M2 · Frontend | Frontend inicial de nutricion |
| Misael Patrick Ramos Torrez | M2 · Base de datos | Modelos Pydantic iniciales, seed, avance en `PROGRESS.md` |
| Franco Guerra Roca | M2 · Backend y migraciones | No pudo entregar por motivos personales; su parte fue cubierta por el lider (Antonio) |
| Allen Jhonatan Requena Heredia | M3 · Frontend | Base Vite/Tailwind, biblioteca de videos |
| Kevin Pena Jamachi | M3 · Storage y bucket | Puerto y adaptador de Storage, endpoint de URL firmada, script de carga, reglas del bucket, 22 tests |
| Luis David Cespedes Camacho | M3 · Backend y BD | Entrego la logica de rachas, insignias y metas familiares en stack Flask/SQLite; fue portada a la arquitectura hexagonal por el lider (Antonio) |

**Nota sobre aportes no visibles directamente en el historial de Git:**
- Franco Guerra no pudo subir commits por motivos personales. El lider cubrio su parte del backend del M2 integramente.
- Luis David Cespedes entrego su trabajo en ZIPs con stack distinto al proyecto. Su logica se rescato y adapto; el resto se descarto.
- Todos los modulos tienen su backend funcional y testeado a la fecha del 14 de octubre de 2026.
