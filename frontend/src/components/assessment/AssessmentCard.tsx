import { Clock, Lock, ListChecks, Target, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import type { AssessmentItem } from '../../types';
import { assessmentAction } from '../../utils/assessmentAction';
import { formatMarks, formatRank } from '../../utils/format';
import Button from '../common/Button';
import StatusBadge from '../common/StatusBadge';

const difficultyTone: Record<string, string> = { EASY: 'text-mint-700', MEDIUM: 'text-cream-700', HARD: 'text-danger-700' };

interface Props {
  item: AssessmentItem;
  /** title of the test that must be finished first (shown on locked cards) */
  previousTitle?: string;
  language?: 'en' | 'ta';
}

export default function AssessmentCard({ item, previousTitle, language = 'en' }: Props) {
  const action = assessmentAction(item);
  const locked = item.lock_status === 'LOCKED' && item.attempt_type === 'GRADED';
  const displayTitle = language === 'ta'
    ? (item.title_ta || (item.attempt_type === 'PRACTICE' ? 'சதவீதம் - பயிற்சித் தொகுப்பு' : 'சதவீதம் - மதிப்பீட்டுத் தேர்வு'))
    : item.title;
  const displayDesc = language === 'ta' && item.description_ta ? item.description_ta : item.description;

  return (
    <div className={`panel flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between ${locked ? 'bg-navy-50/60' : ''}`}>
      <div className="min-w-0">
        <div className="flex flex-wrap items-center gap-2">
          <h3 className="text-base">{displayTitle}</h3>
          <StatusBadge item={item} />
          {item.difficulty && <span className={`text-xs font-medium ${difficultyTone[item.difficulty]}`}>{item.difficulty.toLowerCase()}</span>}
        </div>
        {displayDesc && <p className="mt-1 line-clamp-2 text-sm text-navy-500">{displayDesc}</p>}
        <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-navy-500">
          <span className="inline-flex items-center gap-1"><ListChecks className="h-3.5 w-3.5" />{item.total_questions} questions</span>
          {item.attempt_type === 'GRADED' ? (
            <>
              <span className="inline-flex items-center gap-1"><Clock className="h-3.5 w-3.5" />{item.min_duration_minutes}–{item.default_duration_minutes} min</span>
              <span className="inline-flex items-center gap-1"><Target className="h-3.5 w-3.5" />Pass {item.pass_percentage}%</span>
            </>
          ) : (
            <span>No timer · instant feedback</span>
          )}
          {item.lock_status === 'COMPLETED' && <span className="font-medium text-mint-700">{formatMarks(item.score, item.total)} · {formatRank(item.rank_position, item.total_participants)}</span>}
        </div>
        {locked && previousTitle && (
          <p className="mt-2 inline-flex items-center gap-1 text-xs text-navy-500"><Lock className="h-3.5 w-3.5" />Finish “{previousTitle}” to unlock this test.</p>
        )}
      </div>
      <div className="shrink-0 w-full sm:w-auto mt-2 sm:mt-0">
        {action.to ? (
          <Link to={action.to} className="block w-full sm:w-auto">
            <Button
              variant={action.variant}
              icon={action.variant === 'primary' ? <ArrowRight className="h-4 w-4" /> : undefined}
              fullWidth
            >
              {action.label}
            </Button>
          </Link>
        ) : (
          <Button variant="ghost" disabled fullWidth>{action.label}</Button>
        )}
      </div>
    </div>
  );
}
