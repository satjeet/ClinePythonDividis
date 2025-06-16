<template>
  <!-- Resumen visual de resultados -->
  <div class="survey-summary">
    <h2 class="text-xl font-bold mb-4">¡Encuesta completada!</h2>
    <SurveySummaryChart :averages="categoryAverages" :labels="categoryLabels" />
    <div class="mt-6">
      <button class="bg-sky-500 text-white px-4 py-2 rounded" @click="$emit('close')">Cerrar</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import SurveySummaryChart from './SurveySummaryChart.vue';
const props = defineProps<{ answers: Record<string, number>; questions: any[] }>();

const categoryLabels = computed(() => props.questions.map(q => q.category));
const categoryAverages = computed(() => {
  return props.questions.map(cat => {
    const values = cat.questions.map((q: string) => props.answers[cat.category + ':' + q]).filter((v: number) => typeof v === 'number');
    if (!values.length) return 0;
    return Number((values.reduce((a: number, b: number) => a + b, 0) / values.length).toFixed(2));
  });
});
</script>

<style scoped>
.survey-summary { text-align: center; padding: 2rem 0; }
</style>
