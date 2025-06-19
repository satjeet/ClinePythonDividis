<template>
  <div class="survey-summary-chart">
    <v-chart class="chart" :option="chartOption" autoresize />
  </div>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts';
import { computed } from 'vue';

interface Props {
  averages: number[];
  labels: string[];
}

const props = defineProps<Props>();

const chartOption = computed(() => ({
  backgroundColor: '#090f20',
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(15, 23, 42, 0.9)',
    borderColor: '#38bdf8',
    textStyle: {
      color: '#fff',
      fontFamily: 'var(--theme-font)'
    },
    formatter: ({ name, value }: { name: string; value: number[] }) => {
      return `${name}: ${value[0]}/10`;
    }
  },
  radar: {
    indicator: props.labels.map(label => ({ 
      name: label, 
      max: 10,
      axisType: 'value' 
    })),
    radius: '65%',
    center: ['50%', '50%'],
    axisName: {
      color: '#fff',
      fontSize: 14,
      fontFamily: 'var(--theme-font)',
      backgroundColor: 'rgba(15, 23, 42, 0.6)',
      padding: [5, 8],
      borderRadius: 3,
      formatter: (name: string) => name
    },
    splitLine: {
      lineStyle: {
        color: '#1e293b'
      }
    },
    splitArea: {
      show: true,
      areaStyle: {
        color: [
          'rgba(56,189,248,0.02)',
          'rgba(56,189,248,0.05)'
        ]
      }
    },
    axisLine: {
      lineStyle: {
        color: '#1e293b'
      }
    }
  },
  series: [{
    name: 'Resultados',
    type: 'radar',
    symbol: 'circle',
    symbolSize: 8,
    data: [{
      value: props.averages,
      name: 'Resultados',
      itemStyle: {
        color: '#38bdf8',
        borderColor: '#fff',
        borderWidth: 2
      },
      lineStyle: {
        width: 3,
        color: '#38bdf8'
      },
      areaStyle: {
        opacity: 0.4,
        color: '#38bdf8'
      }
    }]
  }]
}));
</script>

<style scoped>
.survey-summary-chart {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
}
.chart {
  width: 100%;
  height: 400px;
}
</style>
