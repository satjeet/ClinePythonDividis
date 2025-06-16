import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '../services/api';

export const useVitalRadarStore = defineStore('vitalRadar', () => {
  const values = ref<number[]>([80, 60, 70, 30, 40, 50, 20, 60]); // Mock inicial
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function fetchRadarValues() {
    loading.value = true;
    error.value = null;
    try {
      const res = await api.get('/api/wellness-survey/results/');
      // Espera un array de 8 promedios (0-100)
      values.value = res.data.values;
    } catch (e: any) {
      error.value = e.message || 'Error al cargar radar';
    } finally {
      loading.value = false;
    }
  }

  return {
    values,
    loading,
    error,
    fetchRadarValues
  };
});
