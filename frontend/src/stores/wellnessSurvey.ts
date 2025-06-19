import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { SurveyAnswer } from '@/services/wellnessSurveyApi';

export interface SurveyCategory {
  category: string;
  questions: string[];
}

export const useWellnessSurveyStore = defineStore('wellnessSurvey', () => {
  const currentStep = ref(1);
  const questions = ref<SurveyCategory[]>([]);
  const answers = ref<Record<string, number>>({});
  const isCompleted = ref(false);
  const error = ref<string | null>(null);
  const loading = ref(false);

  const totalSteps = computed(() => questions.value.length);
  const currentCategory = computed(() => 
    questions.value[currentStep.value - 1]?.category || ''
  );
  const progress = computed(() => 
    Math.round((currentStep.value / totalSteps.value) * 100)
  );

  // Convertir respuestas al formato esperado por el backend
  const formattedAnswers = computed((): SurveyAnswer[] => {
    return Object.entries(answers.value).map(([key, value]) => {
      const [category, question] = key.split(':');
      if (!category || !question) {
        throw new Error(`Formato de respuesta inválido: ${key}`);
      }
      return {
        category,
        question,
        answer: value
      };
    });
  });

  const hasAnsweredAllQuestions = computed(() => {
    const totalQuestions = questions.value.reduce(
      (acc, cat) => acc + cat.questions.length, 
      0
    );
    const answeredQuestions = Object.keys(answers.value).length;
    return answeredQuestions === totalQuestions;
  });

  const answersByCategory = computed(() => {
    const grouped: Record<string, SurveyAnswer[]> = {};
    for (const answer of formattedAnswers.value) {
      if (!grouped[answer.category]) {
        grouped[answer.category] = [];
      }
      grouped[answer.category].push(answer);
    }
    return grouped;
  });

  function setQuestions(newQuestions: SurveyCategory[]) {
    questions.value = newQuestions;
  }

  function setCurrentStep(step: number) {
    if (step >= 1 && step <= totalSteps.value) {
      currentStep.value = step;
    }
  }

  function setAnswer(category: string, question: string, value: number) {
    if (value < 0 || value > 10) {
      throw new Error('El valor debe estar entre 0 y 10');
    }
    answers.value = {
      ...answers.value,
      [`${category}:${question}`]: value
    };
  }

  function setCompleted(value: boolean) {
    isCompleted.value = value;
  }

  function setError(value: string | null) {
    error.value = value;
  }

  function reset() {
    currentStep.value = 1;
    answers.value = {};
    isCompleted.value = false;
    error.value = null;
    loading.value = false;
  }

  return {
    currentStep,
    questions,
    answers,
    formattedAnswers,
    answersByCategory,
    isCompleted,
    error,
    loading,
    totalSteps,
    currentCategory,
    progress,
    hasAnsweredAllQuestions,
    setQuestions,
    setCurrentStep,
    setAnswer,
    setCompleted,
    setError,
    reset
  };
});
