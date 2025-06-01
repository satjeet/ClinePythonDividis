<template>
  <div class="min-h-screen bg-slate-950 py-16">
    <!-- Loading state -->
    <div v-if="loading" class="container mx-auto px-4 py-12 text-center">
      <div class="animate-cosmic-spin w-16 h-16 border-4 border-cosmic-500 rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-4 text-slate-400">Cargando tu viaje cósmico...</p>
    </div>

    <template v-else>
      <!-- Hero section -->
      <div class="container mx-auto px-4 py-12">
        <h1 class="text-4xl md:text-5xl font-bold text-cosmic-100 mb-4">
          Bienvenido, {{ authStore.user?.username }}
        </h1>
        <p class="text-xl text-slate-400 mb-8">
          Continúa tu viaje de desarrollo personal
        </p>

        <!-- Progress overview -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div class="card-cosmic">
            <h3 class="text-lg font-medium text-slate-300 mb-2">Nivel</h3>
            <p class="text-3xl font-bold text-cosmic-400">
              {{ authStore.user?.profile?.current_level || 1 }}
            </p>
          </div>
          <div class="card-cosmic">
            <h3 class="text-lg font-medium text-slate-300 mb-2">Módulos Desbloqueados</h3>
            <p class="text-3xl font-bold text-cosmic-400">
              {{ modulesStore.unlockedModules.length }}
            </p>
          </div>
          <div class="card-cosmic">
            <h3 class="text-lg font-medium text-slate-300 mb-2">Misiones Completadas</h3>
            <p class="text-3xl font-bold text-cosmic-400">
              {{ completedMissionsCount }}
            </p>
          </div>
        </div>

        <!-- Active missions -->
        <div class="mb-12">
          <h2 class="text-2xl font-bold text-cosmic-100 mb-6">Misiones Activas</h2>
          <div v-if="activeMissions.length" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="mission in activeMissions" 
                 :key="mission.id" 
                 class="card-cosmic transform hover:-translate-y-1 transition-transform duration-300">
              <div class="flex justify-between items-start mb-4">
                <h3 class="text-lg font-medium text-cosmic-300">{{ mission.title }}</h3>
                <span class="text-sm text-cosmic-400">+{{ mission.xp_reward }} XP</span>
              </div>
              <p class="text-slate-400 mb-4">{{ mission.description }}</p>
              <button 
                @click="handleCompleteMission(mission.id)"
                class="btn-cosmic w-full"
                :disabled="loading">
                Completar Misión
              </button>
            </div>
          </div>
          <div v-else class="card-cosmic text-center py-8">
            <p class="text-slate-400">No tienes misiones activas. ¡Explora los módulos para comenzar!</p>
          </div>
        </div>

        <!-- Modules grid -->
        <div>
          <h2 class="text-2xl font-bold text-cosmic-100 mb-6">Módulos</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div v-for="module in modulesStore.modules" 
                 :key="module.id"
                 class="relative">
              <!-- Module card -->
              <div :class="[
                'module-card',
                module.state === 'locked' ? 'module-locked' : ''
              ]">
                <!-- Module content -->
                <div class="flex items-start justify-between mb-4">
                  <div class="flex-1">
                    <h3 class="text-lg font-medium text-cosmic-300">{{ module.name }}</h3>
                    <p class="text-sm text-slate-400">{{ module.description }}</p>
                  </div>
                </div>

                <!-- Module status and actions -->
                <div class="mt-4">
                  <template v-if="module.state === 'locked'">
                    <p class="text-sm text-slate-500 mb-2">
                      Requiere {{ module.xp_required }} XP para desbloquear
                    </p>
                    <button 
                      @click="handleUnlockModule(module.id)"
                      class="btn-cosmic w-full"
                      :disabled="authStore.user?.profile?.experience_points < module.xp_required">
                      Desbloquear
                    </button>
                  </template>
                  <template v-else>
                    <RouterLink 
                      :to="{ name: 'module', params: { id: module.id }}"
                      class="btn-cosmic w-full block text-center">
                      {{ module.state === 'completed' ? 'Revisar' : 'Continuar' }}
                    </RouterLink>
                  </template>
                </div>
              </div>

              <!-- Locked overlay -->
              <div v-if="module.state === 'locked'"
                   class="absolute inset-0 bg-slate-950/50 backdrop-blur-sm rounded-lg flex items-center justify-center">
                <svg class="w-8 h-8 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useModulesStore } from '@/stores/modules'

const authStore = useAuthStore()
const modulesStore = useModulesStore()
const loading = ref(false)

const activeMissions = computed(() => 
  modulesStore.missions.filter(m => m.state === 'active')
)

const completedMissionsCount = computed(() =>
  modulesStore.missions.filter(m => m.state === 'completed').length
)

async function handleUnlockModule(moduleId: string) {
  loading.value = true
  try {
    await modulesStore.unlockModule(moduleId)
  } catch (err) {
    console.error('Error unlocking module:', err)
  } finally {
    loading.value = false
  }
}

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
    console.error('Error loading dashboard:', err)
  } finally {
    loading.value = false
  }
})
</script>
