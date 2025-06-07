<template>
  <div class="min-h-screen bg-slate-950">
    <AppNavbar sectionTitle="Constelación" />
    <ConstellationNavBar />
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-cosmic-900 rounded-lg shadow p-4 mb-8">
        <h1 class="text-cosmic-300 font-bold text-2xl mb-2">
          <i class="fas fa-star"></i> {{ constellationName }}
        </h1>
        <p class="text-slate-400">Explora y define tu camino en esta área vital.</p>
      </div>

      <div class="bg-cosmic-900 rounded-lg shadow p-4">
        <DeclarationInput :unlockedPillars="unlockedPillars" :module-id="moduleId" @declaration-added="handleDeclarationAdded" />
      </div>

      <div class="bg-cosmic-900 rounded-lg shadow p-4">
        <PillarTabs :pillars="unlockedPillars" @pillar-click="handlePillarClick" />
      </div>

      <div class="bg-cosmic-900 rounded-lg shadow p-4 mt-8">
        <DeclarationList :pillar="selectedPillar" :module-id="moduleId" />
      </div>

      <div class="bg-cosmic-900 rounded-lg shadow p-4 mt-8">
        <UnlockedTools />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import AppNavbar from '../components/ui/AppNavbar.vue';
import ConstellationNavBar from '../components/dashboard/ConstellationNavBar/ConstellationNavBar.vue';
import DeclarationInput from '../components/dashboard/DeclarationInput/DeclarationInput.vue';
import PillarTabs from '../components/dashboard/PillarTabs/PillarTabs.vue';
import DeclarationList from '../components/dashboard/DeclarationList/DeclarationList.vue';
import UnlockedTools from '../components/dashboard/UnlockedTools/UnlockedTools.vue';
import { unlockedPillarApi } from '@/services/api';

const route = useRoute();
const constellationName = route.params.area as string;

import { useModulesStore } from '@/stores/modules';
const moduleStore = useModulesStore();

const moduleId = computed(() => {
  // Busca el módulo cuyo nombre coincida con constellationName
  const mod = moduleStore.modules.find(m => m.name === constellationName);
  return mod ? mod.id : '';
});

// Pilar backend, para evitar "Purpose"
const allPillars = [
  { backend: 'Vision', label: 'Visión' },
  { backend: 'Proposito', label: 'Propósito' },
  { backend: 'Creencias', label: 'Creencias' },
  { backend: 'Estrategias', label: 'Estrategias' }
];

// Este array se llena con los valores backend desbloqueados desde el backend
const unlockedPillarsRaw = ref<string[]>(['Vision']);

// Este computed mantiene el orden correcto
const unlockedPillars = computed(() =>
  allPillars
    .filter(p => unlockedPillarsRaw.value.includes(p.backend))
    .map(p => p.backend)
);

const selectedPillar = ref('Vision');

const handlePillarClick = (pillar: string) => {
  selectedPillar.value = pillar;
};

const handleDeclarationAdded = async (declaration: { pillar: string; text: string }) => {
  selectedPillar.value = declaration.pillar;
  // Desbloquear el siguiente pilar si existe y no está desbloqueado aún
  const currentIndex = allPillars.findIndex(p => p.backend === declaration.pillar);
  if (currentIndex !== -1 && currentIndex < allPillars.length - 1) {
    const nextPillar = allPillars[currentIndex + 1].backend;
    if (!unlockedPillarsRaw.value.includes(nextPillar)) {
      unlockedPillarsRaw.value.push(nextPillar);
      // Guardar desbloqueo en backend
      if (moduleId.value) {
        try {
          await unlockedPillarApi.create({ module: moduleId.value, pillar: nextPillar });
        } catch (e) {
          // Si ya existe, ignorar error
        }
      }
    }
  }
};

// Cargar declaraciones y pilares desbloqueados al montar la vista
const loadData = async () => {
  await moduleStore.fetchDeclarations();
  // Cargar pilares desbloqueados desde backend
  if (moduleId.value) {
    try {
      const res = await unlockedPillarApi.getAll({ module: moduleId.value });
      const unlocked = res.data.map((p: any) => p.pillar);
      // Siempre desbloquear Vision por defecto
      unlockedPillarsRaw.value = Array.from(new Set(['Vision', ...unlocked]));
    } catch (e) {
      unlockedPillarsRaw.value = ['Vision'];
    }
  } else {
    unlockedPillarsRaw.value = ['Vision'];
  }
};

onMounted(loadData);

// Si cambia el módulo (área), recargar declaraciones y pilares
watch(moduleId, () => {
  loadData();
});
</script>

<style scoped>
/* Add styles here */
</style>
