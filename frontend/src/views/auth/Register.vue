<template>
  <div class="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-bold text-cosmic-100">
        Comienza tu Viaje Cósmico
      </h2>
      <p class="mt-2 text-center text-sm text-slate-400">
        ¿Ya tienes una cuenta?
        <RouterLink 
          to="/login" 
          class="font-medium text-cosmic-400 hover:text-cosmic-300">
          Inicia Sesión
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
                v-model="form.username"
                name="username" 
                type="text" 
                required 
                class="input-cosmic w-full"
                :disabled="loading">
            </div>
          </div>

          <!-- Email field -->
          <div>
            <label 
              for="email" 
              class="block text-sm font-medium text-slate-300">
              Email
            </label>
            <div class="mt-1">
              <input 
                id="email" 
                v-model="form.email"
                name="email" 
                type="email" 
                required 
                class="input-cosmic w-full"
                :disabled="loading">
            </div>
          </div>

          <!-- Password fields -->
          <div>
            <label 
              for="password" 
              class="block text-sm font-medium text-slate-300">
              Contraseña
            </label>
            <div class="mt-1">
              <input 
                id="password" 
                v-model="form.password"
                name="password" 
                type="password" 
                required 
                class="input-cosmic w-full"
                :disabled="loading">
            </div>
          </div>

          <div>
            <label 
              for="password2" 
              class="block text-sm font-medium text-slate-300">
              Confirmar Contraseña
            </label>
            <div class="mt-1">
              <input 
                id="password2" 
                v-model="form.password2"
                name="password2" 
                type="password" 
                required 
                class="input-cosmic w-full"
                :disabled="loading">
            </div>
          </div>

          <!-- Optional fields -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label 
                for="first_name" 
                class="block text-sm font-medium text-slate-300">
                Nombre
              </label>
              <div class="mt-1">
                <input 
                  id="first_name" 
                  v-model="form.first_name"
                  name="first_name" 
                  type="text" 
                  class="input-cosmic w-full"
                  :disabled="loading">
              </div>
            </div>
            <div>
              <label 
                for="last_name" 
                class="block text-sm font-medium text-slate-300">
                Apellido
              </label>
              <div class="mt-1">
                <input 
                  id="last_name" 
                  v-model="form.last_name"
                  name="last_name" 
                  type="text" 
                  class="input-cosmic w-full"
                  :disabled="loading">
              </div>
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
              :disabled="loading || !isFormValid">
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
              {{ loading ? 'Registrando...' : 'Registrarse' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  password2: '',
  first_name: '',
  last_name: ''
})

const loading = ref(false)
const error = ref('')

const isFormValid = computed(() => {
  return (
    form.value.username &&
    form.value.email &&
    form.value.password &&
    form.value.password2 &&
    form.value.password === form.value.password2
  )
})

async function handleSubmit() {
  if (!isFormValid.value) {
    error.value = 'Por favor, completa todos los campos requeridos.'
    return
  }

  if (form.value.password !== form.value.password2) {
    error.value = 'Las contraseñas no coinciden.'
    return
  }

  loading.value = true
  error.value = ''
  
  try {
    await authStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      first_name: form.value.first_name,
      last_name: form.value.last_name
    })
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.message || 'Error al registrarse'
  } finally {
    loading.value = false
  }
}
</script>
