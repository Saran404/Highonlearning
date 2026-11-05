import type { TriggerType } from '../types';
import { api } from './client';

export const proctoringApi = {
  uploadSnapshot: (attemptId: number, trigger: TriggerType, image: Blob) => {
    const form = new FormData();
    form.append('attempt_id', String(attemptId));
    form.append('trigger_type', trigger);
    form.append('image', image, 'snapshot.jpg');
    return api.post<{ snapshot_id: number; captured_at: string }>('/proctoring/snapshot', form).then((r) => r.data);
  },
};
