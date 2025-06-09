import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { User } from '@/types'
import { authApi } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userProfile = computed(() => user.value)
  const userLevel = computed(() => user.value?.profile?.current_level || 1)
  const userXP = computed(() => user.value?.profile?.experience_points || 0)

  // Actions
  async function login(username: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.login(username, password)
      token.value = response.data.access
      localStorage.setItem('token', response.data.access)
      
      // Get user profile
      await fetchUserProfile()
      
      router.push('/dashboard')
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error de autenticación'
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    } finally {
      loading.value = false
    }
  }

  async function register(userData: {
    username: string
    password: string
    email: string
  }) {
    loading.value = true
    error.value = null
    try {
      await authApi.register({
        username: userData.username,
        password: userData.password,
        email: userData.email
      })
      await login(userData.username, userData.password)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error en el registro'
    } finally {
      loading.value = false
    }
  }

  async function fetchUserProfile() {
    if (!token.value) {
      user.value = null
      return
    }
    try {
      const response = await authApi.getProfile()
      user.value = response.data
    } catch (err) {
      user.value = null
      logout()
    }
  }

  async function updateProfile(data: Partial<User>) {
    loading.value = true
    error.value = null
    try {
      const response = await authApi.updateProfile(data)
      user.value = response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al actualizar perfil'
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  // Initialize
  if (token.value) {
    fetchUserProfile()
  }

  return {
    // State
    user,
    token,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    userProfile,
    userLevel,
    userXP,
    
    // Actions
    login,
    register,
    logout,
    fetchUserProfile,
    updateProfile
  }
})
