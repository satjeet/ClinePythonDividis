<template>
  <div class="vital-radar-chart-root">
    <div class="flex flex-col items-center w-full">
      <h3 class="text-cosmic-300 font-bold mb-2">Mapa de Progreso Vital</h3>
      <v-chart class="chart" :option="chartOption" autoresize />
      <WellnessSurveyButton @click="goToSurvey" class="mt-4" />
    </div>
  </div>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts';
import { useChartOptions } from '@/components/dashboard/VitalRadarChart/VitalRadarChart.ts';
import WellnessSurveyButton from './WellnessSurveyButton.vue';
import { useRouter } from 'vue-router';
import { useVitalRadarStore } from '@/stores/vitalRadar';
import { onMounted } from 'vue';
const router = useRouter();
const vitalRadar = useVitalRadarStore();
function goToSurvey() {
  router.push({ name: 'WellnessSurvey' });
}
onMounted(() => {
  vitalRadar.fetchRadarValues();
});
const chartOption = useChartOptions({ values: vitalRadar.values }).chartOption;
</script>
