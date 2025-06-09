<template>
  <div class="min-h-screen bg-slate-950">
    <!-- Navigation -->
    <nav class="py-4 px-4 sm:px-6 lg:px-8 cosmic-bg">
      <div class="container mx-auto">
        <div class="flex items-center justify-between">
          <!-- Back button and title -->
          <div class="flex items-center space-x-4">
            <button 
              @click="router.back()"
              class="text-slate-400 hover:text-cosmic-400 transition-colors">
              <i class="fas fa-arrow-left"></i>
            </button>
            <h1 class="text-xl font-bold text-cosmic-100">
              {{ module?.name }}
            </h1>
          </div>

          <!-- Module stats -->
          <div class="flex items-center space-x-6 text-sm">
            <div class="flex items-center space-x-2">
              <i class="fas fa-star text-cosmic-400"></i>
              <span class="text-slate-400">{{ moduleXP }} XP</span>
            </div>
            <div class="flex items-center space-x-2">
              <i class="fas fa-fire text-cosmic-400"></i>
              <span class="text-slate-400">{{ currentStreak }} días</span>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-cosmic-spin w-12 h-12 border-2 border-cosmic-500 rounded-full border-t-transparent"></div>
      </div>

      <template v-else-if="module">
        <!-- Si es el módulo de salud, mostrar la experiencia gamificada -->
        <SaludMain v-if="module.id === 'salud'" />
        <!-- Si no, mostrar el layout de misiones por defecto -->
        <template v-else>
          <!-- Module progress -->
          <div class="cosmic-bg rounded-lg p-6 mb-8">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-medium text-cosmic-100">Progreso del módulo</h2>
              <div class="text-sm text-slate-400">
                {{ completedMissions.length }}/{{ availableMissions.length }} misiones completadas
              </div>
            </div>

            <!-- Progress bar -->
            <div class="w-full bg-slate-800 rounded-full h-2">
              <div 
                class="bg-cosmic-500 h-2 rounded-full transition-all duration-500"
                :style="{
                  width: `${(completedMissions.length / availableMissions.length) * 100}%`
                }">
              </div>
            </div>
          </div>

          <!-- Available missions -->
          <section>
            <h2 class="text-2xl font-bold text-cosmic-100 mb-6">
              Misiones disponibles
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <MissionCard
                v-for="mission in availableMissions"
                :key="mission.id"
                :mission="mission"
                :userLevel="authStore.userLevel"
                :loading="completingMission === mission.id"
                @complete="handleCompleteMission"
                @retry="handleRetryMission"
              />
            </div>
          </section>

          <!-- Module completion message -->
          <div 
            v-if="isModuleCompleted"
            class="mt-12 cosmic-bg rounded-lg p-8 text-center animate-cosmic-float">
            <div class="w-16 h-16 mx-auto mb-4 text-cosmic-400">
              <i class="fas fa-trophy text-4xl"></i>
            </div>
            <h3 class="text-2xl font-bold text-cosmic-100 mb-2">
              ¡Módulo completado!
            </h3>
            <p class="text-slate-400 mb-6">
              Has completado todas las misiones de este módulo. ¡Sigue así!
            </p>
            <Button @click="router.push('/dashboard')">
              Volver al Dashboard
            </Button>
          </div>
        </template>
      </template>

      <!-- Error state -->
      <template v-else>
        <div class="text-center py-12">
          <p class="text-red-500">Error al cargar el módulo</p>
          <Button 
            class="mt-4"
            @click="loadModule">
            Reintentar
          </Button>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useModulesStore } from '@/stores/modules'
import Button from '@/components/ui/Button.vue'
import MissionCard from '@/components/missions/MissionCard.vue'
import SaludMain from '@/components/modules/salud/SaludMain.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const moduleStore = useModulesStore()

const loading = ref(true)
const completingMission = ref<string | null>(null)

// Computed properties
const moduleId = computed(() => route.params.id as string)

const module = computed(() => 
  moduleStore.modules.find(m => m.id === moduleId.value)
)

const availableMissions = computed(() => 
  moduleStore.missions.filter(m => m.module.id === moduleId.value)
)

const completedMissions = computed(() => 
  availableMissions.value.filter(m => m.state === 'completed')
)

const isModuleCompleted = computed(() => 
  availableMissions.value.length > 0 &&
  completedMissions.value.length === availableMissions.value.length
)

const moduleXP = computed(() => 
  module.value?.progress?.experience_points || 0
)

const currentStreak = computed(() => 
  module.value?.streak?.current_streak || 0
)

// Actions
async function loadModule() {
  loading.value = true
  try {
    await moduleStore.setCurrentModule(moduleId.value)
  } catch (err) {
    console.error('Error loading module:', err)
  } finally {
    loading.value = false
  }
}

async function handleCompleteMission(missionId: string) {
  completingMission.value = missionId
  try {
    await moduleStore.completeMission(missionId)
  } catch (err) {
    console.error('Error completing mission:', err)
  } finally {
    completingMission.value = null
  }
}

async function handleRetryMission(missionId: string) {
  // Reset mission progress and start over
  handleCompleteMission(missionId)
}

// Initialize
onMounted(() => {
  loadModule()
})
</script>
