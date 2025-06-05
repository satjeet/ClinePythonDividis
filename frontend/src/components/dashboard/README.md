# Galactic Dashboard Components

Esta carpeta contiene la estructura modular del Galactic Dashboard, siguiendo principios SOLID y separación de responsabilidades.

## Estructura

- **Dashboard.vue**  
  Componente principal, organiza la disposición general y orquesta los subcomponentes.

- **ExperienceBar/**  
  Barra de experiencia, nivel y título cósmico.

- **MotivationalMessage/**  
  Mensaje motivacional dinámico del Guía Cósmico.

- **VitalRadarChart/**  
  Radar chart de progreso en las 8 áreas vitales.

- **ConstellationsMap/**  
  Visualización de constelaciones vitales y su estado.

- **UserLog/**  
  Últimas declaraciones y misiones activas.

## Convenciones

- Cada subcomponente tiene:
  - `Componente.vue` (solo estructura y slots)
  - `Componente.ts` (lógica y props)
  - `Componente.css` (estilos scoped)
- Documentación en comentarios JSDoc en los scripts.
- Datos mock y props preparados para futura integración.

## Extensión

- Añadir nuevas secciones creando carpetas y siguiendo la misma convención.
- Integrar lógica real reemplazando los datos mock en los scripts.
