import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Styles
import '@fortawesome/fontawesome-free/css/all.min.css'
import './assets/css/main.css'

// Configure GSAP
import { gsap } from 'gsap'
gsap.config({
  nullTargetWarn: false
})

// Configure axios defaults
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
axios.defaults.headers.common['Content-Type'] = 'application/json'

// Get token from localStorage if it exists
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// Create the app instance
const app = createApp(App)

// Use plugins
app.use(createPinia())
app.use(router)

// Global error handler
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Error info:', info)

  // Handle 401 Unauthorized errors
  if (axios.isAxiosError(err) && err.response?.status === 401) {
    localStorage.removeItem('token')
    router.push('/login')
  }
}

// Mount the app
app.mount('#app')
