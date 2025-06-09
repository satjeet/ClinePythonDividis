import { computed } from 'vue';
import { useModulesStore } from '@/stores/modules';

// Mapeo de id de módulo a icono FontAwesome
export const iconMap: Record<string, string> = {
  salud: 'fas fa-heartbeat',
  personalidad: 'fas fa-user-astronaut',
  intelecto: 'fas fa-brain',
  carrera: 'fas fa-rocket',
  finanzas: 'fas fa-coins',
  'calidad-vida': 'fas fa-star',
  emocionalidad: 'fas fa-spa',
  relaciones: 'fas fa-users',
  vision: 'fas fa-eye'
};

export function useConstellationsAreas() {
  const modulesStore = useModulesStore();

  const areas = computed(() =>
    modulesStore.modules.map(mod => ({
      id: mod.id, // <-- AÑADIDO: id real para navegación
      name: mod.name,
      icon: iconMap[mod.id] || 'fas fa-star',
      active: mod.id === 'salud' ? true : (mod.state === 'unlocked' || mod.state === 'completed')
    }))
  );

  return { areas };
}
