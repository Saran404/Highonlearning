import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Dumbbell, Lock, ArrowRight, Loader2 } from 'lucide-react';
import { coursesApi } from '../../api/courses';
import type { AssessmentItem } from '../../types';
import BottomSheet from '../common/BottomSheet';
import Button from '../common/Button';

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function PracticeBottomSheet({ open, onClose }: Props) {
  const [practiceSets, setPracticeSets] = useState<AssessmentItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open) return;
    setLoading(true);
    coursesApi
      .dashboard()
      .then((d) => {
        const p = d.assessments.filter((a) => a.attempt_type === 'PRACTICE');
        setPracticeSets(p);
      })
      .catch(() => setPracticeSets([]))
      .finally(() => setLoading(false));
  }, [open]);

  return (
    <BottomSheet
      open={open}
      onClose={onClose}
      title={
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sky-100 text-sky-700">
            <Dumbbell className="h-4 w-4" />
          </div>
          <span>Practice Sets</span>
        </div>
      }
    >
      <p className="mb-4 text-xs text-navy-500">
        Reinforce concepts with untimed questions and detailed instant explanations.
      </p>

      {loading ? (
        <div className="flex h-36 items-center justify-center text-sky-600">
          <Loader2 className="h-6 w-6 animate-spin" />
        </div>
      ) : practiceSets.length === 0 ? (
        <div className="py-8 text-center text-sm text-navy-400">
          No practice sets available right now.
        </div>
      ) : (
        <div className="space-y-2.5">
          {practiceSets.map((p) => {
            const isLocked = p.lock_status === 'LOCKED';
            return (
              <div
                key={p.id}
                className={`flex items-center justify-between gap-3 rounded-2xl border p-3.5 transition-all ${
                  isLocked
                    ? 'border-line bg-navy-50/40 opacity-70 select-none'
                    : 'border-line bg-white hover:border-sky-300 hover:shadow-xs active:bg-sky-50/40'
                }`}
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="truncate text-sm font-bold text-navy">
                      {p.title}
                    </span>
                    {isLocked && (
                      <span className="inline-flex items-center gap-1 rounded bg-navy-100 px-1.5 py-0.5 text-[10px] font-semibold text-navy-600">
                        <Lock className="h-3 w-3" /> Locked
                      </span>
                    )}
                  </div>
                  <div className="mt-0.5 text-xs text-navy-500">
                    {p.total_questions} questions · {isLocked ? 'Unlocks with course' : 'Untimed feedback'}
                  </div>
                </div>

                {isLocked ? (
                  <Button size="sm" variant="secondary" disabled className="cursor-not-allowed opacity-60">
                    Locked
                  </Button>
                ) : (
                  <Link to={`/practice/${p.id}`} onClick={onClose}>
                    <Button size="sm" variant="primary" icon={<ArrowRight className="h-4 w-4" />}>
                      Practise
                    </Button>
                  </Link>
                )}
              </div>
            );
          })}
        </div>
      )}
    </BottomSheet>
  );
}
