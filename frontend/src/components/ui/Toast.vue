<template>
  <div class="fixed top-4 right-4 z-50 flex flex-col gap-2">
    <transition-group name="toast-fade" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'px-4 py-2 rounded shadow-lg text-white min-w-[220px] max-w-xs',
          toast.type === 'success' ? 'bg-green-600' :
          toast.type === 'error' ? 'bg-red-600' : 'bg-cosmic-400'
        ]"
      >
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useGlobalToastStore } from '@/stores/globalToast'

const toastStore = useGlobalToastStore()
const { toasts } = storeToRefs(toastStore)
</script>

<style scoped>
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.3s;
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
}
</style>
