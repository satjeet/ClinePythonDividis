import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getSurveyAnswers } from '@/services/wellnessSurveyApi';

export const useVitalRadarStore = defineStore('vitalRadar', () => {
  const values = ref<number[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const initialized = ref(false);

  async function fetchRadarValues() {
    if (loading.value) return;

    loading.value = true;
    error.value = null;
    
    try {
      // Obtener los datos más recientes
      const surveyData = await getSurveyAnswers();
      values.value = surveyData.values;
      initialized.value = true;
      
      // Validar que tengamos todos los valores necesarios
      if (!Array.isArray(values.value) || values.value.length === 0) {
        throw new Error('No hay datos disponibles para el radar vital');
      }

    } catch (e: any) {
      console.error('Error al cargar datos del radar:', e);
      error.value = e.message;
      values.value = new Array(8).fill(0); // Valores por defecto
    } finally {
      loading.value = false;
    }
  }

  function updateValues(newValues: number[]) {
    if (Array.isArray(newValues) && newValues.length > 0) {
      values.value = newValues.map(v => parseFloat(v.toFixed(2)));
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
