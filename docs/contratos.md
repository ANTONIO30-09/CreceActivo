# Contratos entre módulos

Este documento registra las interfaces (`ports`) que cada módulo expone hacia los demás, para que cualquiera pueda programar contra el contrato sin necesidad de leer el código interno del otro módulo.

## Módulo 1 — Usuarios y perfil infantil
_(por definir)_

## Módulo 2 — Nutrición y orientación profesional
Ver seccion detallada mas abajo.

## Módulo 3 — Ejercicios, progreso y motivación
_(por definir)_

---

## Modulo 1 - Usuarios y perfil infantil

- **Version:** 1.0
- **Fecha:** 2026-09-15
- **Rama:** `feature/modulo1-perfil-infantil-port`
- **Ruta publica (unica permitida para Modulos 2 y 3):**
  `app.modulo1_usuarios.ports.perfil_infantil_port`

### 1. Regla de dependencias (no negociable)

- Modulos 2 y 3 **importan solo** desde `modulo1_usuarios.ports.perfil_infantil_port`.
- **Prohibido** importar `modulo1_usuarios.service`, `modulo1_usuarios.adapters.*`
  o `modulo1_usuarios.domain.*` desde fuera del Modulo 1.
- Internamente: `domain` no depende de `ports` ni `adapters`; `ports` depende
  solo de `domain`; `adapters` depende de `ports` y `domain`.

### 2. Enums publicos

**`Sexo`**
| Valor |
|---|
| `masculino` |
| `femenino` |
| `otro` |
| `prefiero_no_decir` |

**`NivelActividadFisica`**
| Valor |
|---|
| `sedentario` |
| `ligero` |
| `moderado` |
| `activo` |
| `muy_activo` |

### 3. `PerfilInfantilDTO` (read-model publico)

| Campo | Tipo | Descripcion |
|---|---|---|
| `id` | `str` | Identificador del perfil. |
| `tutor_id` | `str` | UID de Firebase del padre/tutor propietario (1-128 caracteres). |
| `nombre` | `str` | Nombre del nino/a (1-60 caracteres). |
| `edad` | `int` | Entre 6 y 14 anios. Dato declarado por el tutor, no calculado. |
| `sexo` | `Sexo` | Enum. |
| `peso_kg` | `float` | > 0 y <= 200. |
| `estatura_cm` | `float` | > 0 y <= 250. |
| `nivel_actividad_fisica` | `NivelActividadFisica` | Enum. |
| `habitos_alimenticios` | `str or None` | Texto libre (<= 500). `None` si no se declaro. |
| `alergias` | `tuple[str, ...]` | Cada item <= 50 caracteres. Maximo 30 items. Vacia si no hay. |
| `objetivos` | `str or None` | Texto libre (<= 500). `None` si no se declaro. |

**No expuestos (internos):** `activo`, `creado_en`, `actualizado_en`.

### 4. `PerfilInfantilPort` (interfaz ofrecida)

| Metodo | Entrada | Salida | Semantica |
|---|---|---|---|
| `obtener_por_id` | `perfil_id: str` | `PerfilInfantilDTO or None` | Devuelve el perfil si existe y esta activo; `None` si no. |
| `listar_por_tutor` | `tutor_id: str` | `list[PerfilInfantilDTO]` | Perfiles activos del tutor; lista vacia si no tiene. |
| `existe` | `perfil_id: str` | `bool` | `True` si existe y esta activo. |

Todos son `async` (FastAPI + Motor son asincronos).
El puerto se declara con `typing.Protocol` (tipado estructural): los adapters
**no heredan** nada.

### 5. Errores

En esta version el puerto **no lanza excepciones de dominio**: usa
`None` / lista vacia / `False`.

### 6. Politica de compatibilidad

- Aniadir campos **opcionales** al DTO es no-breaking.
- Aniadir metodos al puerto es no-breaking para consumidores, si para
  implementaciones existentes -> se anunciara con antelacion en `PROGRESS.md`.
