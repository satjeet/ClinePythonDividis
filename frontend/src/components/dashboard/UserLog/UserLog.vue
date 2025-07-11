<template>
  <Card variant="interactive">
    <!-- Últimas declaraciones y misiones activas -->
    <div class="">
      <div class="flex flex-col md:flex-row gap-6">
        <!-- Declaraciones recientes -->
        <div class="flex-1">
          <h4 class="font-semibold mb-2" :style="{ color: 'var(--theme-border)' }">Últimas declaraciones</h4>
          <ul class="space-y-1 text-sm" :style="{ color: 'var(--theme-accent-contrast, #fff)' }">
            <li v-if="declarationsLoading">Cargando declaraciones...</li>
            <li v-else-if="declarationsError">{{ declarationsError }}</li>
            <li v-else-if="recentDeclarations.length === 0">No hay declaraciones recientes.</li>
            <template v-else v-for="declaration in recentDeclarations" :key="declaration.id">
              <li>
                <span class="font-bold">{{ declaration.pillar }}:</span>
                “{{ declaration.text }}”
                <span class="ml-2 text-xs" :style="{ color: 'var(--theme-border)' }">{{ timeAgo(declaration.created_at) }}</span>
              </li>
            </template>
          </ul>
        </div>
        <!-- Misiones activas y completadas -->
        <div class="flex-1">
          <h4 class="font-semibold mb-2" :style="{ color: 'var(--theme-border)' }">Misiones Activas</h4>
          <ul class="space-y-1 text-sm" :style="{ color: 'var(--theme-accent-contrast, #fff)' }">
            <li v-if="loading">Cargando misiones...</li>
            <li v-else-if="error">{{ error }}</li>
            <li v-else-if="activeMissions.length === 0">No tienes misiones activas.</li>
            <template v-for="mission in activeMissions" :key="mission.id">
              <li
                :class="{
                  'opacity-60 line-through': mission.state === 'completed'
                }"
                class="rounded px-2 py-1 mb-1 transition-all"
                :style="mission.state === 'active'
                  ? {
                      background: 'color-mix(in srgb, var(--theme-accent) 10%, transparent 90%)',
                      borderLeft: '4px solid var(--theme-accent)'
                    }
                  : mission.state === 'completed'
                  ? {
                      background: 'color-mix(in srgb, var(--theme-border) 10%, transparent 90%)',
                      borderLeft: '4px solid var(--theme-border)'
                    }
                  : {}"
              >
                <div class="flex items-center justify-between">
                  <div>
                    <span class="font-bold">{{ mission.title }}:</span>
                    <span class="ml-1">{{ mission.description }}</span>
                    <span v-if="mission.progress" class="ml-2 text-xs" :style="{ color: 'var(--theme-border)' }">
                      {{ mission.progress.label }}
                    </span>
                  </div>
                  <span
                    v-if="mission.state === 'completed'"
                    class="ml-2 text-xs px-2 py-0.5 rounded"
                    :style="{ background: 'rgba(34,197,94,0.8)', color: '#fff' }"
                  >Completada</span>
                  <span
                    v-else
                    class="ml-2 text-xs px-2 py-0.5 rounded"
                    :style="{ background: 'var(--theme-accent)', color: 'var(--theme-accent-contrast, #fff)' }"
                  >Activa</span>
                </div>
                <div class="ml-2 text-xs" :style="{ color: 'var(--theme-border)' }">
                  Recompensa: {{ mission.xp_reward }} XP
                  <span v-if="mission.frequency">| {{ mission.frequency === 'daily' ? 'Diaria' : mission.frequency === 'weekly' ? 'Semanal' : 'Global' }}</span>
                </div>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
// Cambios para usar el store de misiones y evitar error 404
import { ref, onMounted, computed } from 'vue'
import { useMissionsStore } from '@/stores/missions'
// Cambios para evitar error TS6133: 'api' is declared but its value is never read.
import { declarationApi } from '@/services/api'

// Declaraciones recientes
interface Declaration {
  id: string
  pillar: string
  text: string
  created_at: string
}

const recentDeclarations = ref<Declaration[]>([])
const declarationsLoading = ref(false)
const declarationsError = ref<string | null>(null)

function timeAgo(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now.getTime() - date.getTime()) / 1000)
  if (diff < 60) return 'justo ahora'
  if (diff < 3600) return `${Math.floor(diff / 60)} min`
  if (diff < 86400) return `${Math.floor(diff / 3600)} h`
  if (diff < 172800) return 'ayer'
  return `hace ${Math.floor(diff / 86400)} días`
}

// Misiones activas desde el store Pinia
const missionsStore = useMissionsStore()
const loading = computed(() => missionsStore.loading)
const error = computed(() => missionsStore.error)
const activeMissions = computed(() => missionsStore.activeMissions.slice(0, 3))

onMounted(async () => {
  // Declaraciones recientes
  declarationsLoading.value = true
  try {
    const res = await declarationApi.getAll()
    // Ordenar por fecha descendente y tomar las 2 más recientes
    recentDeclarations.value = (res.data as Declaration[])
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 2)
  } catch (e: any) {
    declarationsError.value = e.message || 'Error al cargar declaraciones'
  } finally {
    declarationsLoading.value = false
  }

  // Asegurar que las misiones estén cargadas
  if (missionsStore.missions.length === 0) {
    await missionsStore.fetchMissions()
  }
})
</script>
<style scoped src="./UserLog.css"></style>
