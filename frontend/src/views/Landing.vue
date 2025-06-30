<template>
  <!-- Main container -->
  <div class="min-h-screen bg-slate-950">
    <!-- Navigation -->
    <nav class="absolute top-0 left-0 right-0 z-50">
      <div class="container mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <!-- Logo -->
          <RouterLink to="/" class="text-2xl font-bold text-cosmic-100">
            Dividis
          </RouterLink>

          <!-- Nav links -->
          <div class="flex items-center gap-4">
            <RouterLink 
              v-if="authStore.isAuthenticated"
              to="/dashboard" 
              class="text-slate-400 hover:text-cosmic-400 transition-colors">
              Dashboard
            </RouterLink>
            <template v-else>
              <button 
                @click="openLoginModal"
                class="text-slate-400 hover:text-cosmic-400 transition-colors">
                Iniciar Sesión
              </button>
<Button @click="goToRegister">
  Registrarse
</Button>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero section -->
<HeroSection 
  @register="goToRegister"
  @login="openLoginModal"
/>

    <!-- Auth Modals -->
    <Teleport to="body">
      <!-- Login Modal -->
      <div v-if="showLoginModal" 
           class="fixed inset-0 bg-slate-950/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <Card class="w-full max-w-md">
          <template #header>
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold text-cosmic-100">Iniciar Sesión</h2>
              <button 
                @click="closeLoginModal"
                class="text-slate-400 hover:text-cosmic-400 transition-colors">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </template>

          <form @submit.prevent="handleLogin" class="space-y-6">
            <FormInput
              id="login-username"
              v-model="loginForm.username"
              label="Usuario"
              type="text"
              required
            />
            <FormInput
              id="login-password"
              v-model="loginForm.password"
              label="Contraseña"
              type="password"
              required
            />

            <div v-if="loginError" class="text-red-500 text-sm">
              {{ loginError }}
            </div>

            <Button 
              type="submit"
              :loading="loading"
              fullWidth>
              Entrar
            </Button>

            <p class="text-center text-slate-400">
              ¿No tienes una cuenta?
              <button 
                type="button"
                @click="switchToRegister"
                class="text-cosmic-400 hover:underline">
                Regístrate
              </button>
            </p>
          </form>
        </Card>
      </div>

      <!-- Register Modal -->
      <div v-if="showRegisterModal"
           class="fixed inset-0 bg-slate-950/90 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <Card class="w-full max-w-md">
          <template #header>
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold text-cosmic-100">Registro</h2>
              <button 
                @click="closeRegisterModal"
                class="text-slate-400 hover:text-cosmic-400 transition-colors">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </template>

          <form @submit.prevent="handleRegister" class="space-y-6">
            <FormInput
              id="register-username"
              v-model="registerForm.username"
              label="Usuario"
              type="text"
              required
            />
            <FormInput
              id="register-email"
              v-model="registerForm.email"
              label="Email"
              type="email"
              required
            />
            <FormInput
              id="register-password"
              v-model="registerForm.password"
              label="Contraseña"
              type="password"
              required
            />

            <div v-if="registerError" class="text-red-500 text-sm">
              {{ registerError }}
            </div>

            <Button 
              type="submit"
              :loading="loading"
              fullWidth>
              Crear Cuenta
            </Button>

            <p class="text-center text-slate-400">
              ¿Ya tienes una cuenta?
              <button 
                type="button"
                @click="switchToLogin"
                class="text-cosmic-400 hover:underline">
                Inicia sesión
              </button>
            </p>
          </form>
        </Card>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HeroSection from '@/components/landing/HeroSection.vue'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import FormInput from '@/components/ui/FormInput.vue'

const router = useRouter()
const authStore = useAuthStore()

// Form state
const loading = ref(false)
const loginError = ref('')
const registerError = ref('')

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  email: '',
  password: ''
})

// Modal state
const showLoginModal = ref(false)
const showRegisterModal = ref(false)

const goToRegister = () => {
  router.push('/register')
}

// Modal actions
const openLoginModal = () => {
  showLoginModal.value = true
  showRegisterModal.value = false
}

const closeLoginModal = () => {
  showLoginModal.value = false
  loginForm.value = { username: '', password: '' }
  loginError.value = ''
}

const openRegisterModal = () => {
  showRegisterModal.value = true
  showLoginModal.value = false
}

const closeRegisterModal = () => {
  showRegisterModal.value = false
  registerForm.value = { username: '', email: '', password: '' }
  registerError.value = ''
}

const switchToLogin = () => {
  closeRegisterModal()
  openLoginModal()
}

const switchToRegister = () => {
  closeLoginModal()
  openRegisterModal()
}

// Form handlers
async function handleLogin() {
  loading.value = true
  loginError.value = ''

  try {
    await authStore.login(loginForm.value.username, loginForm.value.password)
    closeLoginModal()
    router.push('/dashboard')
  } catch (err: any) {
    loginError.value = err.message || 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  loading.value = true
  registerError.value = ''

  try {
    await authStore.register(registerForm.value)
    closeRegisterModal()
    router.push('/dashboard')
  } catch (err: any) {
    registerError.value = err.message || 'Error al crear la cuenta'
  } finally {
    loading.value = false
  }
}
</script>
