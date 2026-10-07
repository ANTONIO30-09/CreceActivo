# Avances de CreceActivo

Estado al 7 de octubre de 2026, reconstruido a partir del historial de Git y de
los Pull Requests (#1 a #9). Refleja lo que esta subido al repositorio; el
trabajo que alguien tenga en local sin subir no aparece aqui.

Estado general: `dev` y `main` estan sincronizadas, los 44 tests del backend
pasan y el frontend compila (`npm run build`).

## Resumen por modulo

| Modulo | Estado | Entregado | Pendiente |
| --- | --- | --- | --- |
| 1 · Usuarios y perfil infantil | Backend avanzado | Contrato publico, API base, auth Firebase, esquema Mongo, repositorio, CRUD de perfiles, 44 tests | Frontend (registro, login, perfiles); tests de endpoints exitosos y del repositorio contra Mongo real |
| 2 · Nutricion y orientacion profesional | Inicial | Modelos Pydantic, script seed, frontend inicial de nutricion | Guias y menus, IMC con percentiles, chatbot, solicitud a especialistas, endpoints |
| 3 · Ejercicios, progreso y motivacion | Inicial | Base Vite + Tailwind, `VideoCard`, `VideoLibrary` | Backend, storage de videos, registro de rutinas/agua/minutos, rachas e insignias, metas |

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

**Pendiente:** guias y menus validados (RF-05), IMC infantil con percentiles (RF-06, RF-07), chatbot con respuestas validadas (RF-08), solicitud de orientacion a especialistas (RF-09), endpoints y servicio del modulo. Sin commits visibles de Juan Pablo Villca ni Franco Guerra.

## Modulo 3 — Ejercicios, progreso y motivacion

**Frontend (usuario `jhonesde`, 6 commits; probablemente Allen Requena)**
- Inicializacion de Vite y Tailwind para el modulo (PR #5).
- Componentes `VideoCard` y `VideoLibrary` (biblioteca de videos).
- Reubicacion de componentes en `frontend/` y limpieza de configuracion en la raiz (PR #6).

**Pendiente:** backend del modulo, almacenamiento de videos (RF-10, RF-11), registro de rutinas, agua y minutos (RF-12), rachas e insignias (RF-13), metas familiares (RF-14). Sin commits visibles de Kevin Pena ni Luis David Cespedes.

## Aportes por integrante

| Integrante | Usuario de GitHub | Modulo / rol (informe) | Aporte visible |
| --- | --- | --- | --- |
| Antonio Vicente Garcia Corrales | `ANTONIO30-09` | M1 · Backend | 29 commits: contrato, dominio, infraestructura, tests, integracion, fix de PATCH, README y PRs #1, #2, #7, #8, #9 |
| Pablo Nicolas Villazon Quiroga | `cbbepablonicolasvillazonqu-sudo` | M1 · Base de datos | Esquema y validador de Mongo, indice parcial, 7 tests |
| Natalia Camacho Cardozo | `NatXaam` (por confirmar) | M1 · Frontend | Repositorio Mongo del puerto (trabajo de backend; sin frontend subido) |
| David Ignacio Bazoberry Grigoriu | `MateoBazo` (por confirmar) | M1 · Backend y API | Esquemas Pydantic y CRUD de perfiles |
| Juan Pablo Villca Revollo | sin identificar | M2 · Backend | Sin aportes visibles |
| Matthew Alejandro Gomez Torrez | `MATTUPAPI-art` (por confirmar) | M2 · Frontend | Frontend inicial de nutricion |
| Misael Patrick Ramos Torrez | `surevalle2627` (por confirmar) | M2 · Base de datos | Modelos Pydantic, seed y avance en `PROGRESS.md` |
| Franco Guerra Roca | sin identificar | M2 · Backend y migraciones | Sin aportes visibles |
| Allen Jhonatan Requena Heredia | `jhonesde` (por confirmar) | M3 · Frontend | Base Vite/Tailwind, biblioteca de videos |
| Kevin Pena Jamachi | sin identificar | M3 · Storage y bucket | Sin aportes visibles |
| Luis David Cespedes Camacho | sin identificar | M3 · Backend y BD | Sin aportes visibles |

"Sin aportes visibles" significa que no hay commits ni Pull Requests suyos en el
repositorio; puede haber trabajo local sin subir o commits hechos con otro
correo. Cada integrante debe configurar en su maquina el mismo correo que usa
en GitHub (`git config user.email`).
