# Avances de CreceActivo

Estado al 7 de octubre de 2026, reconstruido a partir del historial de Git y de
los Pull Requests (#1 a #17). Refleja lo que esta subido al repositorio; el
trabajo que alguien tenga en local sin subir no aparece aqui.

Estado general: `dev` y `main` estan sincronizadas, los 106 tests del backend
pasan y el frontend compila (`npm run build`).

## Resumen por modulo

| Modulo | Estado | Entregado | Pendiente |
| --- | --- | --- | --- |
| 1 · Usuarios y perfil infantil | Backend avanzado | Contrato publico, API base, auth Firebase, esquema Mongo, repositorio, CRUD de perfiles, 44 tests | Frontend (registro, login, perfiles); tests de endpoints exitosos y del repositorio contra Mongo real |
| 2 · Nutricion y orientacion profesional | En marcha | Modelos Pydantic, script seed, frontend inicial de nutricion, dominio de nutricion (entidades, enums, reglas, excepciones, tests) | Guias y menus, IMC con percentiles, chatbot, solicitud a especialistas, endpoints |
| 3 · Ejercicios, progreso y motivacion | En marcha | Base Vite + Tailwind, `VideoCard`, `VideoLibrary`, puerto y adaptador de Storage de videos, endpoint de URL firmada | Catalogo de videos con metadatos, registro de rutinas/agua/minutos, rachas e insignias, metas |

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
- Modelos Pydantic del modulo (`modulo2_nutricion/models.py`).
- Script `seed_mod2.py` para cargar datos iniciales.
- Actualizacion de `PROGRESS.md` con el avance de la base de datos (PR #3).

**Frontend (Matthew Gomez)**
- Frontend inicial de nutricion (PR #4).

**Dominio (Juan Pablo Villca, usuario `juanw21`, PR #17)**
- Entidades `Plato` y `MenuInfantil` inmutables, con validacion de invariantes en `__post_init__`.
- Enums `RangoEdad` (6-8, 9-11, 12-14) y `TipoComida`.
- Regla de dominio `obtener_rango_edad` en `reglas.py`, con excepcion propia `EdadFueraDeRango`.
- Excepciones de dominio (`ErrorDominioNutricion`, `PlatoInvalido`, `MenuInvalido`).
- 40 tests nuevos de dominio puro, sin Mongo ni Firebase.

**Deuda conocida (nota en `docs/contratos.md`):** el seed inserta en `menus` y `specialists` sin validador y con nombres en ingles; falta alinearlos con la convencion del modulo 1.

**Pendiente:** guias y menus validados (RF-05), IMC infantil con percentiles (RF-06, RF-07), chatbot con respuestas validadas (RF-08), solicitud de orientacion a especialistas (RF-09), endpoints y servicio del modulo. Sin commits visibles de Franco Guerra.

## Modulo 3 — Ejercicios, progreso y motivacion

**Frontend (usuario `jhonesde`, 6 commits; probablemente Allen Requena)**
- Inicializacion de Vite y Tailwind para el modulo (PR #5).
- Componentes `VideoCard` y `VideoLibrary` (biblioteca de videos).
- Reubicacion de componentes en `frontend/` y limpieza de configuracion en la raiz (PR #6).

**Storage de videos (Kevin Pena, usuario `kpena6532-commits`, PR #13)**
- Puerto `VideoStoragePort` y adaptador `FirebaseVideoStorage` (Firebase Storage, bucket privado, operaciones fuera del event loop).
- Endpoint `GET /modulo3/videos/{grupo_edad}/{video_id}/url`: entrega una URL firmada temporal (900 s por defecto) solo a tutores autenticados.
- Script administrativo `backend/subir_video_mod3.py` para cargar MP4 sin sobrescribir existentes.
- `storage.rules` que niega todo acceso directo al bucket, `.gitignore` para credenciales y videos, y `docs/modulo3_storage.md`.
- 22 tests nuevos (el total del backend paso a 106 tras el dominio del modulo 2), sin Firebase real.

**Pendiente:** catalogo de videos con metadatos (duracion, dificultad, materiales, seguridad; RF-11) y su listado por rango de edad (RF-10); decidir si el endpoint exige un perfil infantil registrado (CU-05); registro de rutinas, agua y minutos (RF-12); rachas e insignias (RF-13); metas familiares (RF-14). Sin commits visibles de Luis David Cespedes. La subida a Firebase no se ha probado con un bucket real.

## Aportes por integrante

| Integrante | Usuario de GitHub | Modulo / rol (informe) | Aporte visible |
| --- | --- | --- | --- |
| Antonio Vicente Garcia Corrales | `ANTONIO30-09` | M1 · Backend | 29 commits: contrato, dominio, infraestructura, tests, integracion, fix de PATCH, README y PRs #1, #2, #7, #8, #9 |
| Pablo Nicolas Villazon Quiroga | `cbbepablonicolasvillazonqu-sudo` | M1 · Base de datos | Esquema y validador de Mongo, indice parcial, 7 tests |
| Natalia Camacho Cardozo | `NatXaam` (por confirmar) | M1 · Frontend | Repositorio Mongo del puerto (trabajo de backend; sin frontend subido) |
| David Ignacio Bazoberry Grigoriu | `MateoBazo` (por confirmar) | M1 · Backend y API | Esquemas Pydantic y CRUD de perfiles |
| Juan Pablo Villca Revollo | `juanw21` | M2 · Backend | Dominio de nutricion (entidades, enums, reglas, excepciones, 40 tests) · PR #17 |
| Matthew Alejandro Gomez Torrez | `MATTUPAPI-art` (por confirmar) | M2 · Frontend | Frontend inicial de nutricion |
| Misael Patrick Ramos Torrez | `surevalle2627` (por confirmar) | M2 · Base de datos | Modelos Pydantic, seed y avance en `PROGRESS.md` |
| Franco Guerra Roca | sin identificar | M2 · Backend y migraciones | Sin aportes visibles |
| Allen Jhonatan Requena Heredia | `jhonesde` (por confirmar) | M3 · Frontend | Base Vite/Tailwind, biblioteca de videos |
| Kevin Pena Jamachi | `kpena6532-commits` | M3 · Storage y bucket | Puerto y adaptador de Storage, endpoint de URL firmada, script de carga, reglas del bucket, 22 tests |
| Luis David Cespedes Camacho | sin identificar | M3 · Backend y BD | Sin aportes visibles |

"Sin aportes visibles" significa que no hay commits ni Pull Requests suyos en el
repositorio; puede haber trabajo local sin subir o commits hechos con otro
correo. Cada integrante debe configurar en su maquina el mismo correo que usa
en GitHub (`git config user.email`).
