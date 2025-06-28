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

  function showToast(message: string, type: 'success' | 'info' | 'error' = 'success', duration = 3500) {
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
