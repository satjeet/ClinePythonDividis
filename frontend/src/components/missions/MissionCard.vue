<template>
  <Card 
    variant="interactive"
    :loading="loading"
    class="h-full mission-card"
    :class="{ 'mission-completed': mission.state === 'completed' }">
    <template #header>
      <div class="flex items-start justify-between">
        <div>
          <h3 class="text-lg font-medium text-cosmic-300">{{ mission.title }}</h3>
          <p class="text-sm text-slate-400">{{ mission.description }}</p>
        </div>
        <div class="flex-shrink-0">
          <!-- XP Reward -->
          <div class="bg-cosmic-500/20 text-cosmic-400 px-3 py-1 rounded-full text-sm">
            +{{ mission.xp_reward }} XP
          </div>
        </div>
      </div>
    </template>

    <!-- Mission content -->
    <div class="space-y-4">
      <!-- Requirements -->
      <div v-if="mission.required_level > 1" class="text-sm text-slate-400">
        <span class="font-medium">Nivel requerido:</span> {{ mission.required_level }}
      </div>

      <!-- Status -->
      <div class="flex items-center" v-if="mission.state">
        <template v-if="mission.state === 'completed'">
          <svg class="w-5 h-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span class="text-green-500">Completada</span>
        </template>
        <template v-else-if="mission.state === 'active'">
          <div class="w-2 h-2 rounded-full bg-cosmic-500 mr-2"></div>
          <span class="text-cosmic-400">En progreso</span>
        </template>
        <template v-else-if="mission.state === 'failed'">
          <svg class="w-5 h-5 text-red-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <span class="text-red-500">Fallida</span>
        </template>
      </div>
    </div>

    <!-- Mission actions -->
    <template #footer>
      <div class="flex justify-end">
        <Button 
          v-if="mission.state !== 'completed'"
          @click="$emit('complete', mission.id)"
          :disabled="
            loading || 
            userLevel < mission.required_level ||
            mission.state === 'failed'
          ">
          {{ mission.state === 'active' ? 'Completar' : 'Iniciar' }}
        </Button>
        <Button 
          v-else
          variant="ghost"
          @click="$emit('retry', mission.id)">
          Volver a intentar
        </Button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import type { Mission } from '@/types'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'

interface Props {
  mission: Mission
  userLevel: number
  loading?: boolean
}

withDefaults(defineProps<Props>(), {
  loading: false
})

defineEmits<{
  (e: 'complete', missionId: string): void
  (e: 'retry', missionId: string): void
}>()
</script>

<style scoped>
.mission-card {
  @apply transition-all duration-300 ease-in-out;
}

.mission-completed {
  @apply opacity-75 hover:opacity-100;
}

.mission-completed::before {
  content: '';
  @apply absolute inset-0 bg-green-500/10 pointer-events-none rounded-lg;
}
</style>
