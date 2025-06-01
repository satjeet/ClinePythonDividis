# Dividis Project Brief

## Project Overview
Dividis es una aplicación web de desarrollo personal integral, construida sobre Django REST Framework y Vue.js 3, que integra herramientas especializadas para potenciar el crecimiento en distintas áreas de la vida. El usuario progresa desbloqueando áreas y, con cada avance, accede a nuevas herramientas que lo ayudan a profundizar en su autodescubrimiento y mejora continua.

## Core Requirements

### Technical Stack
- Backend: Django REST Framework con PostgreSQL
- Frontend: Vue.js 3 con Pinia
- Despliegue: Docker, Fly.io
- Autenticación: JWT
- API: dividis-backend.fly.dev
- Frontend: dividis-frontend.fly.dev

### Key Features

1. **Authentication System**
   - Registro y login de usuarios
   - Gestión de tokens JWT

2. **Landing Page**
   - Diseño atractivo y enfocado en conversión
   - Propuesta de valor clara
   - Llamados a la acción para registro/login

3. **User Dashboard**
   - Hub central que conecta con nueve áreas clave de la vida
   - Progresión gamificada: las áreas y sus herramientas se desbloquean secuencialmente según el avance del usuario

#### Module Structure & Unlockable Tools

Cada área representa un módulo que se desbloquea al alcanzar ciertos hitos de progreso. Al desbloquear un área, el usuario accede a herramientas específicas que potencian su desarrollo en esa dimensión:

1. **Salud (Serpiente de Hábitos)**
   - Sistema de seguimiento de hábitos (habit tracker)
   - Visualización de progreso
   - *Desbloqueable*: Herramienta de hábitos tras completar el onboarding y primer objetivo de salud

2. **Personalidad (Diálogos Socráticos)**
   - Sistema de auto-reflexión guiada
   - Flujos de diálogo estructurados
   - *Desbloqueable*: Al mantener una racha de hábitos saludables

3. **Intelecto**
   - Simplificador de creencias
   - Árboles lógicos
   - Herramientas de análisis de ideas
   - *Desbloqueable*: Al completar reflexiones en personalidad

4. **Carrera (Box Time Manager)**
   - Gestión de tiempo y tareas
   - *Desbloqueable*: Al alcanzar hitos en intelecto

5. **Finanzas (Colecciones de Estrategias)**
   - Herramientas de planificación financiera
   - Sistema de colección de estrategias
   - *Desbloqueable*: Al organizar tareas de carrera

6. **Calidad de Vida (Agradecimiento)**
   - Botón interactivo de gratitud
   - Feedback visual positivo
   - *Desbloqueable*: Al cumplir metas financieras

7. **Emocionalidad (Timer de Meditación)**
   - Temporizador de meditación guiada
   - Seguimiento de sesiones
   - *Desbloqueable*: Al mantener prácticas de gratitud

8. **Relaciones**
   - Calendario de citas
   - Herramientas de gestión de relaciones
   - *Desbloqueable*: Al completar sesiones de meditación

9. **Visión General (Pizarra de Sueños)**
   - Visualización de metas y sueños
   - Seguimiento de progreso global
   - *Desbloqueable*: Al desbloquear todas las áreas anteriores

## Project Structure
```
dividis/
├── backend/           # Django REST Framework API
├── frontend/          # Vue.js + Pinia frontend
├── memory-bank/       # Documentación del proyecto
└── docker-compose.yml
```

## Development Guidelines
1. **Arquitectura Modular**
   - Separación clara entre backend y frontend
   - Despliegue independiente y containerizado

2. **Seguridad**
   - Autenticación JWT
   - Variables de entorno seguras
   - Configuración CORS

3. **Escalabilidad**
   - Diseño modular
   - Escalado independiente de módulos
   - Despliegue containerizado

4. **Documentación**
   - Memory Bank completo
   - Documentación de API y despliegue

## Success Criteria
1. Despliegue exitoso en Fly.io
2. Sistema de autenticación funcional
3. Módulos y herramientas desbloqueables operativos
4. Documentación completa en Memory Bank
5. Código listo para expansión de features

## Initial Development Phase
1. Configuración inicial del proyecto y documentación
2. Despliegue de infraestructura base
3. Implementación del sistema de autenticación
4. Creación de stubs de módulos y lógica de desbloqueo
5. Pruebas de integración y validación manual

---

**Nota:** El sistema de desbloqueo de módulos y herramientas refuerza la motivación del usuario, alineando el avance personal con el acceso a recursos cada vez más potentes y personalizados.
