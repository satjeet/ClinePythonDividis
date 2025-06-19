import axios from 'axios';

export interface SurveyAnswer {
  category: string;
  question: string;
  answer: number;
}

export interface SurveyResult {
  categories: {
    category: string;
    average: number;
    answers: SurveyAnswer[];
  }[];
  values: number[];
}

export const getSurveyQuestions = async () => {
  try {
    const res = await axios.get('/api/wellness-survey/questions/');
    return res.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Error al cargar las preguntas');
  }
};

export const getSurveyAnswers = async (): Promise<SurveyResult> => {
  try {
    const res = await axios.get('/api/wellness-survey/answers/');
    return res.data;
  } catch (error: any) {
    console.error('Error fetching survey answers:', error);
    throw new Error(error.response?.data?.error || 'Error al cargar las respuestas');
  }
};

export const saveSurveyAnswers = async (answers: SurveyAnswer[] | Record<string, number>) => {
  try {
    // Si recibimos un Record<string, number>, convertirlo a SurveyAnswer[]
    const formattedAnswers = Array.isArray(answers)
      ? answers
      : Object.entries(answers).map(([key, value]) => {
          const [category, question] = key.split(':');
          if (!category || !question) {
            throw new Error('Formato de respuesta inválido');
          }
          return {
            category,
            question,
            answer: value
          };
        });

    // Validar que haya respuestas
    if (formattedAnswers.length === 0) {
      throw new Error('No hay respuestas para guardar');
    }

    // Guardar respuestas
    const res = await axios.post('/api/wellness-survey/answers/', formattedAnswers);

    // Verificar respuesta exitosa
    if (res.status === 201 && res.data.status === 'success') {
      // Devolver valores actualizados para el radar chart
      return {
        success: true,
        data: {
          values: res.data.values
        },
        message: res.data.message
      };
    } else {
      throw new Error(res.data.error || 'Error al guardar las respuestas');
    }
  } catch (error: any) {
    console.error('Error saving survey answers:', error);
    throw new Error(
      error.response?.data?.error || 
      error.message || 
      'Error al guardar las respuestas'
    );
  }
};

export const getSurveySession = async () => {
  try {
    const res = await axios.get('/api/wellness-survey/session/');
    return res.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Error al obtener la sesión');
  }
};

export const updateSurveySession = async (data: any) => {
  try {
    const res = await axios.put('/api/wellness-survey/session/', data);
    return res.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'Error al actualizar la sesión');
  }
};
