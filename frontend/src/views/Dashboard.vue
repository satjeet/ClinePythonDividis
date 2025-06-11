<template>
  <div class="min-h-screen bg-[var(--theme-bg)]">
    <!-- Navigation -->
    <AppNavbar sectionTitle="Dashboard" />

    <!-- Main content -->
    <main class="container mx-auto px-2 sm:px-4 lg:px-8 py-8 flex flex-col items-center">
      <!-- Loading state -->
      <div v-if="loading || !authStore.user" class="flex justify-center py-12">
        <div class="animate-cosmic-spin w-12 h-12 border-2 border-cosmic-500 rounded-full border-t-transparent"></div>
      </div>

      <template v-else>
        <!-- Galactic Dashboard modular (nuevo) -->
        <div class="w-full max-w-4xl neon-border card-cosmic shadow-xl rounded-2xl p-8 mb-12">
          <DashboardModular />
        </div>

        <!-- Available modules -->
        <section class="w-full max-w-6xl neon-border card-cosmic shadow-xl rounded-2xl p-8">
          <div class="flex flex-col md:flex-row md:items-baseline md:justify-between mb-6 gap-2">
            <h2 class="text-2xl font-bold cosmic-gradient-text">
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useModulesStore } from '@/stores/modules'
import ModuleCard from '@/components/modules/ModuleCard.vue'
import DashboardModular from '@/components/dashboard/DashboardModular.vue'
import AppNavbar from '@/components/ui/AppNavbar.vue'

const router = useRouter()
const authStore = useAuthStore()
const moduleStore = useModulesStore()
const loading = ref(true)

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



 // Initialize
onMounted(() => {
  loadDashboard()
})
</script>
