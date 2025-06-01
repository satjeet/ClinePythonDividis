<template>
  <div class="min-h-screen bg-slate-950">
    <!-- Page transitions -->
    <RouterView v-slot="{ Component }">
      <Transition
        name="page"
        mode="out-in"
        appear
      >
        <component :is="Component" />
      </Transition>
    </RouterView>

    <!-- Loading overlay -->
    <div v-if="loading" 
         class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/90 backdrop-blur-sm">
      <div class="text-center space-y-4">
        <div class="animate-cosmic-spin w-12 h-12 border-2 border-cosmic-500 rounded-full border-t-transparent mx-auto"></div>
        <p class="text-cosmic-400">Cargando...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)

// Global navigation guard for loading state
router.beforeEach(() => {
  loading.value = true
})

router.afterEach(() => {
  loading.value = false
})

// Handle authentication errors globally
router.beforeEach(async (to) => {
  // Check if route requires auth
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // Check if user is authenticated for auth pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'dashboard' }
  }

  return true
})
</script>

<style>
/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Loading animation */
@keyframes cosmic-spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-cosmic-spin {
  animation: cosmic-spin 1s linear infinite;
}

/* Root styles */
:root {
  color-scheme: dark;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Focus outline styles */
:focus-visible {
  @apply outline-none ring-2 ring-cosmic-500/50;
}

/* Selection styles */
::selection {
  @apply bg-cosmic-500/20 text-cosmic-100;
}
</style>
