<template>
  <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
    <div class="bg-slate-900 rounded-xl shadow-xl p-6 w-full max-w-md relative">
      <button class="absolute top-2 right-2 text-slate-400 hover:text-red-400" @click="$emit('close')">
        <i class="fas fa-times"></i>
      </button>
      <h3 class="text-xl font-bold text-cosmic-400 mb-4">Requisitos para activar misión</h3>
      <ul class="mb-4 space-y-2">
        <li v-for="req in requirements" :key="req.id" class="flex items-center gap-2">
          <i
            v-if="isRequirementMet(req)"
            class="fas fa-check-circle text-green-400"
          ></i>
          <i
            v-else
            class="fas fa-times-circle text-red-400"
          ></i>
          <span>
            <template v-if="req.type === 'module'">
              Desbloquea el módulo <b>{{ req.name }}</b>
            </template>
            <template v-else-if="req.type === 'mission'">
              Completa la misión <b>{{ req.name }}</b>
            </template>
          </span>
        </li>
      </ul>
      <button
        class="w-full py-2 rounded bg-cosmic-500 text-white font-semibold disabled:bg-slate-700"
        :disabled="!allRequirementsMet"
        @click="activate"
      >
        Activar misión
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useModulesStore } from '@/stores/modules'
import { useMissionsStore } from '@/stores/missions'

const props = defineProps<{
  mission: any
  requirements: any[]
  open: boolean
}>()

const emit = defineEmits(['close'])

const modulesStore = useModulesStore()
const missionsStore = useMissionsStore()

function isRequirementMet(req: any) {
  if (req.type === 'module') {
    const mod = modulesStore.modules.find((m) => m.id === req.id)
    return mod && mod.state === 'unlocked'
  }
  if (req.type === 'mission') {
    const prev = missionsStore.missions.find((m) => m.id === req.id)
    return prev && prev.state === 'completed'
  }
  return false
}

const allRequirementsMet = computed(() =>
  props.requirements.every(isRequirementMet)
)

function activate() {
  if (allRequirementsMet.value) {
    missionsStore.activateMission(props.mission)
    emit('close')
  }
}
</script>
