import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface ToastMessage {
  id: number
  message: string
  type?: 'success' | 'info' | 'error'
  duration?: number
}

export const useGlobalToastStore = defineStore('globalToast', () => {
  const toasts = ref<ToastMessage[]>([])

  function showToast(message: string, type: 'success' | 'info' | 'error' = 'success', duration = 6000) {
    // Evitar duplicados: si ya existe un toast igual, no agregarlo
    if (toasts.value.some(t => t.message === message && t.type === type)) {
      return
    }
    const id = Date.now() + Math.random()
    toasts.value.push({ id, message, type, duration })
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  function removeToast(id: number) {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return {
    toasts,
    showToast,
    removeToast
  }
})
