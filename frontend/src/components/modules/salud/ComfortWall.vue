<template>
  <div class="comfort-wall cosmic-card mb-4 relative">
    <h2 class="font-semibold mb-2">Zona de Confort</h2>
    <div v-if="!wallLoaded" class="text-blue-400 text-xs py-4">Cargando muro de confort...</div>
    <div v-else>
      <div class="wall-bar bg-gray-700 rounded h-6 w-full relative overflow-hidden">
        <div
          class="wall-hp bg-green-400 h-6 rounded transition-all duration-700"
          :style="{ width: animatedPercent + '%' }"
        ></div>
        <span class="absolute left-2 top-0 text-xs text-white">
          HP: {{ hpActual }}/{{ hpMax }}
        </span>
      </div>
      <transition name="toast-fade">
        <div
          v-if="showDefeated"
          class="fixed top-8 left-1/2 -translate-x-1/2 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 text-lg font-bold animate-bounce"
          style="pointer-events:none;"
        >
          ¡Has derrotado tu muro de confort!
        </div>
      </transition>
      <transition name="toast-fade">
        <div
          v-if="showLevelUp"
          class="fixed top-20 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 text-lg font-bold animate-bounce"
          style="pointer-events:none;"
        >
          ¡Tu muro ha subido de nivel y se ha restaurado!
        </div>
      </transition>
      <button
        v-if="hpActual === 0"
        @click="levelUpWall"
        :disabled="!wallLoaded"
        class="mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-bold"
      >
        Subir nivel de confort y restaurar muro
      </button>
      <div v-if="levelUpError" class="text-xs text-red-400 mt-2">{{ levelUpError }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref, watch } from 'vue'
import { useWallStore } from './stores/wallStore'
import axios from 'axios'

const wallStore = useWallStore()
const wallLoaded = computed(() => !!wallStore.wall)
onMounted(() => {
  wallStore.fetchWall()
})

const hpActual = computed(() => wallStore.wall?.hp_actual ?? 0)
const hpMax = computed(() => wallStore.wall?.hp_max ?? 100)
const nivelMuro = computed(() => wallStore.wall?.nivel_muro ?? 1)
const fechaUltimoAtaque = computed(() => wallStore.wall?.fecha_ultimo_ataque ?? null)
const wallId = computed(() => wallStore.wall?.id)

const hpPercent = computed(() =>
  hpMax.value > 0 ? Math.round((hpActual.value / hpMax.value) * 100) : 0
)

// Animación suave del HP
const animatedPercent = ref(hpPercent.value)
watch(hpPercent, (newVal) => {
  setTimeout(() => {
    animatedPercent.value = newVal
  }, 50)
})

// Toast al derrotar el muro
const showDefeated = ref(false)
watch(hpActual, (newVal, oldVal) => {
  if (oldVal > 0 && newVal === 0) {
    showDefeated.value = true
    setTimeout(() => { showDefeated.value = false }, 2000)
  }
})

// Toast al subir de nivel
const showLevelUp = ref(false)

// Botón para subir nivel manualmente
const levelUpError = ref('')
async function levelUpWall() {
  levelUpError.value = ''
  try {
    if (!wallStore.wall) throw new Error('No hay muro cargado')
    await axios.patch(`/api/comfortwall/${wallId.value}/`, {
      hp_actual: 0,
      hp_max: hpMax.value,
      nivel_muro: nivelMuro.value,
      fecha_ultimo_ataque: fechaUltimoAtaque.value
    })
    await wallStore.fetchWall()
    showLevelUp.value = true
    setTimeout(() => { showLevelUp.value = false }, 2000)
  } catch (err) {
    const e = err as any;
    // eslint-disable-next-line no-console
    console.error('Error PATCH muro:', e, e?.response?.data);
    if (e.response && e.response.data) {
      levelUpError.value = JSON.stringify(e.response.data)
    } else if (e.message) {
      levelUpError.value = 'Error: ' + e.message
    } else {
      levelUpError.value = 'Error al subir nivel del muro'
    }
  }
}
</script>

<style scoped>
.comfort-wall {
  background: #23294a;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 2px 8px #0002;
}
.wall-bar {
  margin-top: 0.5rem;
}
.wall-hp {
  transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}
.toast-fade-enter-active, .toast-fade-leave-active {
  transition: opacity 0.5s;
}
.toast-fade-enter-from, .toast-fade-leave-to {
  opacity: 0;
}
</style>
