import { AlertTriangle, Clock, Medal, ShieldAlert } from 'lucide-react';
import type { ResultResponse } from '../../types';
import { formatDuration, formatRank } from '../../utils/format';
import ProgressRing from '../common/ProgressRing';

export default function ResultScoreCard({ attempt }: { attempt: ResultResponse['attempt'] }) {
  const tone = attempt.passed ? '#1f8a54' : '#2b7fc9';
  const correct = attempt.score;
  const wrongOrSkipped = attempt.total - attempt.score;
  return (
    <div className="panel p-5 sm:p-6">
      <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-center">
        <ProgressRing value={attempt.percentage} size={132} stroke={12} color={tone} label={`Scored ${attempt.percentage} percent`}>
          <span className="text-3xl font-semibold tabular-nums">{attempt.score}<span className="text-lg text-navy-400">/{attempt.total}</span></span>
          <span className="text-xs text-navy-500">{attempt.percentage}%</span>
        </ProgressRing>
        <div className="w-full flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <h1 className="text-xl">{attempt.assessment_title}</h1>
            <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${attempt.passed ? 'bg-mint text-mint-700' : 'bg-cream text-cream-700'}`}>
              {attempt.passed ? 'Passed' : `Below ${attempt.pass_percentage}% pass mark`}
            </span>
          </div>
          <dl className="mt-4 grid grid-cols-3 gap-3 text-sm">
            <div className="rounded-lg bg-canvas p-3">
              <dt className="flex items-center gap-1 text-xs text-navy-500"><Medal className="h-3.5 w-3.5" /> Rank</dt>
              <dd className="mt-0.5 font-semibold">{formatRank(attempt.rank_position, attempt.total_participants)}</dd>
            </div>
            <div className="rounded-lg bg-canvas p-3">
              <dt className="flex items-center gap-1 text-xs text-navy-500"><Clock className="h-3.5 w-3.5" /> Time</dt>
              <dd className="mt-0.5 font-semibold">{formatDuration(attempt.time_taken_sec)}</dd>
            </div>
            <div className="rounded-lg bg-canvas p-3">
              <dt className="flex items-center gap-1 text-xs text-navy-500"><ShieldAlert className="h-3.5 w-3.5" /> Warnings</dt>
              <dd className="mt-0.5 font-semibold">{attempt.malpractice_count}</dd>
            </div>
          </dl>
          <p className="mt-3 text-xs text-navy-500">{correct} correct · {wrongOrSkipped} wrong or skipped</p>
        </div>
      </div>
      {attempt.status === 'FLAGGED' && (
        <div className="mt-4 flex items-start gap-2 rounded-lg bg-danger px-3 py-2.5 text-sm text-danger-700">
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
          This attempt was submitted automatically after too many rule violations and is marked as flagged for review.
        </div>
      )}
      {attempt.status === 'AUTO_SUBMITTED' && (
        <p className="mt-4 rounded-lg bg-cream px-3 py-2.5 text-sm text-cream-700">Your time ran out, so the test was submitted with the answers you had saved.</p>
      )}
    </div>
  );
}
