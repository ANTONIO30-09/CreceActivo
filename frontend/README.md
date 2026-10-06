# Frontend del módulo 2

Primer avance de Mathew: React + Tailwind CSS + Vite. Requiere Node.js 22.12 o superior.

## Ejecutar

Desde `frontend/`:

```bash
npm install
npm run dev
```

Abrir la dirección que muestra Vite. Para generar el sitio: `npm run build`.

## Avance

- Catálogo de guías con búsqueda por título, filtros de edad/categoría y estado sin resultados.
- Vista de detalle de guía.
- Navegación entre guías, menús y orientación.
- Formulario de orientación con validación local; no envía ni guarda datos.
- Diseño adaptable a teléfono y escritorio, etiquetas y navegación por teclado.

Los datos de `src/demo.js` son fixtures y no contenido profesional validado. Sus campos siguen `GuiaNutricional` de la rama `feat/mod2-esquemas-mongodb`. Menús es una sección pendiente; no se implementan aún IMC, chatbot, autenticación ni conexión a FastAPI. No se inventaron endpoints: acordarlos con backend antes de reemplazar los fixtures.

## Integración

Esta carpeta es nueva y no modifica el backend. Integrar mediante una rama `feat/mod2-frontend-nutricion` y un Pull Request hacia `dev`, conforme al README general. Si otro compañero ya inició el frontend fuera del repositorio, coordinar la base antes de integrar.
