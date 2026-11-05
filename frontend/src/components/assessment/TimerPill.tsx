import { Timer } from 'lucide-react';
import { formatTime } from '../../utils/format';

interface Props {
  remaining: number;
  low?: boolean;
  critical?: boolean;
}

/** Sits on the navy exam bar. Turns cream at 5 minutes and red at 1 minute. */
export default function TimerPill({ remaining, low, critical }: Props) {
  const tone = critical ? 'bg-danger text-danger-700' : low ? 'bg-cream text-cream-700' : 'bg-white/10 text-white';
  return (
    <div className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm font-semibold tabular-nums ${tone}`} role="timer" aria-live="off" aria-label={`Time left ${formatTime(remaining)}`}>
      <Timer className="h-4 w-4" aria-hidden />
      {formatTime(remaining)}
    </div>
  );
}
