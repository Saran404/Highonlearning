import type { StudentRow } from '../../types';
import { formatDate } from '../../utils/format';
import EmptyState from '../common/EmptyState';

export default function StudentTable({ rows }: { rows: StudentRow[] }) {
  if (rows.length === 0) return <EmptyState title="No students found" />;
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-line text-xs text-navy-500">
          <tr>
            {['Student', 'Session', 'Last seen', 'Attempts', 'Joined'].map((h) => <th key={h} className="whitespace-nowrap px-4 py-3 font-medium">{h}</th>)}
          </tr>
        </thead>
        <tbody className="divide-y divide-line">
          {rows.map((s) => (
            <tr key={s.id}>
              <td className="px-4 py-3">
                <div className="font-medium">{s.name}</div>
                <div className="text-xs text-navy-400">{s.email}</div>
              </td>
              <td className="px-4 py-3">
                <span className={`inline-flex items-center gap-1.5 text-xs font-medium ${s.has_active_session ? 'text-mint-700' : 'text-navy-400'}`}>
                  <span className={`h-2 w-2 rounded-full ${s.has_active_session ? 'bg-mint-600' : 'bg-navy-200'}`} />
                  {s.has_active_session ? 'Signed in' : 'Signed out'}
                </span>
              </td>
              <td className="px-4 py-3 tabular-nums text-navy-500">{formatDate(s.last_seen_at)}</td>
              <td className="px-4 py-3 tabular-nums">{s.attempts_count}</td>
              <td className="px-4 py-3 text-navy-500">{formatDate(s.created_at, 'dd MMM yyyy')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
