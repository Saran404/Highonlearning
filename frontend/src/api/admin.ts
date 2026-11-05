import type { AdminUserReflectionSummary, AlertRow, AttemptDrilldownData, AttemptRow, LiveAttemptRow, Page, StudentRow } from '../types';
import { api } from './client';

export const adminApi = {
  students: (params: { search?: string; page?: number }) =>
    api.get<Page<StudentRow>>('/admin/students', { params }).then((r) => r.data),
  attempts: (params: { status?: string; assessment_id?: number; user_id?: number; page?: number }) =>
    api.get<Page<AttemptRow>>('/admin/attempts', { params }).then((r) => r.data),
  live: () => api.get<LiveAttemptRow[]>('/admin/attempts/live').then((r) => r.data),
  attempt: (id: number) => api.get<AttemptDrilldownData>(`/admin/attempts/${id}`).then((r) => r.data),
  forceSubmit: (id: number) => api.post<AttemptRow>(`/admin/attempts/${id}/force-submit`).then((r) => r.data),
  reset: (id: number) => api.post(`/admin/attempts/${id}/reset`).then((r) => r.data),
  alerts: () => api.get<AlertRow[]>('/admin/alerts').then((r) => r.data),
  revokeSession: (id: string) => api.post(`/admin/sessions/${id}/revoke`).then((r) => r.data),
  reflections: (search?: string) =>
    api.get<AdminUserReflectionSummary[]>('/admin/reflections', { params: { search: search || undefined } }).then((r) => r.data),
};
