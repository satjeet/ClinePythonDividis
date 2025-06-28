<template>
  <nav class="py-4 px-4 sm:px-6 lg:px-8 cosmic-bg shadow">
    <div class="container mx-auto flex items-center justify-between">
      <!-- Logo y sección -->
      <div class="flex items-center space-x-4">
        <RouterLink to="/" class="text-2xl font-bold text-cosmic-100">
          Dividis
        </RouterLink>
        <span class="text-slate-400">|</span>
        <span class="text-cosmic-400">{{ sectionTitle }}</span>
      </div>
      <!-- Menú usuario -->
      <div class="flex items-center space-x-6">
        <RouterLink 
          :to="{ name: 'missions' }"
          class="text-slate-400 hover:text-cosmic-400 transition-colors"
        >
          <i class="fas fa-flag-checkered"></i>
          <span class="ml-1">Misiones</span>
        </RouterLink>
        <RouterLink 
          :to="{ name: 'profile' }"
          class="text-slate-400 hover:text-cosmic-400 transition-colors"
        >
          <i class="fas fa-user"></i>
        </RouterLink>
        <button 
          @click="handleLogout"
          class="text-slate-400 hover:text-red-400 transition-colors"
        >
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

defineProps({
  sectionTitle: {
    type: String,
    default: 'Dashboard'
  }
})

const router = useRouter()
const authStore = useAuthStore()

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.cosmic-bg {
  background: linear-gradient(90deg, #1e293b 0%, #312e81 100%);
}
</style>
