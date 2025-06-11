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
  const userProfile = computed(() => {
    if (!user.value) return null
    return user.value
  })
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
      // Si la respuesta es solo {email, first_name, last_name}, actualiza solo esos campos
      if ('email' in response.data && 'first_name' in response.data && 'last_name' in response.data) {
        user.value = {
          ...(user.value ?? {}),
          email: response.data.email,
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          id: user.value?.id ?? 0,
          username: user.value?.username ?? '',
          profile: user.value?.profile ?? {
            experience_points: 0,
            current_level: 1,
            created_at: '',
            updated_at: ''
          }
        }
      } else {
        user.value = response.data
      }
    } catch (err) {
      user.value = null
      logout()
    }
  }

  async function updateProfile(data: any) {
    loading.value = true
    error.value = null
    try {
      console.log('2. Store: updateProfile llamado con:', data)
      const response = await authApi.updateProfile(data)
      console.log('4. Respuesta de PATCH:', response)
      // Actualiza solo los campos de perfil editables
      user.value = {
        ...(user.value ?? {}),
        email: response.data.email,
        first_name: response.data.first_name,
        last_name: response.data.last_name,
        id: user.value?.id ?? 0,
        username: user.value?.username ?? '',
        profile: user.value?.profile ?? {
          experience_points: 0,
          current_level: 1,
          created_at: '',
          updated_at: ''
        }
      }
    } catch (err: any) {
      console.error('Error en updateProfile:', err);
      error.value = err.response?.data?.detail || err.message || 'Error al actualizar perfil'
      throw err;
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