- Renombrar o eliminar campos/metodos es **breaking** y requiere bump de
  version mayor del contrato.

### 7. Fuera del contrato

- Calculo de IMC (responsabilidad del Modulo 2 / Franco).
- Reglas nutricionales o de ejercicios.
- Persistencia fisica de MongoDB Atlas. No forma parte de este puerto.
  El modelo de la coleccion esta en "Persistencia interna — perfiles_infantiles".
  Los modulos 2 y 3 siguen sin importar `adapters`.

---

## Modulo 1 - Endpoints base (Fase 2)

- **Version:** 2.0
- **Fecha:** 2026-09-15
- **Rama:** `feature/modulo1-fastapi-skeleton`

### 1. Arranque del backend

    cd backend
    uvicorn app.main:app --reload

Al levantar, el lifespan:
1. Inicializa Firebase Admin con `FIREBASE_SERVICE_ACCOUNT_PATH`.
2. Abre cliente `motor` contra `MONGODB_URI` y hace `ping`.
3. Asegura el validador y el indice de `perfiles_infantiles`.

Si cualquiera de los dos primeros falla, la app no arranca. Si el tercero
falla (permisos insuficientes sobre la coleccion), la app tampoco arranca.

### 2. Endpoints publicos

| Metodo | Ruta | Auth | Respuesta |
|---|---|---|---|
| GET | `/` | No | `{"service": "CreceActivo backend", "version": "..."}` |
| GET | `/modulo1/health` | No | `{"status": "ok", "env": "...", "db": "ok"}` |

`db` es `ok` si el ping a Mongo respondio; `error` si no.

### 3. Endpoints protegidos (Bearer Firebase)

| Metodo | Ruta | Auth | Respuesta |
|---|---|---|---|
| GET | `/modulo1/whoami` | Si | `{"uid": "...", "email": "..."}` |

Header esperado: `Authorization: Bearer <idToken>`.
Token ausente, invalido o expirado -> 401.

### 4. Variables de entorno (backend)

| Variable | Obligatoria | Descripcion |
|---|---|---|
| `MONGODB_URI` | Si | URI de MongoDB Atlas. |
| `MONGODB_DB_NAME` | No (default `creceactivo`) | Nombre de la base. |
| `FIREBASE_PROJECT_ID` | Si | Project ID de Firebase. |
| `FIREBASE_SERVICE_ACCOUNT_PATH` | Si | Ruta ABSOLUTA al JSON del service account, fuera del repo. |
| `CORS_ORIGINS` | No (default `http://localhost:5173`) | Origenes permitidos, separados por coma. |
| `APP_ENV` | No (default `development`) | Se expone en `/modulo1/health`. |

### 5. Fuera de esta fase

- CRUD de `PerfilInfantil` (Fase 3, endpoints `/modulo1/perfiles`).
- Repositorio Mongo que implemente `PerfilInfantilPort`.
- Despliegue a Cloud Run.

---

## Persistencia interna — perfiles_infantiles

- **Version:** 1.0
- **Fecha:** 2026-09-22
- **Rama:** `feat/mod1-esquema-perfiles`
- **Dueno:** base de datos, Modulo 1
- **Codigo:** `app.modulo1_usuarios.adapters.db.perfiles_infantiles`

Esta seccion describe la coleccion. No es una superficie de importacion.
Modulos 2 y 3 siguen leyendo perfiles solo por `PerfilInfantilPort`.

### 1. Coleccion

Nombre: `perfiles_infantiles`.

`_id` es un string UUID (no ObjectId). `tutor_id` es el UID de Firebase
del tutor (1 a 128 caracteres); no es un UUID. Un tutor puede tener varios
perfiles: no hay indice unico sobre `tutor_id`.

`edad` es un entero de 6 a 14 declarado por el tutor. No se guarda
`fecha_nacimiento`. La edad queda desactualizada hasta que el tutor la
edite. El Modulo 2 agrupa menus y guias por `rango_edad` ("6-8 años",
"9-11 años", "12-14 años") a partir de ese entero.

