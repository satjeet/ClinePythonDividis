<template>
  <div class="bg-slate-900/50 backdrop-blur-sm border border-cosmic-700/30 rounded-lg p-6">
    <div class="flex items-center justify-between mb-6">
      <!-- User info -->
      <div class="flex items-center space-x-4">
        <!-- Avatar placeholder -->
        <div class="w-12 h-12 rounded-full bg-cosmic-500/20 flex items-center justify-center">
          <span class="text-lg font-bold text-cosmic-400">
            {{ getInitials(username) }}
          </span>
        </div>

        <!-- User details -->
        <div>
          <h2 class="text-xl font-bold text-cosmic-100">{{ username }}</h2>
          <p class="text-sm text-slate-400">
            Nivel {{ level }} • {{ xp }} XP
          </p>
        </div>
      </div>

      <!-- Current streak -->
      <div class="text-right">
        <p class="text-sm text-slate-400">Mejor racha</p>
        <p class="text-2xl font-bold text-cosmic-400">{{ longestStreak }} días</p>
      </div>
    </div>

    <!-- Progress bar -->
    <div class="space-y-2">
      <div class="flex justify-between text-sm">
        <span class="text-slate-400">
          Nivel {{ level }}
        </span>
        <span class="text-slate-400">
          {{ xpToNextLevel }} XP para nivel {{ level + 1 }}
        </span>
      </div>
      <div class="w-full bg-slate-800 rounded-full h-2">
        <div 
          class="bg-cosmic-500 h-2 rounded-full transition-all duration-500"
          :style="{
            width: `${levelProgress}%`
          }">
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-6 mt-6">
      <div>
        <p class="text-sm text-slate-400">Módulos Desbloqueados</p>
        <p class="text-2xl font-bold text-cosmic-400">{{ stats.modules_unlocked }}</p>
      </div>
      <div>
        <p class="text-sm text-slate-400">Misiones Completadas</p>
        <p class="text-2xl font-bold text-cosmic-400">{{ stats.missions_completed }}</p>
      </div>
      <div>
        <p class="text-sm text-slate-400">Logros Obtenidos</p>
        <p class="text-2xl font-bold text-cosmic-400">{{ stats.achievements_earned }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  username: string
  level: number
  xp: number
  stats: {
    modules_unlocked: number
    missions_completed: number
    achievements_earned: number
  }
  longestStreak: number
}

const props = defineProps<Props>()

// Computed values
const xpForCurrentLevel = computed(() => (props.level - 1) * 100)
const xpForNextLevel = computed(() => props.level * 100)
const xpProgress = computed(() => props.xp - xpForCurrentLevel.value)
const xpToNextLevel = computed(() => xpForNextLevel.value - props.xp)
const levelProgress = computed(() => 
  (xpProgress.value / (xpForNextLevel.value - xpForCurrentLevel.value)) * 100
)

// Methods
function getInitials(name: string): string {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
</script>

<style scoped>
.progress-pulse {
  animation: progress-pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes progress-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .7;
  }
}
</style>
