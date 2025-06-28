// frontend/src/stores/userProgress.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useUserProgressStore = defineStore('userProgress', () => {
  const username = ref('')
  const level = ref(1)
  const xp = ref(0)
  const title = ref('')
  const stats = ref({
    modules_unlocked: 0,
    missions_completed: 0,
    achievements_earned: 0
  })
  const longestStreak = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchProgress() {
    loading.value = true
    error.value = null
    try {
      const res = await api.get('/progress/overview/')
      // Ajustar según la estructura real de la respuesta
      username.value = res.data.username || ''
      level.value = res.data.level || 1
      xp.value = res.data.total_xp || 0
      title.value = res.data.title || ''
      stats.value = {
        modules_unlocked: res.data.modules_unlocked || 0,
        missions_completed: res.data.missions_completed || 0,
        achievements_earned: res.data.achievements_earned || 0
      }
      // Si hay streaks por módulo, tomar el mayor
      if (res.data.current_streaks) {
        const streakVals = Object.values(res.data.current_streaks).map(v => Number(v))
        longestStreak.value = Math.max(...streakVals, 0)
      } else {
        longestStreak.value = 0
      }
    } catch (e: any) {
      error.value = e.message || 'Error al cargar progreso'
    } finally {
      loading.value = false
    }
  }

  return {
    username,
    level,
    xp,
    title,
    stats,
    longestStreak,
    loading,
    error,
    fetchProgress
  }
})
