import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export interface Habit {
  id: number
  nombre: string
  dificultad: string
  horario_sugerido?: string
  fecha_creacion?: string
  dias_activos?: number
  estrellas?: number
  nivel?: number
  estado?: string
}

export const useHabitStore = defineStore('habit', () => {
  const habits = ref<Habit[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchHabits() {
    loading.value = true
    error.value = null
    try {
      const res = await axios.get('/api/habits/')
      habits.value = res.data
    } catch (e: any) {
      error.value = e?.message || 'Error al cargar hábitos'
    } finally {
      loading.value = false
    }
  }

  async function createHabit(data: { nombre: string, dificultad: string, horario_sugerido?: string }) {
    loading.value = true
    error.value = null
    try {
      await axios.post('/api/habits/', data)
      // Refrescar la lista completa para mantener la reactividad y evitar sobrescribir
      await fetchHabits()
    } catch (e: any) {
      error.value = e?.message || 'Error al crear hábito'
    } finally {
      loading.value = false
    }
  }

  async function updateHabit(id: number, data: Partial<Habit>) {
    loading.value = true
    error.value = null
    try {
      await axios.patch(`/api/habits/${id}/`, data)
      await fetchHabits()
    } catch (e: any) {
      error.value = e?.message || 'Error al actualizar hábito'
    } finally {
      loading.value = false
    }
  }

  return {
    habits,
    loading,
    error,
    fetchHabits,
    createHabit,
    updateHabit
  }
})
