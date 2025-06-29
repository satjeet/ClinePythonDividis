<template>
  <nav class="py-4 px-4 sm:px-6 lg:px-8 navbar-theme shadow" :style="navbarStyle">
    <div class="container mx-auto flex items-center justify-between">
      <!-- Logo y sección -->
      <div class="flex items-center space-x-4">
        <RouterLink to="/" class="text-2xl font-bold" :style="{ color: 'var(--theme-accent)' }">
          Dividis
        </RouterLink>
        <span :style="{ color: 'var(--theme-border)' }">|</span>
        <span :style="{ color: 'var(--theme-accent)' }">{{ sectionTitle }}</span>
      </div>
      <!-- Menú usuario -->
      <div class="flex items-center space-x-6">
        <RouterLink 
          :to="{ name: 'missions' }"
          class="transition-colors"
          :style="navLinkStyle"
        >
          <i class="fas fa-flag-checkered"></i>
          <span class="ml-1">Misiones</span>
        </RouterLink>
        <RouterLink 
          :to="{ name: 'profile' }"
          class="transition-colors"
          :style="navLinkStyle"
        >
          <i class="fas fa-user"></i>
        </RouterLink>
        <button 
          @click="handleLogout"
          class="transition-colors"
          :style="navLinkStyle"
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
import { computed } from 'vue'

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

// Estilos reactivos para integración de theme
const navbarStyle = computed(() => ({
  background: 'var(--theme-navbar-bg, #fff)',
  backdropFilter: 'var(--theme-navbar-blur, blur(0))',
  borderRadius: 'var(--theme-radius, 0)',
  boxShadow: 'var(--theme-shadow, 0 2px 8px 0 #0001)'
}))

const navLinkStyle = {
  color: 'var(--theme-border)',
}
</script>

<style scoped>
.navbar-theme {
  transition: background 0.3s, box-shadow 0.3s, backdrop-filter 0.3s;
}
.navbar-theme a.router-link-exact-active,
.navbar-theme a.router-link-active {
  color: var(--theme-accent) !important;
}
.navbar-theme a:hover {
  color: var(--theme-accent) !important;
}
</style>
