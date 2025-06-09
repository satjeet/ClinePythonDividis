<template>
  <div class="habit-list cosmic-card mb-4">
    <h2 class="font-semibold mb-2">Hábitos Activos</h2>
    <ul>
      <li v-for="habit in safeHabits" :key="habit.id" class="py-1 flex items-center">
        <span class="mr-2">🐍</span>
        <span class="font-medium">{{ habit.nombre }}</span>
        <span class="ml-auto text-xs text-gray-400">Día {{ habit.dias_activos }}</span>
      </li>
    </ul>
    <div v-if="habitStore.loading" class="text-xs text-blue-400 mt-2">Cargando...</div>
    <div v-if="habitStore.error" class="text-xs text-red-400 mt-2">{{ habitStore.error }}</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useHabitStore } from './stores/habitStore'

const habitStore = useHabitStore()
const safeHabits = computed(() => Array.isArray(habitStore.habits) ? habitStore.habits : [])
onMounted(() => {
  habitStore.fetchHabits()
})
</script>

<style scoped>
.habit-list {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
</style>
