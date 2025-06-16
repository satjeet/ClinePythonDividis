import axios from 'axios';

export const getSurveyQuestions = async () => {
  const res = await axios.get('/api/wellness-survey/questions/');
  return res.data;
};

export const getSurveyAnswers = async () => {
  const res = await axios.get('/api/wellness-survey/answers/');
  return res.data;
};

export const saveSurveyAnswers = async (answers: any) => {
  const res = await axios.post('/api/wellness-survey/answers/', answers);
  return res.data;
};

export const getSurveySession = async () => {
  const res = await axios.get('/api/wellness-survey/session/');
  return res.data;
};

export const updateSurveySession = async (data: any) => {
  const res = await axios.put('/api/wellness-survey/session/', data);
  return res.data;
};
