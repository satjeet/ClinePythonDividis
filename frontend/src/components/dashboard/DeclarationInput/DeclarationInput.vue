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
import { ref, computed, watch } from 'vue';
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
  },
  // Nuevo: lista de módulos disponibles (con id y name)
  modulesList: {
    type: Array as () => { id: string, name: string }[],
    required: false,
    default: () => []
  }
});

const emit = defineEmits(['declaration-added', 'update:selectedPillar']);

const modulesStore = useModulesStore();
const localSelectedPillar = ref(props.selectedPillar);
const declarationText = ref('');

// Sincronizar localSelectedPillar con el prop
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

// Obtener el ID real del módulo (por si llega el nombre)
const moduleIdToUse = computed(() => {
  // Si el id ya es el formato correcto, úsalo
  if (props.moduleId && !props.moduleId.includes(' ')) return props.moduleId;
  // Si hay lista de módulos, buscar por nombre
  if (props.modulesList && props.modulesList.length > 0) {
    const found = props.modulesList.find(m => m.name === props.moduleId);
    if (found) return found.id;
  }
  // Fallback: reemplazar espacios por guiones y minúsculas
  return props.moduleId.replace(/\s+/g, '-').toLowerCase();
});

const addDeclaration = async () => {
  if (declarationText.value && localSelectedPillar.value) {
    modulesStore.addDeclaration(localSelectedPillar.value, declarationText.value, moduleIdToUse.value);
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
