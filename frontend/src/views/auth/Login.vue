<template>
  <div class="min-h-screen flex items-center justify-center px-2 py-8" :style="{ background: 'var(--theme-bg)' }">
    <Card variant="interactive" className="w-full max-w-md mx-auto flex flex-col items-center relative animate-profile-fadein">
      <!-- Logo Dividis: D estilizada y línea divisoria -->
      <svg style="width:56px;height:56px;margin-bottom:1.5rem;" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="28" cy="28" r="28" :fill="`var(--theme-accent, #fff)`" fill-opacity="0.08"/>
        <path d="M20 16h8a8 8 0 1 1 0 24h-8V16z" :fill="`var(--theme-accent, #fff)`" fill-opacity="0.95"/>
        <rect x="24" y="22" width="12" height="2.5" rx="1.25" :fill="`var(--theme-border, #3b82f6)`"/>
      </svg>
      <div class="text-center">
        <h1 class="text-2xl font-bold mb-2" :style="{
          background: 'linear-gradient(90deg, var(--theme-accent), var(--theme-border))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }">Login.</h1>
        <p class="mb-4" :style="{ color: 'var(--theme-border)' }">Inicia sesión para continuar tu viaje</p>
      </div>
      <form @submit.prevent="handleSubmit" class="w-full flex flex-col gap-4">
        <input
          class="input-theme"
          id="username"
          v-model="form.username"
          placeholder="Usuario"
          type="text"
          required
          @blur="validateUsername"
        />
        <input
          class="input-theme"
          id="password"
          v-model="form.password"
          placeholder="Contraseña"
          type="password"
          required
          @blur="validatePassword"
        />
        <div v-if="error" class="mt-2 text-center" :style="{ color: 'var(--theme-border)' }">
          {{ error }}
        </div>
        <button type="submit" class="btn-theme w-full mt-4" :disabled="loading">
          {{ loading ? 'Cargando...' : 'Login' }}
        </button>
        <div class="text-center mt-2" :style="{ color: 'var(--theme-border)' }">
          ¿No tienes una cuenta?
          <RouterLink :to="{ name: 'register' }" :style="{ color: 'var(--theme-accent)' }">Regístrate</RouterLink>
        </div>
      </form>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')

// Form state
const form = reactive({
  username: '',
  password: ''
})

const errors = reactive({
  username: '',
  password: ''
})

// Validation
function validateUsername() {
  errors.username = form.username ? '' : 'El usuario es requerido'
}

function validatePassword() {
  if (!form.password) {
    errors.password = 'La contraseña es requerida'
  } else if (form.password.length < 8) {
    errors.password = 'La contraseña debe tener al menos 8 caracteres'
  } else {
    errors.password = ''
  }
}

// Form submission
async function handleSubmit() {
  // Reset errors
  error.value = ''
  validateUsername()
  validatePassword()

  // Check for validation errors
  if (errors.username || errors.password) {
    return
  }

  loading.value = true

  try {
    await authStore.login(form.username, form.password)
    // Redirect to intended page or dashboard
    const redirectTo = route.query.redirect?.toString() || '/dashboard'
    router.push(redirectTo)
  } catch (err: any) {
    // Mostrar mensajes claros según el error del backend
    if (err?.response?.data?.detail) {
      if (err.response.data.detail === "No active account found with the given credentials") {
        error.value = "Usuario o contraseña incorrectos."
      } else {
        error.value = err.response.data.detail
      }
    } else {
      error.value = err.message || 'Error al iniciar sesión'
    }
  } finally {
    loading.value = false
  }
}

/* No forzar ningún theme, el theme activo se maneja globalmente */
</script>
