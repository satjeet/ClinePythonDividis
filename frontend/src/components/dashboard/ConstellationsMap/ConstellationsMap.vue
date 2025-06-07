<template>
  <!-- Mapa de constelaciones vitales -->
  <div class="constellations-map-root">
    <div class="flex flex-col items-center w-full">
      <h3 class="text-cosmic-300 font-bold mb-2">Constelaciones Vitales</h3>
      <div class="flex flex-wrap gap-4 justify-center">
        <div v-for="area in areas" :key="area.name" class="flex flex-col items-center">
          <template v-if="area.active">
            <router-link :to="{ name: 'constellation', params: { area: area.name } }"
              :class="[
                'w-14 h-14 flex items-center justify-center rounded-full border-4 text-2xl mb-1 cursor-pointer',
                area.active
                  ? 'bg-cosmic-400 border-cosmic-300 text-slate-950 shadow-lg animate-pulse'
                  : 'bg-slate-800 border-slate-600 text-slate-500 opacity-60'
              ]"
            >
              <i :class="area.icon"></i>
            </router-link>
          </template>
          <template v-else>
            <div
              :class="[
                'w-14 h-14 flex items-center justify-center rounded-full border-4 text-2xl mb-1',
                area.active
                  ? 'bg-cosmic-400 border-cosmic-300 text-slate-950 shadow-lg animate-pulse'
                  : 'bg-slate-800 border-slate-600 text-slate-500 opacity-60'
              ]"
            >
              <i :class="area.icon"></i>
            </div>
          </template>
          <span class="text-xs text-cosmic-200">{{ area.name }}</span>
          <span v-if="!area.active" class="text-xs text-slate-500"><i class="fas fa-lock"></i></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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
</script>
<style scoped src="./ConstellationsMap.css"></style>
