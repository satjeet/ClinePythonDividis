<template>
  <div class="vital-radar-chart-root">
    <div class="flex flex-col items-center w-full">
      <h3 class="text-cosmic-300 font-bold mb-2">Mapa de Progreso Vital</h3>
      <v-chart class="chart" :option="chartOption" autoresize />
    </div>
  </div>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts';
import { useChartOptions } from './VitalRadarChart.ts';
import './VitalRadarChart.css';

const props = defineProps<{ values?: number[] }>();
const { chartOption } = useChartOptions(props);
</script>