Campos obligatorios, siempre presentes:

- `_id`, `tutor_id`, `nombre`, `edad`, `sexo`, `peso_kg`, `estatura_cm`,
  `nivel_actividad_fisica`
- `habitos_alimenticios` y `objetivos`: string de 1 a 500 caracteres, o `null`
- `alergias`: array de strings (cada uno de 1 a 50 caracteres, maximo 30 items)
- `activo`: bool de borrado logico
- `creado_en` y `actualizado_en`: fecha BSON en UTC

No se admiten campos extra (`additionalProperties: false`). Los limites
coinciden con las constantes de `PerfilInfantil`.

### 2. Validador

`$jsonSchema` con `validationLevel: strict` y `validationAction: error`.
Se aplica al arrancar con `asegurar_perfiles_infantiles`, despues del ping:

- si la coleccion no existe, se crea con el validador;
- si ya existe, `collMod` actualiza el validador.

Los documentos ya cargados que no cumplan no se borran. Un update
posterior falla hasta corregirlos.

### 3. Indice

`idx_perfiles_tutor_activo` sobre `tutor_id`, parcial, con
`partialFilterExpression: { activo: true }`.

Cubre `listar_por_tutor`, que solo devuelve perfiles activos, y deja
fuera los borrados logicos. `_id` sigue siendo el unico indice unico.

### 4. Checklist operativo de Atlas

No esta en el codigo. Quien administra el cluster lo verifica:

- la URI usa `mongodb+srv` (TLS);
- el cluster tiene cifrado en reposo;
- el usuario de la app tiene `readWrite` solo sobre la base `creceactivo`,
  no `atlasAdmin`;
- la lista de IPs del cluster no queda abierta a `0.0.0.0/0` en produccion.

La regla "un tutor solo ve a sus hijos" es de la aplicacion (Fase 3), no
del validador. No hay cifrado campo a campo en esta fase.

### 5. Convencion para colecciones futuras

Cuando el Modulo 2 o el 3 necesiten una coleccion, se acuerda asi antes
de cargarla:

- nombre en snake_case, en espanol y en plural (`perfiles_infantiles`);
- `_id` string UUID, salvo que haya una clave natural ya acordada;
- `creado_en` y `actualizado_en` como fecha UTC cuando el documento cambia;
- borrado logico con `activo` (bool) si la coleccion no es solo de
  referencia;
- validador `$jsonSchema` e indices declarados juntos en
  `adapters/db`, y asegurados al arrancar;
- las constantes de limite viven en el dominio del modulo; el esquema
  las importa, no las duplica.

Pendiente de revisar en conjunto, sin tocar la rama del Modulo 2: el
PR #3 inserta en `menus` y `specialists` sin validador y con nombres en
ingles. Cuando se alineen, se les aplica esta convencion.


---

## Módulo 2 — Nutrición y orientación profesional

- **Version:** 1.0
- **Fecha:** 2026-10-14
- **Rama:** `feat/mod2-backend-franco`
- **Ruta publica (unica permitida para Modulos 1 y 3):**
  `app.modulo2_nutricion.ports.contenido_nutricional_port`

### 1. Regla de dependencias (no negociable)

- Modulos 1 y 3 **importan solo** desde `modulo2_nutricion.ports.contenido_nutricional_port`.
- **Prohibido** importar `modulo2_nutricion.service`, `modulo2_nutricion.adapters.*`
  o `modulo2_nutricion.domain.*` desde fuera del Modulo 2.
- Internamente: `domain` no depende de `ports` ni `adapters`; `ports` depende
  solo de `domain`; `adapters` depende de `ports` y `domain`.

### 2. Enums publicos

**`RangoEdad`**

| Valor |
|---|
| `6-8 años` |
| `9-11 años` |
| `12-14 años` |

**`TipoComida`**

