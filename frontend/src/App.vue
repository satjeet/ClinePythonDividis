<template>
  <div class="bg-slate-950 min-h-screen overflow-x-hidden">
    <!-- Global Navigation for authenticated users -->
    <nav v-if="authStore.isAuthenticated" 
         class="fixed top-0 left-0 right-0 z-50 bg-slate-900/80 backdrop-blur-sm border-b border-cosmic-700/30">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
          <!-- Brand -->
          <RouterLink to="/dashboard" class="text-2xl font-bold text-cosmic-400">
            Dividis
          </RouterLink>

          <!-- Navigation Links -->
          <div class="flex items-center space-x-8">
            <RouterLink 
              to="/dashboard" 
              class="nav-link"
              active-class="text-cosmic-400">
              Panel Principal
            </RouterLink>

            <!-- Profile Menu -->
            <div class="relative" v-if="authStore.user">
              <button 
                @click="showProfileMenu = !showProfileMenu"
                class="flex items-center text-slate-300 hover:text-cosmic-400">
                <span class="mr-2">{{ authStore.user.username }}</span>
                <svg 
                  class="w-5 h-5" 
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24">
                  <path 
                    stroke-linecap="round" 
                    stroke-linejoin="round" 
                    stroke-width="2" 
                    d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <!-- Dropdown Menu -->
              <div v-if="showProfileMenu"
                   class="absolute right-0 mt-2 w-48 card-cosmic py-2"
                   @click.away="showProfileMenu = false">
                <RouterLink 
                  to="/profile"
                  class="block px-4 py-2 text-sm text-slate-300 hover:bg-cosmic-500/20">
                  Mi Perfil
                </RouterLink>
                <button 
                  @click="handleLogout"
                  class="block w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-red-500/20">
                  Cerrar Sesión
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main :class="{ 'pt-16': authStore.isAuthenticated }">
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const showProfileMenu = ref(false)

async function handleLogout() {
  await authStore.logout()
  showProfileMenu.value = false
  router.push('/login')
}
</script>

<style>
@import '@/assets/css/main.css';

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
