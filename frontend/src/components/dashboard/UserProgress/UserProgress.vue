<template>
  <div class="card-theme">
    <div class="flex items-center justify-between mb-6">
      <!-- User info -->
      <div class="flex items-center space-x-4">
        <!-- Avatar placeholder -->
        <div class="w-12 h-12 rounded-full flex items-center justify-center"
             :style="{ background: 'color-mix(in srgb, var(--theme-accent) 20%, transparent 80%)' }">
          <span class="text-lg font-bold" :style="{ color: 'var(--theme-accent)' }">
            {{ getInitials(username) }}
          </span>
        </div>

        <!-- User details -->
        <div>
          <h2 class="text-xl font-bold" :style="{ color: 'var(--theme-accent)' }">{{ username }}</h2>
          <p class="text-sm" :style="{ color: 'var(--theme-border)' }">
            Nivel {{ level }} • {{ xp }} XP
          </p>
        </div>
      </div>

      <!-- Current streak -->
      <div class="text-right">
        <p class="text-sm" :style="{ color: 'var(--theme-border)' }">Mejor racha</p>
        <p class="text-2xl font-bold" :style="{ color: 'var(--theme-accent)' }">{{ longestStreak }} días</p>
      </div>
    </div>

    <!-- Barra de experiencia visual integrada -->
    <div class="flex flex-col w-full mb-4">
      <div class="flex items-center justify-between mb-1">
        <span class="font-bold text-lg" :style="{ color: 'var(--theme-border)' }">Nivel {{ level }}</span>
        <span class="font-semibold" :style="{ color: 'var(--theme-accent)' }">
          {{ title }}
        </span>
      </div>
      <div class="w-full rounded-full h-3 relative" :style="{ background: 'color-mix(in srgb, var(--theme-accent) 20%, transparent 80%)' }">
        <div class="h-3 rounded-full" :style="{ background: 'var(--theme-accent)', width: `${levelProgress}%` }"></div>
        <span class="absolute right-2 top-0 text-xs font-mono" :style="{ color: 'var(--theme-accent-contrast, #fff)' }">{{ xpProgress }} / {{ xpForNextLevel - xpForCurrentLevel }} XP</span>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-6 mt-6">
      <div>
        <p class="text-sm" :style="{ color: 'var(--theme-border)' }">Módulos Desbloqueados</p>
        <p class="text-2xl font-bold" :style="{ color: 'var(--theme-accent)' }">{{ stats.modules_unlocked }}</p>
      </div>
      <div>
        <p class="text-sm" :style="{ color: 'var(--theme-border)' }">Misiones Completadas</p>
        <p class="text-2xl font-bold" :style="{ color: 'var(--theme-accent)' }">{{ stats.missions_completed }}</p>
      </div>
      <div>
        <p class="text-sm" :style="{ color: 'var(--theme-border)' }">Logros Obtenidos</p>
        <p class="text-2xl font-bold" :style="{ color: 'var(--theme-accent)' }">{{ stats.achievements_earned }}</p>
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
  title: string
}

const props = defineProps<Props>()

// Computed values
const xpForCurrentLevel = computed(() => (props.level - 1) * 100)
const xpForNextLevel = computed(() => props.level * 100)
const xpProgress = computed(() => props.xp - xpForCurrentLevel.value)
const levelProgress = computed(() => 
  (xpProgress.value / (xpForNextLevel.value - xpForCurrentLevel.value)) * 100
)

// El título ahora viene del backend vía prop "title"

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
