<template>
  <div class="rank-stars cosmic-card mb-4 flex flex-col items-center">
    <h2 class="font-semibold mb-2">Rango y Estrellas</h2>
    <div v-if="safeTotalStars === 0" class="text-gray-400 text-sm mb-2">
      Aún no tienes estrellas. ¡Entrena tus hábitos para ganar estrellas!
    </div>
    <div v-else class="flex flex-col items-center">
      <div class="flex gap-1 mb-1">
        <span v-for="n in Math.max(0, Math.floor(safeTotalStars))" :key="n" class="text-yellow-400 text-2xl">★</span>
        <span v-if="safeTotalStars % 1 >= 0.5" class="text-yellow-400 text-2xl">☆</span>
      </div>
      <div class="text-xs text-white font-bold mb-1">Total: {{ safeTotalStars }} estrellas</div>
      <div class="text-xs text-blue-400">Rango: {{ rankLabel }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useHabitStore } from './stores/habitStore'

const habitStore = useHabitStore()
const safeHabits = computed(() => Array.isArray(habitStore.habits) ? habitStore.habits : [])
const safeTotalStars = computed(() =>
  safeHabits.value.reduce((sum, h) => sum + (typeof h.estrellas === 'number' ? h.estrellas : 0), 0)
)

const rankLabel = computed(() => {
  if (safeTotalStars.value >= 10) return 'Maestro'
  if (safeTotalStars.value >= 5) return 'Avanzado'
  if (safeTotalStars.value >= 2) return 'Aprendiz'
  if (safeTotalStars.value > 0) return 'Novato'
  return 'Sin rango'
})
</script>

<style scoped>
.rank-stars {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
</style>
