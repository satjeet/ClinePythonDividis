# Active Development Context

## Current Focus Areas

### 1. Frontend Development

- Implementación de la carga y edición del perfil de usuario
- Manejo de estados globales con Pinia
- Navegación y rutas protegidas
- Componentes reactivos para el dashboard
- Integración con el backend a través de servicios API

#### 2. Backend Development

- Endpoints REST para gestión de perfil y datos de usuario
- Serializers específicos para diferentes casos de uso
- Autenticación JWT y manejo de sesiones
- Sistema de misiones y progreso

#### 3. Data Management

- PostgreSQL para almacenamiento persistente
- Modelos Django para usuarios y progreso
- Caché y optimización de consultas

### Recent Implementations (2025-06-23)

- [VitalRadarChart.vue] Refactorización visual y responsiva, unificación de estilos con el dashboard, eliminación de restricciones de ancho y padding en mobile.
- [VitalRadarChart.ts] Ajuste dinámico de radius, center y fontSize para mejorar legibilidad de labels en todos los dispositivos.
- [VitalRadarChart.css] Limpieza de reglas, solo mantiene lo esencial para el gráfico.

### Recent Implementations (2025-06-11)

#### Edición de Perfil de Usuario

- Se implementó un endpoint dedicado `/api/auth/me/update/` con serializer específico
- El frontend ahora permite editar y visualizar email, nombre y apellido
- Sincronización bidireccional entre frontend y backend
- Los cambios se reflejan correctamente en Django admin
- Se mejoró el manejo de datos anidados vs planos en las respuestas del API

### Recent Implementations (2025-06-22)

- [SurveySummaryChart.vue] Nuevo componente para visualizar el resumen gráfico de encuestas de bienestar.
- [wellnessSurveyApi.ts] Servicio API para obtener y enviar respuestas de encuestas.

### Recent Implementations (2025-06-22)

- [serializers.py] Se agregó la inclusión de first_name y last_name en la respuesta del perfil de usuario, permitiendo que el frontend reciba y muestre correctamente estos campos tras actualizar el perfil.

#### Nueva Funcionalidad de Usuario

- Endpoint dedicado para actualización de perfil
- UserProfileUpdateSerializer para manejo específico
- Mejora en la UI de edición de perfil
- Sistema robusto de normalización de datos
- Compatibilidad con serializers existentes

#### Estado del Stack Técnico

- Frontend (Vue/Pinia): Componentes actualizados ✓
- Backend (Django/DRF): Endpoints optimizados ✓
- Base de datos: Persistencia verificada ✓
- Tests: Validación manual completa ✓

#### Aprendizajes Clave

- Los endpoints de perfil deben mantener consistencia en la estructura de datos
- El frontend debe ser resiliente a diferentes formatos de respuesta
- La separación de serializers por caso de uso mejora la mantenibilidad
- El manejo de estado global requiere normalización de datos consistente

##### Decisión sobre precarga global vs modular (2025-06-24)
- Se implementó infraestructura para precarga global tras login/refresh, pero se optó por mantener la carga de datos en cada módulo.
- La experiencia actual es estable y los módulos gestionan correctamente su propio estado y carga.
- La precarga global queda documentada y disponible para futuras necesidades, pero no se fuerza su uso para evitar riesgos en el flujo actual.

---

## Mejoras recientes en feedback de usuario y UI reactiva a theme

- Se implementó persistencia local (localStorage) para evitar mostrar mensajes emergentes de felicitación por misiones más de una vez por usuario, incluso tras cerrar sesión.
- Los mensajes emergentes (toasts) ahora adaptan su estilo visual dinámicamente según el theme global seleccionado por el usuario.
- Este patrón mejora la experiencia de usuario, evita duplicidad de feedback y refuerza la coherencia visual de la plataforma.

### Next Steps

1. Validar exhaustivamente el flujo de perfil en diferentes escenarios
2. Documentar el nuevo endpoint en la API
3. Considerar implementar validaciones adicionales de correo
4. Revisar la experiencia móvil del formulario de perfil

### Technical Debt

- Optimizar consultas al backend para reducir latencia
- Implementar manejo de errores más detallado
- Considerar cacheo de datos de perfil
- Evaluar necesidad de websockets para actualizaciones en tiempo real

### Active Issues

- None at the moment - recent profile editing implementation working as expected

### Documentation Needed

- Actualizar API docs con nuevo endpoint de perfil
- Documentar patrones de manejo de datos anidados
- Guía de mejores prácticas para actualización de perfil
- Documentar decisión de mantener carga modular y dejar la precarga global como infraestructura opcional.

### Estado de Módulos en Desarrollo

#### Módulo Salud

##### Actualización 2025-06-23

- Sistema de hábitos funcional y en uso, con integración visual tipo serpiente y sistema de rachas activo.
- Se completó la integración visual y la sincronización de progreso con el dashboard.
- El feedback visual inmediato y la gamificación están activos y validados.
- Pendiente: optimización de rendimiento en carga de datos y mejora de feedback visual/UX ante streak roto o hábitos fallidos.
- [Reemplaza: estado previo a 2025-06-23]

#### Sistema de Constelaciones

- Navegación entre módulos implementada
- Estado de desbloqueo sincronizado con backend
- Visualización de progreso funcionando
- Próximo: mejoras en las transiciones visuales

#### Sistema de Declaraciones

- Integración con módulos activa
- Persistencia y sincronización funcionando
- Editor de declaraciones optimizado
- Pendiente: sistema de tags y búsqueda
