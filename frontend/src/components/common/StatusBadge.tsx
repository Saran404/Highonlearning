import { CheckCircle2, CircleDot, Lock, PlayCircle } from 'lucide-react';
import type { AssessmentItem, LockStatus } from '../../types';

const styles: Record<LockStatus, { cls: string; label: string; icon: JSX.Element }> = {
  COMPLETED: { cls: 'bg-mint text-mint-700', label: 'Completed', icon: <CheckCircle2 className="h-3.5 w-3.5" /> },
  AVAILABLE: { cls: 'bg-sky-100 text-sky-800', label: 'Available', icon: <PlayCircle className="h-3.5 w-3.5" /> },
  IN_PROGRESS: { cls: 'bg-cream text-cream-700', label: 'In progress', icon: <CircleDot className="h-3.5 w-3.5" /> },
  LOCKED: { cls: 'bg-navy-100 text-navy-500', label: 'Locked', icon: <Lock className="h-3.5 w-3.5" /> },
};

export default function StatusBadge({ item }: { item: Pick<AssessmentItem, 'lock_status' | 'attempt_type'> }) {
  if (item.attempt_type === 'PRACTICE') {
    return <span className="inline-flex items-center gap-1 rounded-full bg-navy-50 px-2.5 py-1 text-xs font-medium text-navy-600">Practice</span>;
  }
  const s = styles[item.lock_status];
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium ${s.cls}`}>
      {s.icon}
      {s.label}
    </span>
  );
}
