import type { AssessmentItem } from '../types';
import { api } from './client';

export const assessmentsApi = {
  get: (id: number) => api.get<AssessmentItem>(`/assessments/${id}`).then((r) => r.data),
};
