<template>
  <div class="min-h-screen bg-slate-950">
    <!-- Navigation -->
    <nav class="py-4 px-4 sm:px-6 lg:px-8 cosmic-bg">
      <div class="container mx-auto">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <div class="flex items-center space-x-4">
            <RouterLink to="/" class="text-2xl font-bold text-cosmic-100">
              Dividis
            </RouterLink>
            <span class="text-slate-400">|</span>
            <span class="text-cosmic-400">Dashboard</span>
          </div>

          <!-- User menu -->
          <div class="flex items-center space-x-6">
            <!-- Profile link -->
            <RouterLink 
              :to="{ name: 'profile' }"
              class="text-slate-400 hover:text-cosmic-400 transition-colors">
              <i class="fas fa-user"></i>
            </RouterLink>
            <!-- Logout button -->
            <button 
              @click="handleLogout"
              class="text-slate-400 hover:text-red-400 transition-colors">
              <i class="fas fa-sign-out-alt"></i>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading state -->
      <div v-if="loading || !authStore.user" class="flex justify-center py-12">
        <div class="animate-cosmic-spin w-12 h-12 border-2 border-cosmic-500 rounded-full border-t-transparent"></div>
      </div>

      <template v-else>
        <!-- User progress card -->
        <UserProgress
          :username="authStore.user?.username || ''"
          :level="authStore.userLevel"
          :xp="authStore.userXP"
          :stats="stats"
          :longestStreak="longestStreak"
        />

        <!-- Available modules -->
        <section class="mt-12">
          <div class="flex items-baseline justify-between mb-6">
            <h2 class="text-2xl font-bold text-cosmic-100">
              Módulos disponibles
            </h2>
            <span class="text-slate-400">
              {{ moduleStore.unlockedModules.length }} de {{ moduleStore.modules.length }} desbloqueados
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ModuleCard
              v-for="module in moduleStore.modules"
              :key="module.id"
              :module="module"
              :progress="module.progress"
              :missions="module.missions"
              :streak="module.streak"
              :userXP="authStore.userXP"
              @unlock="handleUnlockModule"
              @select="handleSelectModule"
            />
          </div>
        </section>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useModulesStore } from '@/stores/modules'
import UserProgress from '@/components/user/UserProgress.vue'
import ModuleCard from '@/components/modules/ModuleCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const moduleStore = useModulesStore()
const loading = ref(true)

// Computed stats based on module store
const stats = computed(() => ({
  modules_unlocked: moduleStore.unlockedModules.length,
  missions_completed: moduleStore.missions.filter(m => m.state === 'completed').length,
  achievements_earned: 0 // TODO: Implement achievements
}))

const longestStreak = computed(() => {
  return Math.max(
    ...moduleStore.modules
      .map(m => m.streak?.longest_streak || 0)
  )
})

// Load initial data
async function loadDashboard() {
  loading.value = true
  try {
    await Promise.all([
      moduleStore.fetchModules(),
      moduleStore.fetchMissions()
    ])
  } catch (err) {
    console.error('Error loading dashboard:', err)
  } finally {
    loading.value = false
  }
}

// Event handlers
async function handleUnlockModule(moduleId: string) {
  try {
    await moduleStore.unlockModule(moduleId)
  } catch (err) {
    console.error('Error unlocking module:', err)
  }
}

function handleSelectModule(moduleId: string) {
  router.push({
    name: 'module',
    params: { id: moduleId }
  })
}

async function handleLogout() {
  await authStore.logout()
}

// Initialize
onMounted(() => {
  loadDashboard()
})
</script>
