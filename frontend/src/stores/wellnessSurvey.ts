import { defineStore } from 'pinia';

interface Question {
  category: string;
  questions: string[];
}

interface Answers {
  [key: string]: number;
}

interface WellnessSurveyState {
  questions: Question[];
  answers: Answers;
  currentStep: number;
  isCompleted: boolean;
  session: any;
}

export const useWellnessSurveyStore = defineStore('wellnessSurvey', {
  state: (): WellnessSurveyState => ({
    questions: [],
    answers: {},
    currentStep: 1,
    isCompleted: false,
    session: null,
  }),
  actions: {
    setQuestions(questions: Question[]) {
      this.questions = questions;
    },
    setAnswers(answers: Answers) {
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
