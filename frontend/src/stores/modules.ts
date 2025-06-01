import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'

interface Module {
  id: string
  name: string
  description: string
  icon: string
  order: number
  xp_required: number
  state: 'locked' | 'unlocked' | 'completed'
}

interface Mission {
  id: string
  module: Module
  title: string
  description: string
  xp_reward: number
  required_level: number
  created_at: string
}

export const useModulesStore = defineStore('modules', () => {
  // State
  const modules = ref<Module[]>([])
  const missions = ref<Mission[]>([])
  const currentModule = ref<Module | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const unlockedModules = computed(() => 
    modules.value.filter(m => m.state === 'unlocked' || m.state === 'completed')
  )

  const availableMissions = computed(() => 
    missions.value.filter(m => 
      unlockedModules.value.some(mod => mod.id === m.module.id)
    )
  )

  const nextModule = computed(() => {
    const locked = modules.value.find(m => m.state === 'locked')
    return locked || null
  })

  // Actions
  async function fetchModules() {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/modules/')
      modules.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al cargar módulos'
    } finally {
      loading.value = false
    }
  }

  async function fetchMissions() {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/missions/')
      missions.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al cargar misiones'
    } finally {
      loading.value = false
    }
  }

  async function unlockModule(moduleId: string) {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post(`/api/modules/${moduleId}/unlock/`)
      const index = modules.value.findIndex(m => m.id === moduleId)
      if (index !== -1) {
        modules.value[index] = response.data
      }
      await fetchMissions() // Refresh missions after unlock
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al desbloquear módulo'
    } finally {
      loading.value = false
    }
  }

  async function completeMission(missionId: string) {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post(`/api/missions/${missionId}/complete/`)
      const index = missions.value.findIndex(m => m.id === missionId)
      if (index !== -1) {
        missions.value[index] = response.data
      }
      await fetchModules() // Refresh modules after mission completion
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al completar misión'
    } finally {
      loading.value = false
    }
  }

  async function setCurrentModule(moduleId: string) {
    const module = modules.value.find(m => m.id === moduleId)
    if (module) {
      currentModule.value = module
    }
  }

  return {
    // State
    modules,
    missions,
    currentModule,
    loading,
    error,

    // Getters
    unlockedModules,
    availableMissions,
    nextModule,

    // Actions
    fetchModules,
    fetchMissions,
    unlockModule,
    completeMission,
    setCurrentModule
  }
})
