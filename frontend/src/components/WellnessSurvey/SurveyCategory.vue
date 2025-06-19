<template>
  <!-- Componente para mostrar preguntas de una categoría -->
  <div class="survey-category bg-cosmic-800 p-6 rounded-lg">
    <h2 class="text-2xl font-bold mb-6 text-cosmic-100 text-center">{{ category.category }}</h2>
    <div v-for="(question, idx) in category.questions" :key="idx" class="mb-8">
      <label class="block mb-3 text-lg text-cosmic-200">{{ question }}</label>
      <div class="flex items-center gap-4">
        <input
          type="range"
          min="0"
          max="10"
          :value="answers[category.category + ':' + question] ?? 5"
          @input="onInput($event, question)"
          class="flex-grow h-2 rounded-lg appearance-none bg-cosmic-700 accent-cosmic-400"
          aria-valuemin="0"
          aria-valuemax="10"
          :aria-valuenow="answers[category.category + ':' + question] ?? 5"
          :aria-label="question"
        />
        <div class="text-xl font-semibold text-cosmic-300 w-8 text-center">
          {{ answers[category.category + ':' + question] ?? 5 }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';
const props = defineProps<{ category: any; answers: Record<string, number> }>();
const emit = defineEmits(['update-answer']);

function onInput(event: Event, question: string) {
  const value = Number((event.target as HTMLInputElement).value);
  emit('update-answer', {
    category: props.category.category,
    question,
    value
  });
}
</script>

<style scoped>
.survey-category {
  margin-bottom: 2rem;
}
input[type='range'] {
  cursor: pointer;
}
input[type='range']::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  background: #38bdf8;
  border: 2px solid #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.1s;
}
input[type='range']::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}
input[type='range']::-webkit-slider-runnable-track {
  height: 8px;
  border-radius: 4px;
}
</style>
