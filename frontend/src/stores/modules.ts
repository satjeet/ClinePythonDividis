import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Module, Mission, ModuleProgress } from '@/types'
import { moduleApi, missionApi, declarationApi } from '@/services/api'
import { useAuthStore } from './auth'

interface ModuleWithProgress extends Module {
  progress?: ModuleProgress
  missions?: Mission[]
  streak?: {
    current_streak: number
    longest_streak: number
  }
}

interface Declaration {
  id?: number
  module: string
  pillar: string
  text: string
  synced?: boolean
}

export const useModulesStore = defineStore('modules', () => {
  const authStore = useAuthStore()
  
  // State
  const modules = ref<ModuleWithProgress[]>([])
  const missions = ref<Mission[]>([])
  const currentModule = ref<ModuleWithProgress | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Declaraciones
  const declarations = ref<Declaration[]>([])

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
    return modules.value.find(m => 
      m.state === 'locked' && 
      m.xp_required <= (authStore.userXP || 0)
    )
  })

  // Agrupar declaraciones por pilar (para DeclarationList)
  function getDeclarationsByPillar(pillar: string) {
    return declarations.value.filter(d => d.pillar === pillar)
  }

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

  // Declaraciones: cargar desde backend
  async function fetchDeclarations() {
    loading.value = true
    error.value = null
    try {
      const response = await declarationApi.getAll()
      // Mapear a estructura local
      declarations.value = response.data.map((d: any) => ({
        id: d.id,
        module: typeof d.module === 'string' ? d.module : (d.module?.id || ''),
        pillar: d.pillar,
        text: d.text,
        synced: true
      }))
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al cargar declaraciones'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  // Declaraciones: agregar localmente (sincronizar después)
  function addDeclaration(pillar: string, declaration: string, moduleId?: string) {
    // Buscar el id real del módulo
    let modId = moduleId
    if (!modId || typeof modId !== 'string') {
      modId = currentModule.value?.id || ''
    }
    if (typeof modId !== 'string' || !modId) {
      throw new Error('No se pudo determinar el módulo para la declaración')
    }
    declarations.value.push({
      module: modId,
      pillar,
      text: declaration,
      synced: false
    })
  }

  // Declaraciones: sincronizar con backend (guardar las no sincronizadas)
  async function syncDeclarations() {
    loading.value = true
    error.value = null
    try {
      const unsynced = declarations.value.filter(d => !d.synced)
      for (const d of unsynced) {
        try {
          // Asegurar que module sea string id
          const moduleId = typeof d.module === 'string' ? d.module : (d.module as any)?.id || ''
          if (!moduleId) throw new Error('Declaración sin módulo válido')
          const response = await declarationApi.create({
            module: moduleId,
            pillar: d.pillar,
            text: d.text
          })
          d.id = response.data.id
          d.synced = true
        } catch (err: any) {
          // Si es error de unicidad (ya existe), márcala como sincronizada
          if (err.response && err.response.status === 400 && err.response.data && typeof err.response.data === 'object') {
            const detail = JSON.stringify(err.response.data)
            if (detail.includes('unique') || detail.includes('UNIQUE')) {
              d.synced = true
              continue
            }
          }
          // Otro error: mostrar mensaje real del backend
          if (err.response && err.response.data) {
            error.value = JSON.stringify(err.response.data)
            // eslint-disable-next-line no-console
            console.error('Error declaración:', err.response.data)
            throw error.value
          } else {
            error.value = err.response?.data?.detail || 'Error al guardar declaraciones'
            throw error.value
          }
        }
      }
      // Refrescar módulos y declaraciones tras sincronizar (para reflejar desbloqueos)
      await Promise.all([fetchModules(), fetchDeclarations()])
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    modules,
    missions,
    currentModule,
    declarations,
    loading,
    error,

    // Getters
    unlockedModules,
    activeModules,
    availableMissions,
    nextModule,
    getDeclarationsByPillar,

    // Actions
    fetchModules,
    fetchMissions,
    unlockModule,
    completeMission,
    setCurrentModule,
    loadModuleProgress,
    addDeclaration,
    fetchDeclarations,
    syncDeclarations
  }
})
