<template>
  <!-- Vista principal de la encuesta de bienestar -->
  <div class="wellness-survey-container bg-cosmic-900 text-cosmic-100">
    <div v-if="error" class="bg-red-500/20 text-red-200 p-4 rounded-lg mb-6">
      {{ error }}
    </div>

    <SurveyProgressBar :currentStep="currentStep" :totalSteps="totalSteps" />
    
    <div v-if="isLoading" class="text-center p-4">
      <div class="text-cosmic-400">Cargando...</div>
    </div>
    
    <SurveyCategory
      v-else-if="questions.length > 0 && !isCompleted"
      :category="questions[currentStep - 1]"
      :answers="answers"
      @update-answer="updateAnswer"
    />

    <div class="survey-navigation" v-if="!isCompleted">
      <button 
        @click="prevStep" 
        :disabled="currentStep === 1"
        class="px-4 py-2 bg-cosmic-600 text-cosmic-100 rounded hover:bg-cosmic-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Anterior
      </button>
      <button 
        v-if="currentStep < totalSteps" 
        @click="nextStep"
        class="px-4 py-2 bg-cosmic-500 text-cosmic-100 rounded hover:bg-cosmic-400 transition-colors"
      >
        Siguiente
      </button>
      <button 
        v-if="currentStep === totalSteps" 
        @click="finishSurvey"
        :disabled="saving || !hasAnsweredAllQuestions"
        class="px-4 py-2 bg-sky-500 text-white rounded hover:bg-sky-400 transition-colors disabled:opacity-50"
      >
        Ver Resultados
      </button>
    </div>

    <div v-if="isCompleted" ref="resultsSection" class="mt-8">
      <h2 class="text-2xl font-bold mb-6 text-cosmic-100 text-center">Resumen de la Encuesta</h2>
      <SurveySummary :answers="answers" :questions="questions" />
      <h3 class="text-xl font-bold mt-8 mb-4 text-cosmic-100">Detalle de Respuestas</h3>
      <div class="overflow-x-auto mb-8">
        <table class="min-w-full border border-cosmic-700 text-sm bg-cosmic-800 rounded shadow text-cosmic-100">
          <thead>
            <tr>
              <th class="px-4 py-2 border-b border-cosmic-700 bg-cosmic-700 text-left">Área</th>
              <th class="px-4 py-2 border-b border-cosmic-700 bg-cosmic-700 text-left">Pregunta</th>
              <th class="px-4 py-2 border-b border-cosmic-700 bg-cosmic-700 text-left">Respuesta</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="category in Object.keys(answersByCategory)" :key="category">
              <tr v-for="answer in answersByCategory[category]" :key="`${category}-${answer.question}`">
                <td class="px-4 py-2 border-b border-cosmic-700">{{ answer.category }}</td>
                <td class="px-4 py-2 border-b border-cosmic-700">{{ answer.question }}</td>
                <td class="px-4 py-2 border-b border-cosmic-700">{{ answer.answer }}/10</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
      <div class="flex flex-col items-center gap-4">
        <button 
          class="bg-cosmic-500 text-cosmic-100 px-6 py-3 rounded-lg text-lg font-semibold hover:bg-cosmic-400 transition-colors disabled:opacity-50" 
          @click="saveAndExit" 
          :disabled="saving"
        >
          {{ saving ? 'Guardando...' : 'Guardar y Volver al Dashboard' }}
        </button>
        <p class="text-sm text-cosmic-400">
          Tus respuestas se usarán para actualizar tu gráfico de progreso vital
        </p>
      </div>
    </div>

    <transition name="fade">
      <div v-if="showToast" class="fixed top-8 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded shadow-lg z-50">
        {{ toastMessage }}
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

const store = useWellnessSurveyStore();
const router = useRouter();
const currentStep = computed(() => store.currentStep);
const totalSteps = computed(() => store.totalSteps);
const questions = computed(() => store.questions);
const answers = computed(() => store.answers);
const answersByCategory = computed(() => store.answersByCategory);
const isCompleted = computed(() => store.isCompleted);
const hasAnsweredAllQuestions = computed(() => store.hasAnsweredAllQuestions);
const showToast = ref(false);
const saving = ref(false);
const isLoading = ref(false);
const error = ref<string | null>(null);
const toastMessage = ref('');
const resultsSection = ref<HTMLElement | null>(null);

onMounted(async () => {
  try {
    isLoading.value = true;
    const q = await getSurveyQuestions();
    store.setQuestions(q);
  } catch (err) {
    error.value = 'Error al cargar las preguntas. Por favor, intenta más tarde.';
  } finally {
    isLoading.value = false;
  }
});

function updateAnswer({ category, question, value }: { category: string; question: string; value: number }) {
  try {
    store.setAnswer(category, question, value);
  } catch (err: any) {
    error.value = err.message;
  }
}

function nextStep() {
  store.setCurrentStep(store.currentStep + 1);
}

function prevStep() {
  store.setCurrentStep(store.currentStep - 1);
}

async function saveAndExit() {
  saving.value = true;
  error.value = null;
  toastMessage.value = 'Guardando respuestas...';
  showToast.value = true;
  
  try {
    await saveSurveyAnswers(answers.value);
    toastMessage.value = 'Respuestas guardadas correctamente';
    setTimeout(() => {
      showToast.value = false;
      router.push('/dashboard');
    }, 2000);
  } catch (err: any) {
    error.value = err.message || 'Error al guardar las respuestas';
    showToast.value = false;
  } finally {
    saving.value = false;
  }
}

async function finishSurvey() {
  if (!hasAnsweredAllQuestions.value) {
    error.value = 'Por favor responde todas las preguntas antes de continuar';
    return;
  }

  saving.value = true;
  error.value = null;

  try {
    await saveSurveyAnswers(answers.value);
    store.setCompleted(true);
    // Actualizar radar chart global tras finalizar
    const { useVitalRadarStore } = await import('@/stores/vitalRadar');
    const vitalRadarStore = useVitalRadarStore();
    await vitalRadarStore.fetchRadarValues();
    await nextTick();
    // Scroll al módulo de resultados
    if (resultsSection.value) {
      resultsSection.value.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  } catch (err: any) {
    error.value = err.message || 'Error al finalizar la encuesta';
    store.setCompleted(false);
  } finally {
    saving.value = false;
  }
}
</script>

<style scoped>
.wellness-survey-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
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
