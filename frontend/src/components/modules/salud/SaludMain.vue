<template>
  <div class="salud-main">
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin w-12 h-12 border-4 border-blue-400 rounded-full border-t-transparent"></div>
    </div>
    <div v-else-if="error" class="text-center text-red-400 py-8">
      Error al cargar datos de Salud.<br>
      <button class="mt-4 px-4 py-2 bg-blue-600 rounded text-white" @click="loadAll">Reintentar</button>
    </div>
    <div v-else>
      <ComfortWall />
      <HabitSnake />
      <GrowthRoom />
      <IncubationRoom />
      <AttackButton />
      <AchievementsRoom />
      <RankStars />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ComfortWall from './ComfortWall.vue'
import HabitSnake from './HabitSnake.vue'
import GrowthRoom from './GrowthRoom.vue'
import IncubationRoom from './IncubationRoom.vue'
import AttackButton from './AttackButton.vue'
import AchievementsRoom from './AchievementsRoom.vue'
import RankStars from './RankStars.vue'
import { useHabitStore } from './stores/habitStore'
import { useWallStore } from './stores/wallStore'

const habitStore = useHabitStore()
const wallStore = useWallStore()
const loading = ref(true)
const error = ref(false)

async function loadAll() {
  loading.value = true
  error.value = false
  try {
    await Promise.all([
      habitStore.fetchHabits(),
      wallStore.fetchWall()
    ])
  } catch (e) {
    error.value = true
  } finally {
    loading.value = false
  }
}

loadAll()
</script>

<style scoped>
.salud-main {
  min-height: 80vh;
}
.animate-spin {
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
