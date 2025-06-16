<template>
  <div class="survey-summary-chart">
    <v-chart class="chart" :option="chartOption" autoresize />
  </div>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts';
import { computed } from 'vue';
const props = defineProps<{ averages: number[]; labels: string[] }>();
const chartOption = computed(() => ({
  backgroundColor: '#090f20',
  radar: {
    indicator: props.labels.map(label => ({ name: label, max: 10 })),
    radius: '70%',
    center: ['50%', '50%'],
    axisName: { color: '#fff', fontSize: 18 },
    axisLine: { lineStyle: { color: '#1e293b' } },
    splitLine: { lineStyle: { color: '#1e293b' } },
    splitArea: { areaStyle: { color: ['rgba(56,189,248,0.1)','rgba(56,189,248,0.05)'] } }
  },
  series: [{
    name: 'Resultados',
    type: 'radar',
    data: [{ value: props.averages, name: 'Resultados' }],
    areaStyle: { opacity: 0.5, color: '#38bdf8' },
    lineStyle: { color: '#38bdf8' }
  }]
}));
</script>

<style scoped>
.survey-summary-chart { width: 100%; max-width: 500px; margin: 0 auto; }
.chart { width: 100%; height: 300px; }
</style>
