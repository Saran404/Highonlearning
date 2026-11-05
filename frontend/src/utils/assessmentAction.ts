import type { AssessmentItem } from '../types';

export interface AssessmentAction {
  label: string;
  to: string | null;
  variant: 'primary' | 'secondary' | 'success' | 'ghost';
}

/** What the primary button on an assessment row/card does. */
export function assessmentAction(a: AssessmentItem): AssessmentAction {
  if (a.attempt_type === 'PRACTICE') return { label: 'Practice', to: `/practice/${a.id}`, variant: 'primary' };
  switch (a.lock_status) {
    case 'COMPLETED':
      return { label: 'View result', to: a.attempt_id ? `/results/${a.attempt_id}` : null, variant: 'primary' };
    case 'IN_PROGRESS':
      return { label: 'Resume', to: a.attempt_id ? `/attempts/${a.attempt_id}` : `/assessments/${a.id}`, variant: 'success' };
    case 'AVAILABLE':
      return { label: 'Start', to: `/assessments/${a.id}`, variant: 'primary' };
    default:
      return { label: 'Locked', to: null, variant: 'ghost' };
  }
}
