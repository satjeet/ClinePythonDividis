<template>
  <div class="achievements-room cosmic-card mb-4">
    <h2 class="font-semibold mb-2">Logros Desbloqueados</h2>
    <div v-if="loading" class="text-blue-400 text-xs">Cargando logros...</div>
    <div v-else-if="safeAchievements.length === 0" class="text-gray-400 text-sm">
      Aún no has desbloqueado logros en este módulo.
    </div>
    <ul v-else class="flex flex-wrap gap-4">
      <li
        v-for="ach in safeAchievements"
        :key="ach.id"
        class="bg-slate-800 rounded-lg px-4 py-2 flex flex-col items-center min-w-[120px]"
      >
        <span class="text-2xl mb-1">🏆</span>
        <span class="font-bold text-white text-xs mb-1">{{ ach.title }}</span>
        <span class="text-xs text-gray-300">{{ ach.description }}</span>
        <span class="text-xs text-yellow-400 mt-1">+{{ ach.xp_reward }} XP</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const achievements = ref<any[]>([])
const loading = ref(true)
const safeAchievements = computed(() => Array.isArray(achievements.value) ? achievements.value : [])

onMounted(async () => {
  loading.value = true
  try {
    // Filtrar logros del módulo salud
    const res = await axios.get('/api/achievements/', { params: { module: 'salud' } })
    achievements.value = res.data
  } catch (e) {
    achievements.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.achievements-room {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
</style>
