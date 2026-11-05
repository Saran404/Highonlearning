import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import type { AssessmentItem } from '../../types';
import { assessmentAction } from '../../utils/assessmentAction';
import { formatDuration, formatMarks, formatPercent, formatRank } from '../../utils/format';
import Button from '../common/Button';
import StatusBadge from '../common/StatusBadge';

/** Desktop view: one row per assessment. */
export default function AssessmentTable({ items }: { items: AssessmentItem[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-line text-xs text-navy-500">
          <tr>
            {['Name', 'Status', 'Marks', '%', 'Time', 'Rank', ''].map((h) => (
              <th key={h} className="whitespace-nowrap px-4 py-3 font-medium">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-line">
          {items.map((a) => {
            const action = assessmentAction(a);
            return (
              <tr key={a.id} className="hover:bg-navy-50/50">
                <td className="px-4 py-3">
                  <div className="font-medium">{a.title}</div>
                  <div className="text-xs text-navy-400">{a.course_title}</div>
                </td>
                <td className="px-4 py-3"><StatusBadge item={a} /></td>
                <td className="px-4 py-3 tabular-nums">{formatMarks(a.score, a.total)}</td>
                <td className="px-4 py-3 tabular-nums">{formatPercent(a.percentage)}</td>
                <td className="px-4 py-3 tabular-nums">{formatDuration(a.time_taken_sec)}</td>
                <td className="px-4 py-3 tabular-nums">{formatRank(a.rank_position, a.total_participants)}</td>
                <td className="px-4 py-3 text-right">
                  {action.to ? (
                    <Link to={action.to}>
                      <Button
                        size="sm"
                        variant={action.variant}
                        icon={action.variant === 'primary' ? <ArrowRight className="h-3.5 w-3.5" /> : undefined}
                      >
                        {action.label}
                      </Button>
                    </Link>
                  ) : (
                    <Button size="sm" variant="ghost" disabled>{action.label}</Button>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
