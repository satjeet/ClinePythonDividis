<template>
  <div class="fixed top-4 right-4 z-50 flex flex-col gap-2">
    <transition-group name="toast-fade" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'px-4 py-2 rounded shadow-lg min-w-[220px] max-w-xs cursor-pointer',
          getToastClass(toast.type ?? '')
        ]"
        @click="toastStore.removeToast(toast.id)"
        title="Cerrar"
      >
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useGlobalToastStore } from '@/stores/globalToast'
import { useTheme } from '@/utils/useTheme'

const toastStore = useGlobalToastStore()
const { toasts } = storeToRefs(toastStore)
const { currentTheme } = useTheme()

function getToastClass(type: string) {
  const theme = currentTheme.value
  if (theme === 'theme-nebula-red') {
    return type === 'success'
      ? 'bg-red-600 text-white'
      : type === 'error'
      ? 'bg-red-900 text-white'
      : 'bg-red-400 text-white'
  }
  if (theme === 'theme-solar-flare') {
    return type === 'success'
      ? 'bg-yellow-500 text-black'
      : type === 'error'
      ? 'bg-orange-800 text-white'
      : 'bg-yellow-300 text-black'
  }
  if (theme === 'theme-stellar-gold') {
    return type === 'success'
      ? 'bg-yellow-400 text-black'
      : type === 'error'
      ? 'bg-yellow-800 text-white'
      : 'bg-yellow-200 text-black'
  }
  if (theme === 'theme-cosmic-silver') {
    return type === 'success'
      ? 'bg-gray-400 text-black'
      : type === 'error'
      ? 'bg-gray-700 text-white'
      : 'bg-gray-200 text-black'
  }
  if (theme === 'theme-phone-modern') {
    return type === 'success'
      ? 'bg-blue-500 text-white'
      : type === 'error'
      ? 'bg-blue-900 text-white'
      : 'bg-blue-300 text-black'
  }
  // Fallback
  return type === 'success'
    ? 'bg-green-600 text-white'
    : type === 'error'
    ? 'bg-red-600 text-white'
    : 'bg-cosmic-400 text-white'
}
</script>

<style scoped>
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.3s;
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
}
</style>
