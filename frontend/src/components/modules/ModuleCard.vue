<template>
  <Card 
    variant="interactive"
    :locked="module.state === 'locked'"
    :loading="loading"
    class="h-full"
    :lockedMessage="`Requiere ${module.xp_required} XP`">
    <template #header>
      <div class="flex items-start justify-between">
        <div>
          <h3 class="text-lg font-medium text-cosmic-300">{{ module.name }}</h3>
          <p class="text-sm text-slate-400">{{ module.description }}</p>
        </div>
        <div class="flex-shrink-0">
          <!-- Module icon -->
          <div :class="[
            'w-10 h-10 rounded-lg flex items-center justify-center',
            module.state === 'locked' ? 'bg-slate-800 text-slate-500' : 'bg-cosmic-500/20 text-cosmic-400'
          ]">
            <i :class="module.icon"></i>
          </div>
        </div>
      </div>
    </template>

    <!-- Module content -->
    <div class="space-y-4">
      <!-- Progress stats -->
      <div v-if="progress" class="grid grid-cols-2 gap-4">
        <div>
          <p class="text-sm text-slate-400">XP Ganado</p>
          <p class="text-2xl font-bold text-cosmic-400">
            {{ progress.experience_points }}
          </p>
        </div>
        <div>
          <p class="text-sm text-slate-400">Racha</p>
          <p class="text-2xl font-bold text-cosmic-400">
            {{ streak?.current_streak || 0 }} días
          </p>
        </div>
      </div>

      <!-- Missions count -->
      <div v-if="missions?.length">
        <p class="text-sm text-slate-400">
          {{ completedMissionsCount }}/{{ missions.length }} misiones completadas
        </p>
        <div class="w-full bg-slate-800 rounded-full h-2 mt-2">
          <div 
            class="bg-cosmic-500 h-2 rounded-full transition-all duration-500"
            :style="{
              width: `${(completedMissionsCount / missions.length) * 100}%`
            }">
          </div>
        </div>
      </div>
    </div>

    <!-- Module actions -->
    <template #footer>
      <div class="flex justify-end">
        <Button 
          v-if="module.state === 'locked'"
          :disabled="userXP < module.xp_required"
          @click="$emit('unlock', module.id)">
          Desbloquear
        </Button>
        <Button 
          v-else
          @click="$emit('select', module.id)">
          {{ module.state === 'completed' ? 'Revisar' : 'Continuar' }}
        </Button>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import type { Module, ModuleProgress, Mission, Streak } from '@/types'
import Card from '@/components/ui/Card.vue'
import Button from '@/components/ui/Button.vue'
import { computed } from 'vue'

interface Props {
  module: Module
  progress?: ModuleProgress
  missions?: Mission[]
  streak?: Partial<Streak>
  userXP?: number
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  progress: undefined,
  missions: undefined,
  streak: undefined,
  userXP: 0,
  loading: false
})

const completedMissionsCount = computed(() => 
  props.missions?.filter(m => m.state === 'completed').length || 0
)

defineEmits<{
  (e: 'unlock', moduleId: string): void
  (e: 'select', moduleId: string): void
}>()
</script>
