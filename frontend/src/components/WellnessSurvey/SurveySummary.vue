<template>
  <!-- Resumen visual de resultados -->
  <div class="survey-summary">
    <div class="mb-8 text-center">
      <div class="text-cosmic-400 text-sm mb-2">Tu progreso vital</div>
      <h2 class="text-2xl font-bold text-cosmic-100">Vista general de resultados</h2>
    </div>

    <!-- Gráfico radar -->
    <div class="bg-cosmic-800 p-6 rounded-lg mb-8">
      <SurveySummaryChart :averages="categoryAverages" :labels="categoryLabels" />
    </div>

    <!-- Resumen por categoría -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
      <div 
        v-for="(average, idx) in categoryAverages" 
        :key="categoryLabels[idx]"
        class="bg-cosmic-800 p-4 rounded-lg"
      >
        <div class="text-lg font-semibold text-cosmic-100">{{ categoryLabels[idx] }}</div>
        <div class="flex items-center mt-2">
          <div class="flex-grow bg-cosmic-700 h-2 rounded-full overflow-hidden">
            <div 
              class="h-full bg-cosmic-400 transition-all duration-500"
              :style="{ width: `${average * 10}%` }"
            ></div>
          </div>
          <div class="ml-3 text-cosmic-300 font-mono">{{ average }}/10</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import SurveySummaryChart from './SurveySummaryChart.vue';
import { type SurveyCategory } from '@/stores/wellnessSurvey';

interface Props {
  answers: Record<string, number>;
  questions: SurveyCategory[];
}

const props = defineProps<Props>();

const categoryLabels = computed(() => props.questions.map(cat => cat.category));

const categoryAverages = computed(() => {
  return props.questions.map(cat => {
    const values = cat.questions
      .map((question: string) => props.answers[`${cat.category}:${question}`])
      .filter((value: number | undefined): value is number => 
        typeof value === 'number' && !isNaN(value)
      );
    
    if (!values.length) return 0;
    
    const sum = values.reduce((acc: number, val: number) => acc + val, 0);
    return Number((sum / values.length).toFixed(2));
  });
});
</script>

<style scoped>
.survey-summary {
  position: relative;
}
</style>
