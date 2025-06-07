/**
 * ConstellationsMap.ts
 * Lógica y props para la visualización de constelaciones vitales.
 * Preparado para recibir datos de estado de áreas como prop en el futuro.
 */

import { ref } from 'vue'

/**
 * Áreas vitales mock para el mapa de constelaciones.
 */
const areas = ref([
  { name: 'Salud', icon: 'fas fa-heartbeat', active: true },
  { name: 'Personalidad', icon: 'fas fa-user-astronaut', active: false },
  { name: 'Intelecto', icon: 'fas fa-brain', active: false },
  { name: 'Carrera', icon: 'fas fa-rocket', active: false },
  { name: 'Finanzas', icon: 'fas fa-coins', active: false },
  { name: 'Calidad de Vida', icon: 'fas fa-star', active: false },
  { name: 'Emocionalidad', icon: 'fas fa-spa', active: false },
  { name: 'Relaciones', icon: 'fas fa-users', active: false }
])

defineExpose({
  areas
})
