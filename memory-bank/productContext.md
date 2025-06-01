# Product Context

## Purpose
Dividis impulsa a los usuarios a estructurar y alcanzar metas personales organizando declaraciones en ocho áreas fundamentales de la vida (Salud, Personalidad, Intelecto, Carrera, Finanzas, Calidad de Vida, Emocionalidad y Relaciones), cada una con cuatro pilares (Visión, Propósito, Creencias, Estrategias). La aplicación convierte la auto-mejora en una experiencia atractiva y sostenible a través de gamificación, interacción social y una narrativa cósmica única.

## Target Audience
- **Usuarios principales**: Personas de 18 a 40 años que buscan un crecimiento personal estructurado, se sienten motivadas por experiencias gamificadas y valoran la auto-mejora. Son usuarios digitales y aprecian la motivación colectiva.
- **Usuarios secundarios**: Coaches, mentores o líderes de equipos que guían procesos de desarrollo personal y pueden utilizar Dividis para dar seguimiento al progreso de sus clientes o equipos.
- **Alcance global**: Con énfasis en usuarios hispanohablantes que desean diseñar su vida a través de declaraciones y una experiencia visual cósmica.

## User Experience Goals
- **Inmersiva y motivadora**: Los usuarios se sentirán como viajeros estelares en una odisea cósmica, con el Galactic Dashboard como centro de mando, promoviendo la interacción diaria mediante una interfaz visualmente impactante y temática.
- **Estructurada e intuitiva**: El sistema de categorías y pilares debe ser claro y fácil de navegar, permitiendo crear declaraciones y visualizar el progreso sin fricción, aprovechando rutas dinámicas en Vue.js.
- **Gamificada y gratificante**: Completar misiones diarias/semanales y ganar XP por declaración debe sentirse significativo, con mensajes motivacionales personalizados (“¡Tu visión de Salud brilla como una supernova!”) y visualizaciones de progreso llamativas.
- **Comunidad y pertenencia**: La interacción social (reacciones y compartir avances) debe fortalecer el sentido de pertenencia y motivación, fomentando el apoyo entre viajeros cósmicos.
- **Fiable y en tiempo real**: Sincronización instantánea de datos entre frontend y backend mediante WebSockets o polling eficiente, garantizando acceso inmediato a información y misiones.
- **Mobile-first**: Experiencia priorizada para móviles, con interfaz limpia, táctil y responsiva, construida íntegramente con Tailwind CSS.

---

## Cosmic Narrative

### Premisa
Cada usuario es un **Navegante Cósmico** que emprende un viaje a través de una galaxia personal llamada **Dividis Universum**. Esta galaxia contiene ocho constelaciones, cada una representando una de las áreas vitales de la vida: Salud, Personalidad, Intelecto, Carrera, Finanzas, Calidad de Vida, Emocionalidad y Relaciones. En el centro de la galaxia brilla una estrella guía, la **Visión Estelar**, que representa el propósito y la dirección única del usuario. El viaje consiste en explorar cada constelación, completar misiones y recolectar Reliquias Cósmicas (herramientas personalizadas) para construir una vida plena.

### Estructura de la Narrativa

#### Punto de Partida: El Observatorio Cósmico
El usuario comienza en un observatorio estelar, donde define su **Visión Estelar** (su propósito o visión de vida ideal). Esto actúa como el núcleo que guía todas las decisiones y misiones.

- **Actividad inicial:** Completar un cuestionario interactivo para establecer creencias, valores y metas que formen la Visión Estelar. Por ejemplo, un formulario gamificado donde el usuario "enciende" su estrella respondiendo preguntas clave.

#### Las Ocho Constelaciones (Áreas Vitales)
Cada constelación está custodiada por un **Guía Cósmico**, una figura mística que personifica el espíritu del área (por ejemplo, un Guardián de la Vitalidad para Salud, o un Arquitecto de Conexiones para Relaciones).

Cada constelación incluye:
- **Misiones semanales:** Tareas específicas diseñadas para mejorar esa área (por ejemplo, en Salud: "Camina 10,000 pasos diarios durante 5 días").
- **Desafíos Dividis:** Retos más complejos que integran varias áreas (por ejemplo, "Organiza una cena con amigos" para Relaciones y Calidad de Vida).
- **Reliquia Cósmica:** Una herramienta personalizada que el usuario desbloquea al completar misiones clave (por ejemplo, la Serpiente de Hábitos para Salud, un rastreador visual de hábitos).

---

## Module Experience Design

Cada área vital se desbloquea al alcanzar ciertos hitos, y al hacerlo, el usuario accede a herramientas especializadas que potencian su desarrollo en esa dimensión:

1. **Salud (Serpiente de Hábitos)**
   - Seguimiento visual de hábitos
   - Marcadores de racha diaria
   - Visualización de progreso
   - *Desbloqueable*: Tras completar el onboarding y primer objetivo de salud

2. **Personalidad (Diálogos Socráticos)**
   - Sistema de auto-reflexión guiada
   - Flujos de diálogo estructurados
   - Registro de insights personales
   - *Desbloqueable*: Al mantener una racha de hábitos saludables

3. **Intelecto**
   - Herramientas de análisis de creencias
   - Árboles lógicos visuales
   - Mapeo de ideas
   - *Desbloqueable*: Al completar reflexiones en personalidad

4. **Carrera (Box Time Manager)**
   - Gestión de tiempo y tareas
   - Priorización visual
   - Analítica de productividad
   - *Desbloqueable*: Al alcanzar hitos en intelecto

5. **Finanzas (Colecciones de Estrategias)**
   - Biblioteca de estrategias financieras
   - Seguimiento de implementación
   - Herramientas de fijación de metas
   - *Desbloqueable*: Al organizar tareas de carrera

