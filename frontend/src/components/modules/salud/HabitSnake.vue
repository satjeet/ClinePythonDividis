<template>
  <div class="habit-snake cosmic-card mb-4 flex flex-col items-center">
    <h2 class="font-semibold mb-2">Serpiente de Progreso</h2>
    <div v-if="safeActiveHabits.length === 0" class="text-gray-400 text-sm mb-2">
      No tienes hábitos activos. ¡Crea una serpiente en el Salón de Incubación!
    </div>
    <div v-else class="flex flex-wrap gap-2 justify-center">
      <div
        v-for="habit in safeActiveHabits"
        :key="habit.id"
        class="flex flex-col items-center px-2"
      >
        <div class="text-3xl mb-1">🐍</div>
        <div class="text-xs text-white font-bold">{{ habit.nombre }}</div>
        <div class="text-xs text-yellow-400">⭐ {{ habit.estrellas ?? 0 }}</div>
        <div class="text-xs text-blue-400">Nivel {{ habit.nivel ?? 1 }}</div>
        <div class="text-xs text-green-400">Días: {{ habit.dias_activos ?? 0 }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useHabitStore } from './stores/habitStore'

const habitStore = useHabitStore()
const safeHabits = computed(() => Array.isArray(habitStore.habits) ? habitStore.habits : [])
const safeActiveHabits = computed(() =>
  safeHabits.value.filter(h => h.estado === 'activo' || h.estado === 'incubando')
)
</script>

<style scoped>
.habit-snake {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
</style>
