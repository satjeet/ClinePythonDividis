<template>
  <div class="constellation-nav-bar bg-cosmic-900 rounded-lg shadow px-4 py-2 flex items-center justify-between max-w-xl mx-auto mt-4">
    <div class="relative inline-block text-left">
      <button
        type="button"
        class="inline-flex items-center rounded-md border border-cosmic-700 shadow-sm px-4 py-2 bg-cosmic-800 text-cosmic-200 font-semibold hover:bg-cosmic-700 focus:outline-none focus:ring-2 focus:ring-cosmic-500 transition"
        id="menu-button"
        aria-expanded="true"
        aria-haspopup="true"
        @click="toggleMenu"
      >
        <i class="fas fa-rocket mr-2 text-cosmic-400"></i>
        {{ currentConstellation }}
        <svg class="ml-2 h-4 w-4 text-cosmic-300" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </button>
      <div
        v-if="menuOpen"
        class="origin-top-right absolute left-0 mt-2 w-48 rounded-md shadow-lg bg-cosmic-800 ring-1 ring-cosmic-700 ring-opacity-50 focus:outline-none z-50"
      >
        <div class="py-1">
          <template v-for="mod in modulesStore.modules" :key="mod.id">
            <router-link
              v-if="mod.state === 'unlocked' || mod.state === 'completed'"
              :to="`/constellation/${mod.id}`"
              class="block px-4 py-2 text-sm rounded transition text-cosmic-200 hover:bg-cosmic-700 hover:text-cosmic-100"
              @click="menuOpen = false"
            >
              {{ mod.name }}
            </router-link>
            <span
              v-else
              class="block px-4 py-2 text-sm rounded transition text-cosmic-500 cursor-not-allowed opacity-60 pointer-events-none"
            >
              {{ mod.name }}
            </span>
          </template>
        </div>
      </div>
    </div>
    <button
      v-if="hasPendingDeclarations"
      @click="saveDeclarations"
      class="ml-4 px-4 py-2 bg-cosmic-600 text-white rounded shadow hover:bg-cosmic-700 transition font-semibold"
    >
      <i class="fas fa-save mr-2"></i> Guardar
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useModulesStore } from '@/stores/modules';

const modulesStore = useModulesStore();
const route = useRoute();

const currentConstellation = computed(() => {
  // Busca el nombre del módulo activo según la ruta
  let area = route.params.area;
  if (Array.isArray(area)) area = area[0];
  if (!area) return 'Salud';
  const mod = modulesStore.modules.find(m => m.id === area);
  return mod ? mod.name : (typeof area === 'string' ? area.charAt(0).toUpperCase() + area.slice(1) : 'Salud');
});

// Si los módulos aún no están cargados, forzar la recarga al montar o al cambiar la ruta
onMounted(() => {
  if (!modulesStore.modules.length) {
    modulesStore.fetchModules();
  }
});

watch(
  () => route.params.area,
  () => {
    if (!modulesStore.modules.length) {
      modulesStore.fetchModules();
    }
  }
);

const menuOpen = ref(false);

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function handleClickOutside(event: MouseEvent) {
  const menu = document.getElementById('menu-button');
  if (menu && !menu.contains(event.target as Node)) {
    menuOpen.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});

const hasPendingDeclarations = computed(() => {
  return modulesStore.declarations.some(d => !d.synced);
});

const saveDeclarations = async () => {
  try {
    await modulesStore.syncDeclarations();
    alert('¡Declaraciones guardadas exitosamente en el backend!');
  } catch (err) {
    alert('Error al guardar declaraciones.');
  }
};
</script>

<style scoped>
.constellation-nav-bar {
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}
</style>
