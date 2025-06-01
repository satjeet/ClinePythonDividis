<template>
  <div class="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-bold text-cosmic-100">
        Bienvenido de nuevo
      </h2>
      <p class="mt-2 text-center text-sm text-slate-400">
        ¿Aún no tienes una cuenta?
        <RouterLink 
          to="/register" 
          class="font-medium text-cosmic-400 hover:text-cosmic-300">
          Regístrate
        </RouterLink>
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="card-cosmic py-8 px-4 sm:px-10">
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <!-- Username field -->
          <div>
            <label 
              for="username" 
              class="block text-sm font-medium text-slate-300">
              Usuario
            </label>
            <div class="mt-1">
              <input 
                id="username" 
                v-model="username"
                name="username" 
                type="text" 
                required 
                class="input-cosmic w-full"
                :disabled="loading">
            </div>
          </div>

          <!-- Password field -->
          <div>
            <label 
              for="password" 
              class="block text-sm font-medium text-slate-300">
              Contraseña
            </label>
            <div class="mt-1">
              <input 
                id="password" 
                v-model="password"
                name="password" 
                type="password" 
                required 
                class="input-cosmic w-full"
                :disabled="loading">
            </div>
          </div>

          <!-- Error display -->
          <div v-if="error" class="text-red-500 text-sm">
            {{ error }}
          </div>

          <!-- Submit button -->
          <div>
            <button 
              type="submit" 
              class="btn-cosmic w-full flex justify-center py-2 px-4"
              :disabled="loading">
              <svg v-if="loading"
                   class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" 
                   xmlns="http://www.w3.org/2000/svg" 
                   fill="none" 
                   viewBox="0 0 24 24">
                <circle 
                  class="opacity-25" 
                  cx="12" 
                  cy="12" 
                  r="10" 
                  stroke="currentColor" 
                  stroke-width="4">
                </circle>
                <path 
                  class="opacity-75" 
                  fill="currentColor" 
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              {{ loading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
            </button>
          </div>
        </form>

        <!-- Social auth options (placeholder for future) -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-slate-700"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-slate-900 text-slate-400">
                O continúa con
              </span>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-2 gap-3">
            <div>
              <button
                type="button"
                disabled
                class="btn-cosmic w-full bg-transparent border border-cosmic-700/30 opacity-50 cursor-not-allowed">
                Google
              </button>
            </div>
            <div>
              <button
                type="button"
                disabled
                class="btn-cosmic w-full bg-transparent border border-cosmic-700/30 opacity-50 cursor-not-allowed">
                GitHub
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  
  try {
    await authStore.login(username.value, password.value)
    const redirectPath = route.query.redirect?.toString() || '/dashboard'
    router.push(redirectPath)
  } catch (err: any) {
    error.value = err.message || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>