| Valor |
|---|
| `Desayuno` |
| `Almuerzo` |
| `Cena` |
| `Merienda` |

### 3. DTOs publicos (read-models)

**`GuiaDTO`**

| Campo | Tipo | Descripcion |
|---|---|---|
| `id` | `str` | Identificador UUID de la guia. |
| `titulo` | `str` | 1-120 caracteres. |
| `categoria` | `str` | Ej: Alimentacion, Habitos, Meriendas. |
| `rango_edad` | `RangoEdad` | Enum. |
| `contenido` | `str` | Texto validado por profesionales, 1-5000 caracteres. |
| `habitos_clave` | `tuple[str, ...]` | Cada uno 1-200 caracteres, maximo 10. |

**`PlatoDTO`**

| Campo | Tipo | Descripcion |
|---|---|---|
| `nombre` | `str` | 1-100 caracteres. |
| `descripcion` | `str` | 1-300 caracteres. |
| `calorias_aprox` | `int` | Mayor o igual a 0. |
| `ingredientes` | `tuple[str, ...]` | Cada uno 1-80 caracteres, minimo 1. |

**`MenuDTO`**

| Campo | Tipo | Descripcion |
|---|---|---|
| `id` | `str` | Identificador UUID del menu. |
| `titulo` | `str` | 1-120 caracteres. |
| `rango_edad` | `RangoEdad` | Enum. |
| `tipo_comida` | `TipoComida` | Enum. |
| `platos` | `tuple[PlatoDTO, ...]` | Minimo 1. |
| `recomendaciones` | `tuple[str, ...]` | Cada uno 1-200 caracteres. |

**`EspecialistaDTO`**

| Campo | Tipo | Descripcion |
|---|---|---|
| `id` | `str` | Identificador UUID del especialista. |
| `nombre_completo` | `str` | 1-100 caracteres. |
| `rol` | `str` | Nutricionista, Pediatra o Entrenador. |
| `especialidad` | `str` | 1-100 caracteres. |
| `experiencia_anios` | `int` | Mayor o igual a 0. |
| `biografia` | `str` | 1-1000 caracteres. |
| `contacto_email` | `str` | Email valido. |
| `disponible` | `bool` | Default `true`. |

### 4. ContenidoNutricionalPort (interfaz ofrecida)

| Metodo | Entrada | Salida | Semantica |
|---|---|---|---|
| `listar_guias` | `rango_edad: RangoEdad or None` | `list[GuiaDTO]` | Guias activas; filtro opcional por rango. Lista vacia si no hay. |
| `obtener_guia` | `guia_id: str` | `GuiaDTO or None` | La guia si existe y esta activa; None si no. |
| `listar_menus` | `rango_edad, tipo_comida` (opcionales) | `list[MenuDTO]` | Menus activos; filtros opcionales. |
| `obtener_menu` | `menu_id: str` | `MenuDTO or None` | El menu si existe y esta activo; None si no. |
| `listar_especialistas` | — | `list[EspecialistaDTO]` | Especialistas disponibles. |
| `crear_solicitud_orientacion` | `tutor_id, perfil_id, especialista_id, mensaje` | `str` (id) | Crea la solicitud; devuelve su id. |

Todos son `async` (FastAPI + Motor son asincronos).
El puerto se declara con `typing.Protocol` (tipado estructural): los adapters
**no heredan** nada.

### 5. Errores

En lectura el puerto no lanza excepciones de dominio: usa `None` / lista vacia.
`crear_solicitud_orientacion` puede lanzar `PerfilNoEncontrado` o
`EspecialistaNoEncontrado` si las referencias no existen.

### 6. Politica de compatibilidad

Misma que el Modulo 1:

- Aniadir campos **opcionales** al DTO es no-breaking.
- Aniadir metodos al puerto es no-breaking para consumidores, si para
  implementaciones existentes.
- Renombrar o eliminar campos/metodos es **breaking** y requiere bump de
  version mayor del contrato.

### 7. Fuera del contrato

