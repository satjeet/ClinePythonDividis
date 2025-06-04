<template>
  <div class="form-field">
    <!-- Label -->
    <label 
      v-if="label"
      :for="id" 
      class="block text-sm font-medium text-slate-300 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>

    <!-- Input wrapper -->
    <div class="relative">
      <!-- Input field -->
      <input
        :id="id"
        :ref="id"
        v-model="inputValue"
        :type="type"
        :name="name"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        :class="[
          'input-cosmic w-full',
          error ? 'border-red-500 focus:border-red-500' : '',
          className
        ]"
        @input="handleInput"
        @blur="handleBlur"
      >

      <!-- Error icon -->
      <div v-if="error" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>

    <!-- Help text -->
    <p v-if="helpText" class="mt-1 text-sm text-slate-400">
      {{ helpText }}
    </p>

    <!-- Error message -->
    <p v-if="error" class="mt-1 text-sm text-red-500">
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  id: string
  modelValue: string | number
  label?: string
  type?: 'text' | 'password' | 'email' | 'number'
  name?: string
  placeholder?: string
  helpText?: string
  error?: string
  required?: boolean
  disabled?: boolean
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  name: '',
  placeholder: '',
  helpText: '',
  error: '',
  required: false,
  disabled: false,
  className: ''
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'blur'): void
}>()

const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value.toString())
})

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value.toString())
}

function handleBlur() {
  emit('blur')
}

// Focus method exposed to parent
defineExpose({
  focus: () => {
    const input = document.getElementById(props.id)
    if (input) {
      input.focus()
    }
  }
})
</script>

<style scoped>
.form-field {
  @apply space-y-1;
}

.input-cosmic {
  @apply bg-slate-900 border border-cosmic-700/30 rounded-lg px-4 py-2 text-slate-200;
  @apply focus:outline-none focus:ring-2 focus:ring-cosmic-500/50 focus:border-cosmic-500;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
  @apply placeholder:text-slate-500;
}
</style>
