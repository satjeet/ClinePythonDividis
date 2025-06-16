<template>
  <!-- Componente para mostrar preguntas de una categoría -->
  <div class="survey-category">
    <h2 class="text-xl font-bold mb-4">{{ category.category }}</h2>
    <div v-for="(question, idx) in category.questions" :key="idx" class="mb-6">
      <label class="block mb-2 font-medium">{{ question }}</label>
      <input
        type="range"
        min="0"
        max="10"
        :value="answers[category.category + ':' + question] ?? 5"
        @input="onInput($event, question)"
        class="w-full accent-sky-400"
        aria-valuemin="0"
        aria-valuemax="10"
        :aria-valuenow="answers[category.category + ':' + question] ?? 5"
        :aria-label="question"
      />
      <div class="text-sm text-cosmic-400 mt-1">{{ answers[category.category + ':' + question] ?? 5 }}</div>
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
  padding: 1rem 0;
}
input[type='range'] {
  width: 100%;
}
</style>
