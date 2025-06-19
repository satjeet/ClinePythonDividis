<template>
  <div class="vital-radar-chart-root">
    <div class="flex flex-col items-center w-full">
      <h3 class="text-cosmic-300 font-bold mb-2">Mapa de Progreso Vital</h3>
      <v-chart class="chart" :option="chartOption" autoresize />
      <!-- Botón para acceder a la encuesta de bienestar -->
      <button
        class="mt-6 px-6 py-2 bg-sky-500 text-white rounded shadow hover:bg-sky-600 transition-colors"
        @click="goToWellnessSurvey"
      >
        Responder encuesta de bienestar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts';
import { useChartOptions } from './VitalRadarChart.ts';
import './VitalRadarChart.css';
import { useRouter } from 'vue-router';

const props = defineProps<{ values?: number[] }>();
const { chartOption } = useChartOptions(props);

const router = useRouter();
function goToWellnessSurvey() {
  router.push('/wellness-survey');
}
</script>
