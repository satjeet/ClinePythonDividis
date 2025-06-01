import axios from 'axios'
import type { User, Module, Mission, ModuleProgress, MissionProgress } from '@/types'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth endpoints
export const authApi = {
  login: (username: string, password: string) => 
    api.post('/api/token/', { username, password }),

  register: (userData: {
    username: string
    password: string
    email: string
    first_name?: string
    last_name?: string
  }) => api.post('/api/auth/register/', userData),

  getProfile: () => 
    api.get<User>('/api/auth/me/'),

  updateProfile: (data: Partial<User>) =>
    api.patch('/api/auth/me/', data)
}

// Module endpoints
export const moduleApi = {
  getAll: () => 
    api.get<Module[]>('/api/modules/'),

  unlock: (moduleId: string) =>
    api.post<ModuleProgress>(`/api/modules/${moduleId}/unlock/`),

  getProgress: (moduleId: string) =>
    api.get(`/api/progress/module/${moduleId}/`)
}

// Mission endpoints
export const missionApi = {
  getAll: () => 
    api.get<Mission[]>('/api/missions/'),

  complete: (missionId: string) =>
    api.post<MissionProgress>(`/api/missions/${missionId}/complete/`)
}

// Progress endpoints
export const progressApi = {
  getOverview: () =>
    api.get('/api/progress/overview/')
}

export default api
