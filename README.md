# CreceActivo

Proyecto de impacto social — plataforma educativa que ayuda a familias a prevenir el sedentarismo y la obesidad infantil mediante hábitos saludables, sin dietas estrictas ni diagnósticos médicos.

Plataforma web para prevenir el sedentarismo y la obesidad infantil (6-14 años), con guías de nutricionistas y entrenadores, gestionada por padres/tutores.

## Equipo
- **Líder general:** Antonio

### Módulo 1 — Usuarios y perfil infantil
Sublíder: Antonio · Natalia · Nicolás · David Bazo

### Módulo 2 — Nutrición y orientación profesional
Sublíder: Juanpi · Matt · Patrick · Franco

### Módulo 3 — Ejercicios, progreso y motivación
Sublíder: Allen · Kevin · David L.

## Stack tecnológico
| Capa | Tecnología |
|---|---|
| Frontend | React + Tailwind CSS |
| Backend | Python + FastAPI |
| Base de datos | MongoDB (Atlas) |
| Storage | Firebase Storage |
| Autenticación | Firebase Auth |
| Chatbot | Google Gemini API |
| Hosting frontend | Vercel |
| Hosting backend | Google Cloud Run |

## Arquitectura
Monolito modular con arquitectura hexagonal (puertos y adaptadores). Cada módulo (`modulo1_usuarios`, `modulo2_nutricion`, `modulo3_ejercicios`) expone su funcionalidad a través de `ports/`, y los demás módulos consumen esos puertos mediante `adapters/`, nunca importando código interno de otro módulo directamente.

Detalle de los contratos entre módulos: ver `docs/contratos.md`.

## Ramas
- `main`: protegida, solo recibe merges vía Pull Request desde `dev`.
- `dev`: rama de integración.
- Ramas de trabajo: `feat/mod{N}-nombre-corto`, `fix/mod{N}-nombre-corto`, etc.

## Estado del proyecto
Ver `PROGRESS.md` para el estado actual, decisiones tomadas y próximos pasos.
