import { defineStore } from 'pinia';

export const useWellnessSurveyStore = defineStore('wellnessSurvey', {
  state: () => ({
    questions: [],
    answers: {},
    currentStep: 1,
    isCompleted: false,
    session: null,
  }),
  actions: {
    setQuestions(questions: any[]) {
      this.questions = questions;
    },
    setAnswers(answers: Record<string, any>) {
      this.answers = answers;
    },
    setCurrentStep(step: number) {
      this.currentStep = step;
    },
    setSession(session: any) {
      this.session = session;
    },
    setCompleted(val: boolean) {
      this.isCompleted = val;
    },
    resetSurvey() {
      this.answers = {};
      this.currentStep = 1;
      this.isCompleted = false;
    }
  }
});
