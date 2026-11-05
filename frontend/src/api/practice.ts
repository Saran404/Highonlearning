import type { Question } from '../types';
import { api } from './client';

export interface PracticeFeedback {
  correct: boolean;
  correct_index: number;
  explanation: string;
  explanation_ta?: string | null;
  selected_index: number;
}

export const practiceApi = {
  questions: (assessmentId: number) => api.get<Question[]>(`/practice/${assessmentId}/questions`).then((r) => r.data),
  answer: (body: { question_id: number; selected_index: number }) =>
    api.post<PracticeFeedback>('/practice/answer', body).then((r) => r.data),
  reset: (assessmentId: number) => api.post(`/practice/reset/${assessmentId}`).then((r) => r.data),
};
