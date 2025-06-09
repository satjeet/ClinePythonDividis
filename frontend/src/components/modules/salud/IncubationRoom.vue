<template>
  <div class="incubation-room cosmic-card mb-4 relative">
    <h2 class="font-semibold mb-2">Salón de Incubación</h2>
    <form @submit.prevent="handleCreate" class="flex flex-col gap-2">
      <input v-model="nombre" type="text" placeholder="Nombre del hábito" class="input" required />
      <select v-model="dificultad" class="input" required>
        <option disabled value="">Dificultad</option>
        <option value="fácil">Fácil</option>
        <option value="media">Media</option>
        <option value="difícil">Difícil</option>
      </select>
      <input v-model="horario" type="time" class="input" />
      <button
        type="submit"
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        :disabled="!canCreate || habitStore.loading"
      >
        Crear Serpiente
      </button>
    </form>
    <div v-if="showNew" class="mt-4 flex flex-col items-center">
      <span class="text-green-400 text-lg">¡Nueva serpiente nacida!</span>
      <span class="text-3xl">🐍</span>
    </div>
    <transition name="toast-fade">
      <div
        v-if="showToast"
        class="fixed top-8 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 text-lg font-bold animate-bounce"
        style="pointer-events:none;"
      >
        ¡Tu serpiente ha sido creada!
      </div>
    </transition>
    <div v-if="errorMsg" class="text-red-400 text-xs mt-2">{{ errorMsg }}</div>
    <div v-if="habitStore.error" class="text-red-400 text-xs mt-2">{{ habitStore.error }}</div>
    <div v-if="!canCreate && !nombre.startsWith('test_')" class="text-xs text-yellow-400 mt-2">
      Solo puedes crear 3 hábitos al día.
    </div>
    <div class="text-xs text-gray-400 mt-2">
      canCreate: {{ canCreate ? 'true' : 'false' }}, loading: {{ habitStore.loading ? 'true' : 'false' }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHabitStore } from './stores/habitStore'

const habitStore = useHabitStore()
onMounted(() => {
  habitStore.fetchHabits()
})
const nombre = ref('')
const dificultad = ref('')
const horario = ref('')
const showNew = ref(false)
const showToast = ref(false)
const errorMsg = ref('')

const today = new Date().toISOString().slice(0, 10)
const safeHabits = computed(() => Array.isArray(habitStore.habits) ? habitStore.habits : [])
const habitsToday = computed(() =>
  safeHabits.value.filter(h => (h.fecha_creacion ?? '').slice(0, 10) === today)
)

const canCreate = computed(() => {
  if (nombre.value.startsWith('test_')) return true
  return habitsToday.value.length < 3
})

async function handleCreate() {
  errorMsg.value = ''
  if (!canCreate.value) {
    errorMsg.value = 'Solo puedes crear 3 hábitos al día.'
    return
  }
  await habitStore.createHabit({
    nombre: nombre.value,
    dificultad: dificultad.value,
    horario_sugerido: horario.value
  })
  showNew.value = true
  showToast.value = true
  setTimeout(() => {
    showNew.value = false
    showToast.value = false
    nombre.value = ''
    dificultad.value = ''
    horario.value = ''
  }, 1800)
}
</script>

<style scoped>
.incubation-room {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
.input {
  background: #1a223f;
  color: #fff;
  border: 1px solid #334155;
  border-radius: 6px;
  padding: 0.5rem;
}
.input:focus {
  outline: 2px solid #60a5fa;
}
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.5s;
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
}
</style>
