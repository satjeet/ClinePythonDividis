<template>
  <button
    :type="type"
    :class="[
      'btn-theme inline-flex items-center justify-center',
      variant !== 'default' ? variant : '',
      size === 'sm' ? 'text-sm px-3 py-1.5' : '',
      size === 'lg' ? 'text-lg px-6 py-3' : '',
      size === 'default' ? 'px-4 py-2' : '',
      fullWidth ? 'w-full' : '',
      loading ? 'opacity-50 cursor-not-allowed' : '',
      className
    ]"
    :disabled="disabled || loading"
    @click="$emit('click', $event)">
    <template v-if="loading">
      <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      {{ loadingText || 'Cargando...' }}
    </template>
    <template v-else>
      <slot></slot>
    </template>
  </button>
</template>

<script setup lang="ts">
interface Props {
  type?: 'button' | 'submit' | 'reset'
  variant?: 'default' | 'outline' | 'ghost' | 'link'
  size?: 'default' | 'sm' | 'lg'
  className?: string
  fullWidth?: boolean
  disabled?: boolean
  loading?: boolean
  loadingText?: string
}

withDefaults(defineProps<Props>(), {
  type: 'button',
  variant: 'default',
  size: 'default',
  className: '',
  fullWidth: false,
  disabled: false,
  loading: false,
  loadingText: ''
})

defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()
</script>
