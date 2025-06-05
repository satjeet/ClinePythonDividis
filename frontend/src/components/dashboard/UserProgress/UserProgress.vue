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

    <!-- Barra de experiencia visual integrada -->
    <div class="flex flex-col w-full mb-4">
      <div class="flex items-center justify-between mb-1">
        <span class="text-cosmic-300 font-bold text-lg">Nivel {{ level }}</span>
        <span class="text-cosmic-400 font-semibold">
          {{ getTitle(level) }}
        </span>
      </div>
      <div class="w-full bg-cosmic-700/30 rounded-full h-3 relative">
        <div class="bg-cosmic-400 h-3 rounded-full" :style="{ width: `${levelProgress}%` }"></div>
        <span class="absolute right-2 top-0 text-xs text-cosmic-100 font-mono">{{ xpProgress }} / {{ xpForNextLevel - xpForCurrentLevel }} XP</span>
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
const levelProgress = computed(() => 
  (xpProgress.value / (xpForNextLevel.value - xpForCurrentLevel.value)) * 100
)

// Título cósmico mock según nivel
function getTitle(level: number): string {
  if (level < 5) return 'Navegante Novato'
  if (level < 10) return 'Explorador Estelar'
  if (level < 20) return 'Guardián Cósmico'
  return 'Maestro Estelar'
}

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
