<template>
  <!-- Vista principal de la encuesta de bienestar -->
  <div class="wellness-survey-container">
    <SurveyProgressBar :currentStep="currentStep" :totalSteps="totalSteps" />
    <SurveyCategory
      v-if="questions.length > 0"
      :category="questions[currentStep - 1]"
      :answers="answers"
      @update-answer="updateAnswer"
    />
    <div class="survey-navigation">
      <button @click="prevStep" :disabled="currentStep === 1">Anterior</button>
      <button v-if="currentStep < totalSteps" @click="nextStep">Siguiente</button>
      <button v-if="currentStep === totalSteps" @click="finishSurvey">Finalizar</button>
      <button @click="saveAndExit">Guardar y salir</button>
    </div>
    <SurveySummary v-if="isCompleted" :answers="answers" :questions="questions" />
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useWellnessSurveyStore } from '@/stores/wellnessSurvey';
import SurveyCategory from './SurveyCategory.vue';
import SurveyProgressBar from './SurveyProgressBar.vue';
import SurveySummary from './SurveySummary.vue';
import { getSurveyQuestions, getSurveyAnswers, saveSurveyAnswers } from '@/services/wellnessSurveyApi';

const store = useWellnessSurveyStore();
const currentStep = computed(() => store.currentStep);
const totalSteps = computed(() => store.questions.length);
const questions = computed(() => store.questions);
const answers = computed(() => store.answers);
const isCompleted = computed(() => store.isCompleted);

onMounted(async () => {
  const q = await getSurveyQuestions();
  store.setQuestions(q);
  // Opcional: cargar respuestas previas
  // const a = await getSurveyAnswers();
  // store.setAnswers(a);
});

function updateAnswer({ category, question, value }: { category: string; question: string; value: number }) {
  store.answers[`${category}:${question}`] = value;
}
function nextStep() {
  if (store.currentStep < store.questions.length) store.setCurrentStep(store.currentStep + 1);
}
function prevStep() {
  if (store.currentStep > 1) store.setCurrentStep(store.currentStep - 1);
}
async function saveAndExit() {
  await saveSurveyAnswers(store.answers);
  // feedback al usuario
}
async function finishSurvey() {
  await saveSurveyAnswers(store.answers);
  store.setCompleted(true);
  // Actualizar radar chart global tras finalizar
  const { useVitalRadarStore } = await import('@/stores/vitalRadar');
  useVitalRadarStore().fetchRadarValues();
}
</script>

<style scoped>
.wellness-survey-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: #f8fafc;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.survey-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}
</style>
