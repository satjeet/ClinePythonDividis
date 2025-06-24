// frontend/src/stores/globalLoader.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useModulesStore } from './modules'
import { useUserProgressStore } from './userProgress'
// Agrega aquí otros stores necesarios para la precarga global

export const useGlobalLoader = defineStore('globalLoader', () => {
  const isGlobalLoading = ref(false)
  const error = ref<string | null>(null)

  async function preloadAll() {
    isGlobalLoading.value = true
    error.value = null
    try {
      await Promise.all([
        useModulesStore().fetchModules(),
        useUserProgressStore().fetchProgress(),
        // Agrega aquí otras precargas necesarias
      ])
    } catch (e: any) {
      error.value = e.message || 'Error en la precarga global'
    } finally {
      isGlobalLoading.value = false
    }
  }

  return { isGlobalLoading, error, preloadAll }
})
