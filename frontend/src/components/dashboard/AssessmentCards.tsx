import { Link } from 'react-router-dom';
import type { AssessmentItem } from '../../types';
import { assessmentAction } from '../../utils/assessmentAction';
import { formatDuration, formatMarks, formatPercent, formatRank } from '../../utils/format';
import StatusBadge from '../common/StatusBadge';

/** Mobile view: the same fields as the table, stacked. Tapping a card navigates. */
export default function AssessmentCards({ items }: { items: AssessmentItem[] }) {
  return (
    <ul className="space-y-3">
      {items.map((a) => {
        const action = assessmentAction(a);
        const body = (
          <div className={`panel p-4 ${action.to ? 'active:bg-navy-50' : 'opacity-70'}`}>
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <div className="truncate font-medium">{a.title}</div>
                <div className="truncate text-xs text-navy-400">{a.course_title}</div>
              </div>
              <StatusBadge item={a} />
            </div>
            <dl className="mt-3 grid grid-cols-4 gap-2 text-center text-xs">
              {[['Marks', formatMarks(a.score, a.total)], ['%', formatPercent(a.percentage)], ['Time', formatDuration(a.time_taken_sec)], ['Rank', formatRank(a.rank_position, a.total_participants)]].map(([k, v]) => (
                <div key={k} className="rounded-lg bg-canvas px-1 py-2">
                  <dd className="font-semibold tabular-nums">{v}</dd>
                  <dt className="text-navy-400">{k}</dt>
                </div>
              ))}
            </dl>
            <div className={`mt-3 text-right text-sm font-semibold ${action.to ? 'text-sky-700' : 'text-navy-400'}`}>{action.label}</div>
          </div>
        );
        return <li key={a.id}>{action.to ? <Link to={action.to} className="block">{body}</Link> : body}</li>;
      })}
    </ul>
  );
}
