import axios from 'axios'
import type { User, Module, Mission, ModuleProgress, MissionProgress } from '@/types'

// Create axios instance
const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL || '') + '/api',
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
    api.post('/token/', { username, password }),

  register: (userData: {
    username: string
    password: string
    email: string
    first_name?: string
    last_name?: string
  }) => api.post('/auth/register/', userData),

  getProfile: () => 
    api.get<User>('/auth/me/'),

  updateProfile: (data: Partial<User>) =>
    api.patch('/auth/me/', data)
}

// Module endpoints
export const moduleApi = {
  getAll: () => 
    api.get<Module[]>('/modules/'),

  unlock: (moduleId: string) =>
    api.post<ModuleProgress>(`/modules/${moduleId}/unlock/`),

  getProgress: (moduleId: string) =>
    api.get(`/progress/module/${moduleId}/`)
}

// Mission endpoints
export const missionApi = {
  getAll: () => 
    api.get<Mission[]>('/missions/'),

  complete: (missionId: string) =>
    api.post<MissionProgress>(`/missions/${missionId}/complete/`)
}

// Progress endpoints
export const progressApi = {
  getOverview: () =>
    api.get('/progress/overview/')
}

export default api
