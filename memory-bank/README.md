# Documentación Técnica - Estado y Decisiones Clave (Junio 2025)

## Orden y lógica de pilares

- El flujo de pilares en cada constelación/área es SIEMPRE:
  1. Vision
  2. Proposito
  3. Creencias
  4. Estrategias
- El frontend garantiza este orden usando un array fijo y solo muestra como desbloqueados los que el backend indica, pero siempre en ese orden.

## Desbloqueo y Persistencia

- Los pilares desbloqueados se sincronizan con el backend usando el modelo UnlockedPillar.
- Al guardar una declaración en un pilar, se desbloquea automáticamente el siguiente pilar (si existe) y se guarda en el backend.
- Al recargar o volver a iniciar sesión, los pilares desbloqueados se consultan desde el backend y se muestran en el orden correcto.

## Declaraciones

- Las declaraciones se guardan y filtran por módulo (constelación) y pilar.
- El frontend mapea correctamente los nombres de los pilares para que el backend acepte solo los valores válidos (Vision, Proposito, Creencias, Estrategias).
- El modelo de declaración en backend requiere: user, module, pillar, text, created_at, updated_at, synced.

## UX y experiencia de usuario

- El usuario solo puede ver y escribir declaraciones en los pilares desbloqueados, y el orden visual nunca cambia.
- El sistema es persistente: el progreso se mantiene entre sesiones y dispositivos.
- El desbloqueo de pilares es automático y progresivo.

## Backend: Modelos y Endpoints relevantes

- **UnlockedPillar**: modelo que guarda el pilar desbloqueado por usuario y módulo.
- **/api/unlocked-pillars/**: endpoint para consultar y crear pilares desbloqueados.
- **/api/declarations/**: endpoint para consultar y crear declaraciones, filtrando por módulo y pilar.

## Ejemplo de integración frontend-backend

- El frontend consulta los pilares desbloqueados al cargar la vista de constelación y los muestra en el orden fijo.
- Al guardar una declaración, si corresponde, desbloquea el siguiente pilar y lo sincroniza con el backend.
- Las declaraciones se filtran por módulo y pilar para mostrar solo las relevantes en cada área.

## Próximos pasos sugeridos

- Permitir cambiar de constelación solo cuando se hayan desbloqueado todos los pilares de la actual (es decir, cuando haya al menos una declaración en cada pilar).
- Mejorar la navegación y feedback visual para el usuario al desbloquear nuevas constelaciones.

---

**Referencia:**  
Este README técnico se encuentra en `memory-bank/README.md`.  
Para información de onboarding y setup de nuevos desarrolladores, ver el README de la raíz del proyecto.
