# Contratos entre módulos

Este documento registra las interfaces (`ports`) que cada módulo expone hacia los demás, para que cualquiera pueda programar contra el contrato sin necesidad de leer el código interno del otro módulo.

## Módulo 1 — Usuarios y perfil infantil
_(por definir)_

## Módulo 2 — Nutrición y orientación profesional
_(por definir)_

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
| `tutor_id` | `str` | UID de Firebase del padre/tutor propietario. |
| `nombre` | `str` | Nombre del nino/a (1-60 caracteres). |
| `edad` | `int` | Entre 6 y 14 anios. |
| `sexo` | `Sexo` | Enum. |
| `peso_kg` | `float` | > 0 y <= 200. |
| `estatura_cm` | `float` | > 0 y <= 250. |
| `nivel_actividad_fisica` | `NivelActividadFisica` | Enum. |
| `habitos_alimenticios` | `str or None` | Texto libre (<= 500). `None` si no se declaro. |
| `alergias` | `tuple[str, ...]` | Cada item <= 50 caracteres. Vacia si no hay. |
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
- Persistencia y detalles de MongoDB Atlas.
