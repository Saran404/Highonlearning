import type { LeaderboardResponse } from '../types';
import { api } from './client';

export const rankApi = {
  leaderboard: (assessmentId: number) =>
    api.get<LeaderboardResponse>(`/assessments/${assessmentId}/leaderboard`).then((r) => r.data),
};
