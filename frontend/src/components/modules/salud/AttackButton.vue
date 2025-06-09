<template>
  <div class="attack-button cosmic-card mb-4 flex flex-col items-center relative">
    <button
      class="bg-pink-600 hover:bg-pink-700 text-white font-bold py-2 px-6 rounded-full shadow-lg transition"
      :disabled="isAttacking || !canAttack"
      @click="attack"
    >
      <span v-if="!isAttacking">
        Atacar Zona de Confort
        <span v-if="canAttack" class="ml-2 text-yellow-300 font-bold">-{{ damage }} HP</span>
      </span>
      <span v-else>Atacando...</span>
    </button>
    <span v-if="lastAttackText" class="text-xs text-gray-400 mt-2">
      Último ataque: {{ lastAttackText }}
    </span>
    <span v-if="errorMsg" class="text-xs text-red-400 mt-2">{{ errorMsg }}</span>
    <transition name="toast-fade">
      <div
        v-if="showToast"
        class="fixed top-8 left-1/2 -translate-x-1/2 bg-pink-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 text-lg font-bold animate-bounce"
        style="pointer-events:none;"
      >
        ¡Ataque! -{{ lastDamage }} HP
        <div class="text-xs mt-1">
          <span v-for="(h, i) in habitContribs" :key="h.id">
            {{ h.nombre }}: -{{ h.daño }}<span v-if="i < habitContribs.length-1">, </span>
          </span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useWallStore } from './stores/wallStore'
import { useHabitStore } from './stores/habitStore'
import axios from 'axios'

const wallStore = useWallStore()
const habitStore = useHabitStore()
const isAttacking = ref(false)
const errorMsg = ref('')
const showToast = ref(false)
const lastDamage = ref(0)

const lastAttackDate = computed(() => wallStore.wall?.fecha_ultimo_ataque)
const today = new Date().toISOString().slice(0, 10)
const canAttack = computed(() => {
  if (!lastAttackDate.value) return true
  return lastAttackDate.value < today
})

const lastAttackText = computed(() => {
  if (!lastAttackDate.value) return 'Nunca'
  if (lastAttackDate.value === today) return 'Hoy'
  return lastAttackDate.value
})

// Lógica de daño: cada hábito activo suma 5 + días_activos*1
const habitContribs = computed(() =>
  habitStore.habits
    .filter(h => h.estado === 'activo' || h.estado === 'incubando')
    .map(h => ({
      id: h.id,
      nombre: h.nombre,
      daño: 5 + (h.dias_activos || 0)
    }))
)
const damage = computed(() =>
  habitContribs.value.reduce((sum, h) => sum + h.daño, 0)
)

async function attack() {
  errorMsg.value = ''
  isAttacking.value = true
  lastDamage.value = damage.value
  try {
    if (!wallStore.wall) throw new Error('No hay muro cargado')
    await axios.patch(`/api/comfortwall/${wallStore.wall.id}/`, {
      fecha_ultimo_ataque: today,
      hp_actual: Math.max(0, wallStore.wall.hp_actual - damage.value)
    })
    await wallStore.fetchWall()
    showToast.value = true
    setTimeout(() => { showToast.value = false }, 2200)
  } catch (e: any) {
    errorMsg.value = e?.message || 'Error al atacar'
  } finally {
    isAttacking.value = false
  }
}
</script>

<style scoped>
.attack-button {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.5s;
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
}
</style>
