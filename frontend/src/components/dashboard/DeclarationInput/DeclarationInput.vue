<template>
  <div class="declaration-input w-full">
    <label for="pillar-select" class="block text-sm font-medium text-cosmic-200">Pilar</label>
    <select
      :value="localSelectedPillar"
      @change="onSelectPillar"
      id="pillar-select"
      class="mt-1 block w-full pl-3 pr-10 py-2 text-base bg-cosmic-800 border-cosmic-700 text-cosmic-200 focus:outline-none focus:ring-cosmic-500 focus:border-cosmic-500 sm:text-sm rounded-md"
    >
      <option
        v-for="pillar in unlockedPillars"
        :key="pillar"
        :value="pillar"
      >
        {{ pillarLabel(pillar) }}
      </option>
    </select>
    <textarea v-model="declarationText" rows="4" class="shadow-sm bg-cosmic-800 text-cosmic-200 focus:ring-cosmic-500 focus:border-cosmic-500 mt-1 block w-full sm:text-sm border-cosmic-700 rounded-md" placeholder="Escribe tu declaración"></textarea>
    <button @click="addDeclaration" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-cosmic-600 hover:bg-cosmic-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cosmic-500">Añadir Declaración</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useModulesStore } from '@/stores/modules';

const props = defineProps({
  unlockedPillars: {
    type: Array as () => string[],
    required: true
  },
  moduleId: {
    type: String,
    required: true
  },
  selectedPillar: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['declaration-added', 'update:selectedPillar']);

const modulesStore = useModulesStore();
const localSelectedPillar = ref(props.selectedPillar);
const declarationText = ref('');

// Sincronizar localSelectedPillar con el prop
import { watch } from 'vue';
watch(
  () => props.selectedPillar,
  (val) => {
    localSelectedPillar.value = val;
  }
);

// Emitir update:selectedPillar cuando el usuario cambia el select
function onSelectPillar(e: Event) {
  emit('update:selectedPillar', (e.target as HTMLSelectElement).value);
}

// Etiqueta visible para el select
function pillarLabel(pillar: string) {
  switch (pillar) {
    case 'Vision': return 'Visión';
    case 'Proposito': return 'Propósito';
    case 'Creencias': return 'Creencias';
    case 'Estrategias': return 'Estrategias';
    default: return pillar;
  }
}

const addDeclaration = async () => {
  if (declarationText.value && localSelectedPillar.value) {
    modulesStore.addDeclaration(localSelectedPillar.value, declarationText.value, props.moduleId);
    await modulesStore.syncDeclarations();
    emit('declaration-added', { pillar: localSelectedPillar.value, text: declarationText.value });
    declarationText.value = '';
  }
};
</script>

<style scoped>
.declaration-input {
  /* Add styles here */
}
</style>
