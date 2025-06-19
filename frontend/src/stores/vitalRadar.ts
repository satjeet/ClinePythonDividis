import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { getSurveyAnswers } from '@/services/wellnessSurveyApi';

export const useVitalRadarStore = defineStore('vitalRadar', () => {
  const rawValues = ref<number[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const initialized = ref(false);

  // Exponer valores multiplicados por 10 para el dashboard
  const values = computed(() => rawValues.value.map(v => Math.round(v * 10)));

  async function fetchRadarValues() {
    if (loading.value) return;

    loading.value = true;
    error.value = null;
    
    try {
      // Obtener los datos más recientes
      const surveyData = await getSurveyAnswers();
      rawValues.value = surveyData.values;
      initialized.value = true;
      
      // Validar que tengamos todos los valores necesarios
      if (!Array.isArray(rawValues.value) || rawValues.value.length === 0) {
        throw new Error('No hay datos disponibles para el radar vital');
      }

    } catch (e: any) {
      console.error('Error al cargar datos del radar:', e);
      error.value = e.message;
      rawValues.value = new Array(8).fill(0); // Valores por defecto
    } finally {
      loading.value = false;
    }
  }

  function updateValues(newValues: number[]) {
    if (Array.isArray(newValues) && newValues.length > 0) {
      rawValues.value = newValues.map(v => parseFloat(v.toFixed(2)));
    }
  }

  return {
    values,
    loading,
    error,
    initialized,
    fetchRadarValues,
    updateValues
  };
});
