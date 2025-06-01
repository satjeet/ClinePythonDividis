import { defineStore } from 'pinia'
import axios from 'axios'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  
  // State
  const user = ref<any>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const userProfile = computed(() => user.value)

  // Actions
  async function login(username: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await axios.post('/api/token/', { username, password })
      token.value = response.data.access
      localStorage.setItem('token', response.data.access)
      
      // Configure axios
      axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      
      // Get user profile
      await fetchUserProfile()
      
      router.push('/dashboard')
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error de autenticación'
      token.value = null
      localStorage.removeItem('token')
    } finally {
      loading.value = false
    }
  }

  async function register(userData: {
    username: string
    password: string
    email: string
    first_name?: string
    last_name?: string
  }) {
    loading.value = true
    error.value = null
    try {
      await axios.post('/api/auth/register/', userData)
      await login(userData.username, userData.password)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error en el registro'
    } finally {
      loading.value = false
    }
  }

  async function fetchUserProfile() {
    if (!token.value) return
    
    try {
      const response = await axios.get('/api/auth/me/')
      user.value = response.data
    } catch (err) {
      logout()
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
    router.push('/login')
  }

  // Initialize
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
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
    
    // Actions
    login,
    register,
    logout,
    fetchUserProfile
  }
})
