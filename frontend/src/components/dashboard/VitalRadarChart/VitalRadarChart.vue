<template>
  <Card variant="interactive" class="w-full max-w-2xl mx-auto">
    <template #header>
      <h3 class="text-lg font-bold text-cosmic-300 text-center">Mapa de Progreso Vital</h3>
    </template>
<div class="flex flex-col items-center w-full">
<v-chart class="w-full aspect-square mb-6" :option="chartOption" autoresize />
      <Button class="w-full max-w-xs mt-4" @click="goToWellnessSurvey">
        Responder encuesta de bienestar
      </Button>
    </div>
  </Card>
</template>

<script setup lang="ts">
import VChart from 'vue-echarts';
import { useChartOptions } from './VitalRadarChart.ts';
import Card from '@/components/ui/Card.vue';
import Button from '@/components/ui/Button.vue';
import { useRouter } from 'vue-router';

const props = defineProps<{ values?: number[] }>();
const { chartOption } = useChartOptions(props);

const router = useRouter();
function goToWellnessSurvey() {
  router.push('/wellness-survey');
}
</script>
