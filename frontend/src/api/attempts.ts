import type { AttemptState, MalpracticeType, ResultResponse } from '../types';
import { api } from './client';

export interface SubmitPayload {
  answers: { question_id: number; selected_index: number | null }[];
  time_taken_sec?: number;
  auto: boolean;
}

export const attemptsApi = {
  start: (body: {
    assessment_id: number;
    chosen_duration_minutes: number;
    acknowledgments: { no_minimize: boolean; consent_camera: boolean; single_attempt: boolean };
  }) => api.post<AttemptState>('/attempts/start', body).then((r) => r.data),
  get: (id: number) => api.get<AttemptState>(`/attempts/${id}`).then((r) => r.data),
  answer: (id: number, body: { question_id: number; selected_index: number | null; marked_for_review: boolean }) =>
    api.patch(`/attempts/${id}/answer`, body).then((r) => r.data),
  malpractice: (id: number, body: { type: MalpracticeType; metadata?: Record<string, unknown> }) =>
    api
      .post<{ malpractice_count: number; should_terminate: boolean; max_malpractice: number }>(`/attempts/${id}/malpractice`, body)
      .then((r) => r.data),
  extend: (id: number) => api.post<{ deadline_at: string; extended: boolean }>(`/attempts/${id}/extend`).then((r) => r.data),
  submit: (id: number, body: SubmitPayload) => api.post<ResultResponse>(`/attempts/${id}/submit`, body).then((r) => r.data),
  result: (id: number) => api.get<ResultResponse>(`/attempts/${id}/result`).then((r) => r.data),
};
