<template>
  <div class="declaration-list">
    <h2 class="text-cosmic-300 font-bold mb-2">Declaraciones para {{ pillar }}</h2>
    <ul>
      <li v-for="(declaration, index) in declarations" :key="declaration.id || index" class="text-slate-400">
        {{ declaration.text }}
      </li>
    </ul>
    <p v-if="declarations.length === 0" class="text-slate-500">No hay declaraciones para este pilar.</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useModulesStore } from '@/stores/modules';

const props = defineProps({
  pillar: {
    type: String,
    required: true
  },
  moduleId: {
    type: String,
    required: true
  }
});

const modulesStore = useModulesStore();

const declarations = computed(() => {
  // Filtrar por pilar y módulo
  return modulesStore.declarations.filter(
    d => d.pillar === props.pillar && d.module === props.moduleId
  );
});
</script>

<style scoped>
.declaration-list {
  /* Add styles here */
}
</style>
