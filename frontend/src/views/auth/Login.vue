<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center p-4">
    <Card class="w-full max-w-md">
      <template #header>
        <div class="text-center">
          <h1 class="text-2xl font-bold text-cosmic-100">Bienvenido de nuevo</h1>
          <p class="text-slate-400 mt-2">Inicia sesión para continuar tu viaje</p>
        </div>
      </template>

      <!-- Login form -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <FormInput
          id="username"
          v-model="form.username"
          label="Usuario"
          type="text"
          required
          :error="errors.username"
          @blur="validateUsername"
        />

        <FormInput
          id="password"
          v-model="form.password"
          label="Contraseña"
          type="password"
          required
          :error="errors.password"
          @blur="validatePassword"
        >
          <template #help>
            <span class="text-xs text-slate-400">Mínimo 8 caracteres</span>
          </template>
        </FormInput>

        <!-- Error message -->
        <div v-if="error" class="text-red-500 text-sm text-center">
          {{ error }}
        </div>

        <!-- Submit button -->
        <Button 
          type="submit"
          :loading="loading"
          fullWidth>
          Iniciar sesión
        </Button>

        <!-- Register link -->
        <p class="text-center text-slate-400">
          ¿No tienes una cuenta?
          <RouterLink 
            :to="{ name: 'register' }"
            class="text-cosmic-400 hover:underline">
            Regístrate
          </RouterLink>
        </p>
      </form>

      <!-- Divider -->
      <div class="relative my-8">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-cosmic-700/30"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-slate-900 text-slate-400">O</span>
        </div>
      </div>

      <!-- Back to home -->
      <div class="text-center">
        <RouterLink 
          to="/"
          class="text-slate-400 hover:text-cosmic-400 transition-colors inline-flex items-center">
          <i class="fas fa-arrow-left mr-2"></i>
          Volver al inicio
        </RouterLink>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import FormInput from '@/components/ui/FormInput.vue'

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
</script>
