import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export interface ComfortWall {
  id: number
  hp_actual: number
  hp_max: number
  nivel_muro: number
  fecha_ultimo_ataque?: string | null
}

export const useWallStore = defineStore('wall', () => {
  const wall = ref<ComfortWall | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchWall() {
    loading.value = true
    error.value = null
    try {
      const res = await axios.get('/api/comfortwall/')
      if (Array.isArray(res.data) && res.data.length > 0) {
        wall.value = res.data[0]
      } else {
        // Si no hay muro, crearlo automáticamente
        const createRes = await axios.post('/api/comfortwall/', {
          hp_actual: 100,
          hp_max: 100,
          nivel_muro: 1
        })
        wall.value = createRes.data
      }
    } catch (e: any) {
      // Si es 404, crear el muro
      if (e.response && e.response.status === 404) {
        try {
          const createRes = await axios.post('/api/comfortwall/', {
            hp_actual: 100,
            hp_max: 100,
            nivel_muro: 1
          })
          wall.value = createRes.data
        } catch (err: any) {
          error.value = err?.message || 'Error al crear muro'
        }
      } else {
        error.value = e?.message || 'Error al cargar muro'
      }
    } finally {
      loading.value = false
    }
  }

  return {
    wall,
    loading,
    error,
    fetchWall
  }
})