- Calculo de IMC (Fase 2, con tablas de percentiles OMS).
- Chatbot con Google Gemini (diferido, sin API key en esta entrega).
- Reglas de ejercicios (responsabilidad del Modulo 3).

---

## Modulo 2 — Endpoints base

- **Version:** 1.0
- **Fecha:** 2026-10-14

### 1. Endpoints publicos

| Metodo | Ruta | Auth | Respuesta |
|---|---|---|---|
| GET | /modulo2/health | No | status ok, env, db |
| GET | /modulo2/guias | No | Lista de GuiaDTO |
| GET | /modulo2/guias/id | No | GuiaDTO o 404 |
| GET | /modulo2/menus | No | Lista de MenuDTO |
| GET | /modulo2/menus/id | No | MenuDTO o 404 |
| GET | /modulo2/especialistas | No | Lista de EspecialistaDTO |

### 2. Endpoints protegidos (Bearer Firebase)

| Metodo | Ruta | Auth | Respuesta |
|---|---|---|---|
| POST | /modulo2/solicitudes | Si | id, estado pendiente |

Body esperado: perfil_id, especialista_id, mensaje de 1 a 1000 caracteres.

### 3. Filtros opcionales

- GET /modulo2/guias con parametro rango_edad
- GET /modulo2/menus con parametros rango_edad y tipo_comida


---

## Persistencia interna — colecciones del Modulo 2

- **Version:** 1.0
- **Fecha:** 2026-10-14
- **Dueno:** base de datos, Modulo 2
- **Codigo:** app.modulo2_nutricion.adapters.db

Esta seccion describe las colecciones. No es una superficie de importacion.
Modulos 1 y 3 siguen leyendo contenido solo por ContenidoNutricionalPort.

### 1. Colecciones

| Coleccion | Descripcion |
|---|---|
| guias_nutricionales | Guias de alimentacion validadas |
| menus_infantiles | Menus por rango de edad y tipo de comida |
| especialistas | Nutricionistas, pediatras y entrenadores |
| solicitudes_orientacion | Solicitudes de tutores a especialistas |

Todas siguen la convencion del Modulo 1: nombre en snake_case, espanol y
plural; id string UUID; activo bool para borrado logico cuando aplica;
creado_en y actualizado_en UTC.

### 2. Validadores

Todos con jsonSchema, validationLevel strict, validationAction error.
Se aseguran al arrancar con asegurar_colecciones_modulo2.

### 3. Indices

| Coleccion | Indice | Campos | Filtro |
|---|---|---|---|
| menus_infantiles | idx_menus_rango_tipo | rango_edad, tipo_comida | activo true |
| guias_nutricionales | idx_guias_rango | rango_edad | activo true |
| especialistas | idx_especialistas_disponible | disponible | ninguno |
| solicitudes_orientacion | idx_solicitudes_tutor | tutor_id | ninguno |

### 4. Alineacion con el Modulo 1

El seed original (seed_mod2.py, PR 3) insertaba en menus y specialists
con nombres en ingles y sin validador. Esta version renombra a
menus_infantiles y especialistas y anade validadores e indices.


---

## Módulo 3 — Storage de videos, versión 1.0

Responsable: Kevin Peña Jamachi. Ruta pública:
`app.modulo3_ejercicios.ports.video_storage_port`.

`VideoStoragePort` expone `subir_video(Path, GrupoEdad, UUID)` y
`obtener_acceso(GrupoEdad, UUID)` (async). La carga es administrativa; el API
solo entrega lectura temporal a tutores autenticados. Objetos educativos en
`modulo3/videos/{grupo_edad}/{uuid}.mp4`, sin datos de menores.

API: `GET /modulo3/videos/{grupo_edad}/{video_id}/url`, Bearer Firebase.
Devuelve `url` y `expires_at`. Mongo guarda `storage_path`, no URLs temporales.
Consultar `docs/modulo3_storage.md` para errores, configuración e integración.
