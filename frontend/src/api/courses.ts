import type { AssessmentItem, Course, DashboardData, ReflectionAnswerItem, ReflectionResponse } from '../types';
import { api } from './client';

export const coursesApi = {
  list: () => api.get<Course[]>('/courses').then((r) => r.data),
  get: (slug: string) => api.get<Course>(`/courses/${slug}`).then((r) => r.data),
  assessments: (slug: string) => api.get<AssessmentItem[]>(`/courses/${slug}/assessments`).then((r) => r.data),
  dashboard: () => api.get<DashboardData>('/users/me/dashboard').then((r) => r.data),
  reflection: (slug: string) => api.get<ReflectionResponse>(`/courses/${slug}/reflection`).then((r) => r.data),
  submitReflection: (slug: string, answers: ReflectionAnswerItem[]) =>
    api.post<ReflectionResponse>(`/courses/${slug}/reflection`, { answers }).then((r) => r.data),
};
