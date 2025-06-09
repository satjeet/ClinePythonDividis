<template>
  <!-- Últimas declaraciones y misiones activas -->
  <div class="user-log-root">
    <div class="flex flex-col md:flex-row gap-6">
      <!-- Declaraciones recientes -->
      <div class="flex-1">
        <h4 class="text-cosmic-300 font-semibold mb-2">Últimas declaraciones</h4>
        <ul class="space-y-1 text-cosmic-100 text-sm">
          <li>
            <span class="font-bold">Salud:</span> “Me comprometo a caminar 30 minutos diarios.”
            <span class="ml-2 text-xs text-cosmic-400">hace 2 días</span>
          </li>
          <li>
            <span class="font-bold">Intelecto:</span> “Dedicaré 20 minutos a la lectura cada noche.”
            <span class="ml-2 text-xs text-cosmic-400">ayer</span>
          </li>
        </ul>
      </div>
      <!-- Misiones activas y completadas -->
      <div class="flex-1">
        <h4 class="text-cosmic-300 font-semibold mb-2">Misiones globales</h4>
        <ul class="space-y-1 text-cosmic-100 text-sm">
          <li v-if="loading">Cargando misiones...</li>
          <li v-else-if="error">{{ error }}</li>
          <li v-else-if="globalMissions.length === 0">No tienes misiones globales.</li>
          <template v-for="mission in globalMissions" :key="mission.id">
            <li
              :class="{
                'opacity-60 line-through': mission.state === 'completed',
                'bg-cosmic-800/40 border-l-4 border-cosmic-400': mission.state === 'active',
                'bg-cosmic-900/40 border-l-4 border-cosmic-600': mission.state === 'completed'
              }"
              class="rounded px-2 py-1 mb-1 transition-all"
            >
              <div class="flex items-center justify-between">
                <div>
                  <span class="font-bold">{{ mission.title }}:</span>
                  <span class="ml-1">{{ mission.description }}</span>
                  <span v-if="mission.progress" class="ml-2 text-xs text-cosmic-400">
                    {{ mission.progress.label }}
                  </span>
                </div>
                <span
                  v-if="mission.state === 'completed'"
                  class="ml-2 text-xs px-2 py-0.5 rounded bg-green-700 text-green-100"
                >Completada</span>
                <span
                  v-else
                  class="ml-2 text-xs px-2 py-0.5 rounded bg-cosmic-700 text-cosmic-100"
                >Activa</span>
              </div>
              <div class="ml-2 text-xs text-cosmic-400">
                Recompensa: {{ mission.xp_reward }} XP
                <span v-if="mission.frequency">| {{ mission.frequency === 'daily' ? 'Diaria' : mission.frequency === 'weekly' ? 'Semanal' : 'Global' }}</span>
              </div>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

interface MissionGlobal {
  id: string
  title: string
  description: string
  xp_reward: number
  state: string
  frequency?: string
  progress?: {
    current: number
    target: number
    label: string
  }
}

const globalMissions = ref<MissionGlobal[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/missions/global/')
    // Mostrar todas las misiones, activas primero, luego completadas
    globalMissions.value = res.data.sort((a: MissionGlobal, b: MissionGlobal) => {
      if (a.state === b.state) return 0
      if (a.state === 'active') return -1
      return 1
    })
  } catch (e: any) {
    error.value = e.message || 'Error al cargar misiones globales'
  } finally {
    loading.value = false
  }
})
</script>
<style scoped src="./UserLog.css"></style>
