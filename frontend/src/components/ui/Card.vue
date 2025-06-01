<template>
  <div 
    :class="[
      'card-cosmic relative',
      variant === 'interactive' ? 'transform transition-transform duration-300 hover:-translate-y-1' : '',
      className
    ]"
  >
    <!-- Header -->
    <div v-if="$slots.header" class="border-b border-cosmic-700/30 pb-4 mb-4">
      <slot name="header"></slot>
    </div>

    <!-- Content -->
    <div :class="{ 'p-6': padding }">
      <slot></slot>
    </div>

    <!-- Footer -->
    <div v-if="$slots.footer" class="border-t border-cosmic-700/30 pt-4 mt-4">
      <slot name="footer"></slot>
    </div>

    <!-- Overlay for locked state -->
    <div 
      v-if="locked"
      class="absolute inset-0 bg-slate-950/50 backdrop-blur-sm rounded-lg flex items-center justify-center">
      <div class="text-center">
        <svg 
          class="w-8 h-8 text-slate-500 mx-auto mb-2" 
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor">
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
        <span class="text-sm text-slate-400">{{ lockedMessage }}</span>
      </div>
    </div>

    <!-- Loading overlay -->
    <div 
      v-if="loading"
      class="absolute inset-0 bg-slate-950/50 backdrop-blur-sm rounded-lg flex items-center justify-center">
      <div class="text-center">
        <div class="animate-cosmic-spin w-8 h-8 border-2 border-cosmic-500 rounded-full border-t-transparent mb-2 mx-auto"></div>
        <span class="text-sm text-slate-400">{{ loadingMessage || 'Cargando...' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'default' | 'interactive'
  className?: string
  padding?: boolean
  locked?: boolean
  lockedMessage?: string
  loading?: boolean
  loadingMessage?: string
}

withDefaults(defineProps<Props>(), {
  variant: 'default',
  className: '',
  padding: true,
  locked: false,
  lockedMessage: 'Bloqueado',
  loading: false,
  loadingMessage: ''
})
</script>

<style scoped>
@keyframes cosmic-spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-cosmic-spin {
  animation: cosmic-spin 1s linear infinite;
}
</style>