6. **Calidad de Vida (Agradecimiento)**
   - Botón interactivo de gratitud
   - Feedback visual positivo
   - Seguimiento de gratitud
   - *Desbloqueable*: Al cumplir metas financieras

7. **Emocionalidad (Timer de Meditación)**
   - Temporizador de meditación guiada
   - Seguimiento de sesiones
   - Historial de prácticas
   - *Desbloqueable*: Al mantener prácticas de gratitud

8. **Relaciones**
   - Calendario de eventos y citas
   - Herramientas de gestión de relaciones
   - Historial de interacciones
   - *Desbloqueable*: Al completar sesiones de meditación

9. **Visión General (Pizarra de Sueños)**
   - Visual goal board
   - Seguimiento de progreso global
   - Marcado de hitos y celebración de logros
   - *Desbloqueable*: Al desbloquear todas las áreas anteriores

---

## Gamification Mechanics

- **Progresión infinita**: Sin límite máximo de nivel ni XP, para motivar la exploración continua.
- **Curva de progresión**: Cada nivel requiere XP incremental: +10% por nivel hasta el 10, +5% hasta el 40, +2% hasta el 100.
- **Bonificaciones de XP por constancia**: 10% extra de XP por cada día consecutivo escribiendo en la bitácora (máx. 50% al quinto día). Completar todas las misiones diarias de una semana otorga badge “Racha Estelar”.
- **Badges y recompensas**: Badges visuales por hitos y rachas, con mensajes motivacionales.
- **Personalización de títulos**: Jerarquía de títulos por nivel (Navegante Novato → Explorador Estelar → Guardián Cósmico → Maestro Estelar). Al alcanzar hitos, el usuario puede personalizar su título mediante una reflexión.
- **Hitos visuales y marcos estelares**: En niveles clave se desbloquean marcos visuales y efectos progresivos para el dashboard.
- **Misiones**: Hasta 3 diarias y 2 semanales, rotando entre áreas activas. Sistema de guardado de misiones favoritas.
- **Eventos galácticos**: Misiones narrativas recurrentes (ej. “Festival Estelar” semanal, “Eclipse de Reflexión” mensual). Notificaciones integradas en el dashboard.
- **Accesibilidad**: Animaciones y efectos visuales pueden desactivarse para mejorar la experiencia en dispositivos de bajo rendimiento.

---

## Integración en el Dashboard

- **Interfaz Visual:** Dashboard con mapa estelar interactivo; cada constelación es un nodo clickable que despliega misiones, progreso y narrativa del Guía Cósmico.
- **Onboarding Galáctico:** Animación de bienvenida que lleva al Observatorio Cósmico para definir la Visión Estelar.
- **Log de Avances:** Gráfico dinámico que muestra el progreso como un firmamento en expansión.
- **Notificaciones Narrativas:** Alertas presentadas como mensajes de los Guías Cósmicos.
- **Experiencia Galáctica:** Elementos visuales neon y estética espacial, con temas de color seleccionables.
- **Galería Pública:** Los usuarios pueden compartir sus progresos en una galería pública dentro de la app.

---

## Key Features

- **Bienvenida e inicio de viaje:** Página de bienvenida con narrativa visual y acceso al login.
- **Galactic Dashboard:** Visualización central de progreso, acceso a áreas desbloqueadas, bitácora galáctica.
- **Componente "Iniciar Viaje":** Permite al usuario comenzar su camino haciendo declaraciones en cada área.
- **Gestión de declaraciones:** Crear y administrar declaraciones ligadas a categoría y pilar, con XP por declaración.
- **Sistema Categoría-Pilar:** Ocho áreas vitales, cada una con cuatro pilares, accesibles mediante rutas dinámicas en Vue.js.
- **Gamificación:** Misiones diarias/semanales, sistema de XP, desbloqueo secuencial de pilares y mensajes motivacionales.
- **Interacciones sociales:** Reacciones a declaraciones y compartir progreso; todo almacenado en la base de datos del backend.
- **Cosmic UI y temas neon:** Interfaz dark-mode y mobile-first con Tailwind CSS, componentes personalizados y soporte para temas espaciales neon.
- **Autenticación:** Inicio de sesión con email y contraseña, gestión segura de sesiones JWT.
- **Gestión segura de secretos:** Uso de variables de entorno para proteger claves y configuración sensible.

---

## Success Metrics
- **Engagement**: Promedio de logins diarios por usuario, tiempo en cada módulo, uso de features clave.
- **Crecimiento de declaraciones**: Porcentaje de usuarios que crean declaraciones semanalmente.
- **Misiones completadas**: Tasa de finalización de misiones diarias y semanales.
- **Retención**: Porcentaje de usuarios activos a 30 días.
- **Interacción social**: Porcentaje de declaraciones con al menos una reacción.
- **Performance**: Carga de página <2s y latencia de API <500ms.
- **Satisfacción**: NPS ≥ 7 (encuestas in-app).

---

## Notes
- **Balance de gamificación**: Ajustar recompensas y dificultad según feedback y métricas.
- **Cultural y accesibilidad**: Mensajes y UI adaptados al español natural y motivador; componentes accesibles y probados con screen readers.
- **Escalabilidad**: Planificar desde el inicio el uso eficiente de la base de datos y caché para minimizar costos y mantener rendimiento.
- **Temática visual**: Los temas neon deben ofrecer variedad y reforzar la inmersión cósmica, probando su consistencia y legibilidad en todos los dispositivos.
- **Sin tests automáticos (v1.0)**: Validación manual documentada en el Memory Bank.
- **Integración analítica**: Uso de herramientas de analítica compatibles con Django/Vue para eventos clave y mejora continua.
