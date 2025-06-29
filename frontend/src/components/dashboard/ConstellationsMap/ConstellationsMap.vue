<template>
  <!-- Mapa de constelaciones vitales -->
  <div class="constellations-map-root">
    <div class="flex flex-col items-center w-full">
      <h3 class="font-bold mb-2" :style="{ color: 'var(--theme-border)' }">Constelaciones Vitales</h3>
      <div class="flex flex-wrap gap-4 justify-center">
        <div v-for="area in areas" :key="area.name" class="flex flex-col items-center">
          <template v-if="area.active">
            <router-link
              :to="{ name: 'constellation', params: { area: area.id } }"
              :class="[
                'w-14 h-14 flex items-center justify-center rounded-full border-4 text-2xl mb-1 cursor-pointer',
                area.active
                  ? 'shadow-lg animate-pulse'
                  : 'opacity-60'
              ]"
              :style="area.active
                ? {
                    background: 'var(--theme-accent)',
                    borderColor: 'var(--theme-border)',
                    color: 'var(--theme-accent-contrast, #181818)'
                  }
                : {
                    background: 'color-mix(in srgb, var(--theme-border) 10%, transparent 90%)',
                    borderColor: 'var(--theme-border)',
                    color: 'var(--theme-border)'
                  }"
            >
              <i :class="area.icon"></i>
            </router-link>
          </template>
          <template v-else>
            <div
              :class="[
                'w-14 h-14 flex items-center justify-center rounded-full border-4 text-2xl mb-1',
                area.active
                  ? 'shadow-lg animate-pulse'
                  : 'opacity-60'
              ]"
              :style="area.active
                ? {
                    background: 'var(--theme-accent)',
                    borderColor: 'var(--theme-border)',
                    color: 'var(--theme-accent-contrast, #181818)'
                  }
                : {
                    background: 'color-mix(in srgb, var(--theme-border) 10%, transparent 90%)',
                    borderColor: 'var(--theme-border)',
                    color: 'var(--theme-border)'
                  }"
            >
              <i :class="area.icon"></i>
            </div>
          </template>
          <span class="text-xs" :style="{ color: 'var(--theme-border)' }">{{ area.name }}</span>
          <span v-if="!area.active" class="text-xs" :style="{ color: 'var(--theme-border)' }"><i class="fas fa-lock"></i></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useConstellationsAreas } from './ConstellationsMap.ts';

const { areas } = useConstellationsAreas();
</script>
<style scoped src="./ConstellationsMap.css"></style>
