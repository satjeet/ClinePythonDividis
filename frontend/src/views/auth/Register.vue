<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center p-4">
    <Card class="w-full max-w-md">
      <template #header>
        <div class="text-center">
          <h1 class="text-2xl font-bold text-cosmic-100">Únete a la aventura</h1>
          <p class="text-slate-400 mt-2">Crea tu cuenta para comenzar tu viaje</p>
        </div>
      </template>

      <!-- Register form -->
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Username -->
        <FormInput
          id="username"
          v-model="form.username"
          label="Usuario"
          type="text"
          required
          :error="errors.username"
          @blur="validateUsername"
        />

        <!-- Email -->
        <FormInput
          id="email"
          v-model="form.email"
          label="Email"
          type="email"
          required
          :error="errors.email"
          @blur="validateEmail"
        />

        <!-- Password -->
        <FormInput
          id="password"
          v-model="form.password"
          label="Contraseña"
          type="password"
          required
          :error="errors.password"
          @blur="validatePassword"
        />

        <!-- Password confirmation -->
        <FormInput
          id="password_confirmation"
          v-model="form.password_confirmation"
          label="Confirmar contraseña"
          type="password"
          required
          :error="errors.password_confirmation"
          @blur="validatePasswordConfirmation"
        />

        <!-- Name fields -->
        <div class="grid grid-cols-2 gap-4">
          <FormInput
            id="first_name"
            v-model="form.first_name"
            label="Nombre"
            type="text"
          />

          <FormInput
            id="last_name"
            v-model="form.last_name"
            label="Apellido"
            type="text"
          />
        </div>

        <!-- Error message -->
        <div v-if="error" class="text-red-500 text-sm text-center">
          {{ error }}
        </div>

        <!-- Submit button -->
        <Button 
          type="submit"
          :loading="loading"
          fullWidth>
          Crear cuenta
        </Button>

        <!-- Login link -->
        <p class="text-center text-slate-400">
          ¿Ya tienes una cuenta?
          <RouterLink 
            :to="{ name: 'login' }"
            class="text-cosmic-400 hover:underline">
            Inicia sesión
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import FormInput from '@/components/ui/FormInput.vue'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')

// Form state
const form = reactive({
  username: '',
  email: '',
  password: '',
  password_confirmation: '',
  first_name: '',
  last_name: ''
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  password_confirmation: ''
})

// Validation
function validateUsername() {
  errors.username = ''
  if (!form.username) {
    errors.username = 'El usuario es requerido'
  } else if (form.username.length < 3) {
    errors.username = 'El usuario debe tener al menos 3 caracteres'
  }
}

function validateEmail() {
  errors.email = ''
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email) {
    errors.email = 'El email es requerido'
  } else if (!emailRegex.test(form.email)) {
    errors.email = 'Email inválido'
  }
}

function validatePassword() {
  errors.password = ''
  if (!form.password) {
    errors.password = 'La contraseña es requerida'
  } else if (form.password.length < 8) {
    errors.password = 'La contraseña debe tener al menos 8 caracteres'
  }
  validatePasswordConfirmation()
}

function validatePasswordConfirmation() {
  errors.password_confirmation = ''
  if (!form.password_confirmation) {
    errors.password_confirmation = 'Confirma tu contraseña'
  } else if (form.password !== form.password_confirmation) {
    errors.password_confirmation = 'Las contraseñas no coinciden'
  }
}

// Form submission
async function handleSubmit() {
  // Reset error
  error.value = ''

  // Validate all fields
  validateUsername()
  validateEmail()
  validatePassword()
  validatePasswordConfirmation()

  // Check for validation errors
  if (Object.values(errors).some(error => error)) {
    return
  }

  loading.value = true

  try {
    await authStore.register(form)
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.message || 'Error al crear la cuenta'
  } finally {
    loading.value = false
  }
}
</script>
