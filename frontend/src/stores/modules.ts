import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Module, Mission, ModuleProgress, MissionProgress } from '@/types'
import { moduleApi, missionApi } from '@/services/api'
import { useAuthStore } from './auth'

interface ModuleWithProgress extends Module {
  progress?: ModuleProgress
  missions?: Mission[]
  streak?: {
    current_streak: number
    longest_streak: number
  }
}

export const useModulesStore = defineStore('modules', () => {
  const authStore = useAuthStore()
  
  // State
  const modules = ref<ModuleWithProgress[]>([])
  const missions = ref<Mission[]>([])
  const currentModule = ref<ModuleWithProgress | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const unlockedModules = computed(() => 
    modules.value.filter(m => m.state === 'unlocked' || m.state === 'completed')
  )

  const activeModules = computed(() => 
    modules.value.filter(m => m.state === 'unlocked')
  )

  const availableMissions = computed(() => 
    missions.value.filter(m => 
      unlockedModules.value.some(mod => mod.id === m.module.id)
    )
  )

  const nextModule = computed(() => {
    const userLevel = authStore.userLevel
    return modules.value.find(m => 
      m.state === 'locked' && 
      m.xp_required <= (authStore.userXP || 0)
    )
  })

  // Actions
  async function fetchModules() {
    loading.value = true
    error.value = null
    try {
      const response = await moduleApi.getAll()
      modules.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al cargar módulos'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function fetchMissions() {
    loading.value = true
    error.value = null
    try {
      const response = await missionApi.getAll()
      missions.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al cargar misiones'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function unlockModule(moduleId: string) {
    loading.value = true
    error.value = null
    try {
      const response = await moduleApi.unlock(moduleId)
      const index = modules.value.findIndex(m => m.id === moduleId)
      if (index !== -1) {
        modules.value[index] = {
          ...modules.value[index],
          ...response.data
        }
      }
      await fetchMissions() // Refresh missions after unlock
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al desbloquear módulo'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function completeMission(missionId: string) {
    loading.value = true
    error.value = null
    try {
      const response = await missionApi.complete(missionId)
      const index = missions.value.findIndex(m => m.id === missionId)
      if (index !== -1) {
        missions.value[index] = {
          ...missions.value[index],
          ...response.data
        }
      }
      await Promise.all([
        fetchModules(), // Refresh modules after mission completion
        authStore.fetchUserProfile() // Refresh user XP and level
      ])
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al completar misión'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function loadModuleProgress(moduleId: string) {
    loading.value = true
    error.value = null
    try {
      const response = await moduleApi.getProgress(moduleId)
      const index = modules.value.findIndex(m => m.id === moduleId)
      if (index !== -1) {
        modules.value[index] = {
          ...modules.value[index],
          ...response.data
        }
      }
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al cargar progreso del módulo'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function setCurrentModule(moduleId: string) {
    const module = modules.value.find(m => m.id === moduleId)
    if (module) {
      currentModule.value = module
      // Load detailed progress if module is unlocked
      if (module.state !== 'locked') {
        await loadModuleProgress(moduleId)
      }
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
    activeModules,
    availableMissions,
    nextModule,

    // Actions
    fetchModules,
    fetchMissions,
    unlockModule,
    completeMission,
    setCurrentModule,
    loadModuleProgress
  }
})
