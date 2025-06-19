<template>
  <!-- Vista principal de la encuesta de bienestar -->
  <div class="wellness-survey-container">
    <SurveyProgressBar :currentStep="currentStep" :totalSteps="totalSteps" />
    <SurveyCategory
      v-if="questions.length > 0 && !isCompleted"
      :category="questions[currentStep - 1]"
      :answers="answers"
      @update-answer="updateAnswer"
    />
    <div class="survey-navigation" v-if="!isCompleted">
      <button @click="prevStep" :disabled="currentStep === 1">Anterior</button>
      <button v-if="currentStep < totalSteps" @click="nextStep">Siguiente</button>
      <button v-if="currentStep === totalSteps" @click="finishSurvey">Finalizar</button>
    </div>
    <div v-if="isCompleted" ref="resultsSection">
      <SurveySummary :answers="answers" :questions="questions" />
      <h3 class="text-lg font-bold mt-8 mb-2">Resultados en tabla</h3>
      <div class="overflow-x-auto mb-4">
        <table class="min-w-full border text-sm bg-white rounded shadow">
          <thead>
            <tr>
              <th class="px-2 py-1 border">Área</th>
              <th class="px-2 py-1 border">Pregunta</th>
              <th class="px-2 py-1 border">Respuesta</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cat in questions" :key="cat.category">
              <template v-for="q in cat.questions" :key="q">
                <tr>
                  <td class="px-2 py-1 border">{{ cat.category }}</td>
                  <td class="px-2 py-1 border">{{ q }}</td>
                  <td class="px-2 py-1 border">{{ answers[cat.category + ':' + q] ?? '-' }}</td>
                </tr>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
      <button class="bg-sky-500 text-white px-4 py-2 rounded" @click="saveAndExit" :disabled="saving">
        Guardar y salir
      </button>
    </div>
    <transition name="fade">
      <div v-if="showToast" class="fixed top-8 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded shadow-lg z-50">
        Resultados guardados exitosamente
      </div>
    </transition>
  </div>
</template>
<script setup lang="ts">
import { onMounted, computed, ref, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useWellnessSurveyStore } from '@/stores/wellnessSurvey';
import SurveyCategory from './SurveyCategory.vue';
import SurveyProgressBar from './SurveyProgressBar.vue';
import SurveySummary from './SurveySummary.vue';
import { getSurveyQuestions, saveSurveyAnswers } from '@/services/wellnessSurveyApi';

interface Answers {
  [key: string]: number;
}

const store = useWellnessSurveyStore();
const router = useRouter();
const currentStep = computed(() => store.currentStep);
const totalSteps = computed(() => store.questions.length);
const questions = computed(() => store.questions);
const answers = computed<Answers>(() => store.answers);
const isCompleted = computed(() => store.isCompleted);
const showToast = ref(false);
const saving = ref(false);
const resultsSection = ref<HTMLElement | null>(null);

onMounted(async () => {
  const q = await getSurveyQuestions();
  store.setQuestions(q);
});

function updateAnswer({ category, question, value }: { category: string; question: string; value: number }) {
  (store.answers as Answers)[`${category}:${question}`] = value;
}
function nextStep() {
  if (store.currentStep < store.questions.length) store.setCurrentStep(store.currentStep + 1);
}
function prevStep() {
  if (store.currentStep > 1) store.setCurrentStep(store.currentStep - 1);
}
async function saveAndExit() {
  saving.value = true;
  await saveSurveyAnswers(store.answers);
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
    router.push('/dashboard');
  }, 2000);
  saving.value = false;
}
async function finishSurvey() {
  await saveSurveyAnswers(store.answers);
  store.setCompleted(true);
  // Actualizar radar chart global tras finalizar
  const { useVitalRadarStore } = await import('@/stores/vitalRadar');
  useVitalRadarStore().fetchRadarValues();
  await nextTick();
  // Scroll al módulo de resultados
  if (resultsSection.value) {
    resultsSection.value.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
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
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
