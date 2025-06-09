<template>
  <div class="growth-room cosmic-card mb-4">
    <h2 class="font-semibold mb-2">Salón de Crianza</h2>
    <ul>
      <li v-for="habit in habitStore.habits" :key="habit.id" class="py-1 flex items-center">
        <span class="mr-2">🐍</span>
        <span class="font-medium">{{ habit.nombre }}</span>
        <span class="ml-2 text-xs text-yellow-400">⭐ {{ habit.estrellas ?? 0 }}</span>
        <span class="ml-2 text-xs text-blue-400">Nivel {{ habit.nivel ?? 1 }}</span>
        <button
          class="ml-auto bg-green-600 hover:bg-green-700 text-white px-2 py-1 rounded text-xs"
          @click="train(habit)"
          :disabled="trainingId === habit.id"
        >
          <span v-if="trainingId !== habit.id">Entrenar</span>
          <span v-else>Entrenando...</span>
        </button>
      </li>
    </ul>
    <div v-if="showTrain" class="mt-3 text-green-400 text-sm">¡Entrenamiento aplicado!</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useHabitStore, type Habit } from './stores/habitStore'

const habitStore = useHabitStore()
const showTrain = ref(false)
const trainingId = ref<number | null>(null)

async function train(habit: Habit) {
  showTrain.value = false
  trainingId.value = habit.id
  try {
    await habitStore.updateHabit(habit.id, {
      nivel: (habit.nivel ?? 1) + 1,
      estrellas: (habit.estrellas ?? 0) + 0.5
    })
    showTrain.value = true
    setTimeout(() => { showTrain.value = false }, 1200)
  } finally {
    trainingId.value = null
  }
}
</script>

<style scoped>
.growth-room {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
</style>
