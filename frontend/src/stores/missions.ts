import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Mission } from '@/types'
import { useModulesStore } from './modules'
import { useGlobalToastStore } from './globalToast'

type MissionWithRequirements = Mission & { blocked?: boolean }

export const useMissionsStore = defineStore('missions', () => {
  const modulesStore = useModulesStore()
  const toastStore = useGlobalToastStore()

  // Estado
  const missions = ref<any[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Fetch real desde el backend unificado
  async function fetchMissions() {
    loading.value = true
    error.value = null
    try {
      // Obtener token JWT desde localStorage
      const token = localStorage.getItem('token')
      const response = await fetch('/api/user-missions/', {
        credentials: 'include',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {}
      })
      if (!response.ok) throw new Error('Error al obtener misiones')
      const data = await response.json()
      console.log('Misiones recibidas:', data)

      // Persistencia de felicitaciones para evitar duplicados
      const FELICITADAS_KEY = 'missions-felicitadas'
      const felicitadas: string[] = JSON.parse(localStorage.getItem(FELICITADAS_KEY) || '[]')
      const prevCompletedIds = new Set(missions.value.filter(m => m.state === 'completed').map(m => m.id))
      missions.value = data
      const newCompleted = missions.value.filter(m => m.state === 'completed' && !prevCompletedIds.has(m.id))
      for (const mission of newCompleted) {
        if (!felicitadas.includes(mission.id)) {
          toastStore.showToast(`¡Felicidades! Completaste la misión "${mission.title}" (+${mission.xp_reward} XP)`, 'success')
          felicitadas.push(mission.id)
        }
      }
      localStorage.setItem(FELICITADAS_KEY, JSON.stringify(felicitadas))
    } catch (err: any) {
      error.value = err.message || 'Error al cargar misiones'
    } finally {
      loading.value = false
    }
  }

  // Getters
  const missionsWithBlocked = computed(() =>
    missions.value.map(m => ({
      ...m,
      blocked: isBlocked(m)
    }))
  )

  const activeMissions = computed(() =>
    missionsWithBlocked.value.filter(m => m.state === 'active' && !m.blocked)
  )

  const completedMissions = computed(() =>
    missionsWithBlocked.value.filter(m => m.state === 'completed')
  )

  const activableMissions = computed(() =>
    missionsWithBlocked.value.filter(m =>
      m.state !== 'active' &&
      m.state !== 'completed' &&
      !m.blocked
    )
  )

  const blockedMissions = computed(() =>
    missionsWithBlocked.value.filter(m =>
      m.state !== 'active' &&
      m.state !== 'completed' &&
      m.blocked
    )
  )

  const dailyMissions = computed(() =>
    missions.value.filter(m => m.frequency === 'daily')
  )

  const weeklyMissions = computed(() =>
    missions.value.filter(m => m.frequency === 'weekly')
  )

  // Lógica de requisitos
  function isBlocked(mission: MissionWithRequirements) {
    if (!mission.requirements || mission.requirements.length === 0) return false
    for (const req of mission.requirements) {
      if (req.type === 'module') {
        const mod = modulesStore.modules.find(m => m.id === req.id)
        if (!mod || mod.state !== 'unlocked') return true
      }
      if (req.type === 'mission') {
        const prev = missions.value.find(m => m.id === req.id)
        if (!prev || prev.state !== 'completed') return true
      }
    }
    return false
  }

  // Activar misión
  function activateMission(mission: MissionWithRequirements) {
    if (activeMissions.value.length >= 3) return
    if (isBlocked(mission)) return
    mission.state = 'active'
    // Aquí deberías llamar a la API para actualizar el estado en backend
    // El toast de misión completada se dispara en fetchMissions al detectar cambios reales
  }

  return {
    missions,
    loading,
    error,
    fetchMissions,
    activeMissions,
    completedMissions,
    activableMissions,
    blockedMissions,
    dailyMissions,
    weeklyMissions,
    activateMission,
    isBlocked
  }
})
