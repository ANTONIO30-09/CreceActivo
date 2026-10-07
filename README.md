# CreceActivo

Proyecto de impacto social — plataforma educativa que ayuda a familias a prevenir el sedentarismo y la obesidad infantil mediante hábitos saludables, sin dietas estrictas ni diagnósticos médicos.

Plataforma web para prevenir el sedentarismo y la obesidad infantil (6-14 años), con guías de nutricionistas y entrenadores, gestionada por padres/tutores.

## Equipo

- **Líder general:** Antonio Vicente García Corrales

### Módulo 1 — Usuarios y perfil infantil

- Antonio Vicente García Corrales (sublíder) — Backend
- Natalia Camacho Cardozo — Frontend
- Pablo Nicolás Villazón Quiroga — Base de Datos
- David Ignacio Bazoberry Grigoriu — Backend y API

### Módulo 2 — Nutrición y orientación profesional

- Juan Pablo Villca Revollo (sublíder) — Backend
- Matthew Alejandro Gómez Torrez — Frontend
- Misael Patrick Ramos Torrez — Base de Datos
- Franco Guerra Roca — Backend y Migraciones

### Módulo 3 — Ejercicios, progreso y motivación

- Allen Jhonatan Requena Heredia (sublíder) — Frontend
- Kevin Peña Jamachi — Storage y Bucket
- Luis David Céspedes Camacho — Backend y Base de Datos

## Stack tecnológico

| Capa             | Tecnología           |
| ---------------- | -------------------- |
| Frontend         | React + Tailwind CSS |
| Backend          | Python + FastAPI     |
| Base de datos    | MongoDB (Atlas)      |
| Storage          | Firebase Storage     |
| Autenticación    | Firebase Auth        |
| Chatbot          | Google Gemini API    |
| Hosting frontend | Vercel               |
| Hosting backend  | Google Cloud Run     |

## Arquitectura

Monolito modular con arquitectura hexagonal (puertos y adaptadores). Cada módulo (`modulo1_usuarios`, `modulo2_nutricion`, `modulo3_ejercicios`) expone su funcionalidad a través de `ports/`, y los demás módulos consumen esos puertos mediante `adapters/`, nunca importando código interno de otro módulo directamente.

Detalle de los contratos entre módulos: ver `docs/contratos.md`.

## Ramas

- `main`: protegida, solo recibe merges vía Pull Request desde `dev`.
- `dev`: rama de integración.
- Ramas de trabajo: `feat/mod{N}-nombre-corto`, `fix/mod{N}-nombre-corto`, etc.

## Estado del proyecto

Ver `PROGRESS.md` para el estado actual, decisiones tomadas y próximos pasos.
