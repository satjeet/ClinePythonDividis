<template>
  <div class="min-h-screen bg-slate-950 py-16">
    <!-- Loading state -->
    <div v-if="loading" class="container mx-auto px-4 py-12 text-center">
      <div class="animate-cosmic-spin w-16 h-16 border-4 border-cosmic-500 rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-4 text-slate-400">Cargando módulo...</p>
    </div>

    <template v-else-if="module">
      <div class="container mx-auto px-4 py-12">
        <!-- Module header -->
        <div class="mb-12">
          <div class="flex items-center gap-4 mb-6">
            <button 
              @click="router.go(-1)"
              class="text-slate-400 hover:text-cosmic-400 transition-colors">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            <h1 class="text-4xl md:text-5xl font-bold text-cosmic-100">
              {{ module.name }}
            </h1>
          </div>
          <p class="text-xl text-slate-400">
            {{ module.description }}
          </p>
        </div>

        <!-- Module progress -->
        <div class="card-cosmic mb-12">
          <h2 class="text-2xl font-bold text-cosmic-100 mb-6">Progreso del Módulo</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h3 class="text-lg font-medium text-slate-300 mb-2">Estado</h3>
              <p class="text-3xl font-bold text-cosmic-400 capitalize">
                {{ module.state }}
              </p>
            </div>
            <div>
              <h3 class="text-lg font-medium text-slate-300 mb-2">Misiones Completadas</h3>
              <p class="text-3xl font-bold text-cosmic-400">
                {{ completedMissionsCount }}/{{ moduleMissions.length }}
              </p>
            </div>
            <div>
              <h3 class="text-lg font-medium text-slate-300 mb-2">Racha Actual</h3>
              <p class="text-3xl font-bold text-cosmic-400">
                {{ streak?.current_streak || 0 }} días
              </p>
            </div>
          </div>
        </div>

        <!-- Module missions -->
        <div>
          <h2 class="text-2xl font-bold text-cosmic-100 mb-6">Misiones</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="mission in moduleMissions" 
                 :key="mission.id"
                 :class="[
                   'card-cosmic transform transition-transform duration-300',
                   mission.state !== 'completed' ? 'hover:-translate-y-1' : ''
                 ]">
              <div class="flex justify-between items-start mb-4">
                <h3 class="text-lg font-medium text-cosmic-300">{{ mission.title }}</h3>
                <span class="text-sm text-cosmic-400">+{{ mission.xp_reward }} XP</span>
              </div>
              <p class="text-slate-400 mb-4">{{ mission.description }}</p>
              
              <!-- Mission actions -->
              <div v-if="mission.state !== 'completed'"
                   class="flex justify-end">
                <button 
                  @click="handleCompleteMission(mission.id)"
                  class="btn-cosmic"
                  :disabled="loading">
                  Completar Misión
                </button>
              </div>
              <div v-else class="flex justify-between items-center">
                <span class="text-sm text-cosmic-400">Completada</span>
                <svg class="w-6 h-6 text-cosmic-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Module not found -->
    <div v-else class="container mx-auto px-4 py-12 text-center">
      <h2 class="text-2xl font-bold text-cosmic-100 mb-4">
        Módulo no encontrado
      </h2>
      <p class="text-slate-400 mb-8">
        El módulo que buscas parece no existir o no tienes acceso a él.
      </p>
      <RouterLink 
        to="/dashboard"
        class="btn-cosmic">
        Volver al Panel Principal
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useModulesStore } from '@/stores/modules'

const route = useRoute()
const router = useRouter()
const modulesStore = useModulesStore()
const loading = ref(false)

const moduleId = computed(() => route.params.id as string)

const module = computed(() => 
  modulesStore.modules.find(m => m.id === moduleId.value)
)

const moduleMissions = computed(() =>
  modulesStore.missions.filter(m => m.module.id === moduleId.value)
)

const completedMissionsCount = computed(() =>
  moduleMissions.value.filter(m => m.state === 'completed').length
)

const streak = computed(() =>
  module.value ? modulesStore.getModuleStreak(module.value.id) : null
)

async function handleCompleteMission(missionId: string) {
  loading.value = true
  try {
    await modulesStore.completeMission(missionId)
  } catch (err) {
    console.error('Error completing mission:', err)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    await Promise.all([
      modulesStore.fetchModules(),
      modulesStore.fetchMissions()
    ])
  } catch (err) {
    console.error('Error loading module:', err)
  } finally {
    loading.value = false
  }
})
</script>
