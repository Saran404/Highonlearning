import { Bar, BarChart, CartesianGrid, Cell, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { AssessmentItem } from '../../types';
import { formatDuration } from '../../utils/format';
import EmptyState from '../common/EmptyState';

/** Score-per-test chart plus the latest completed tests. */
export default function RecentActivity({ completed }: { completed: AssessmentItem[] }) {
  if (completed.length === 0) {
    return <EmptyState title="No results yet" description="Finish your first graded test and your scores will show up here." />;
  }
  const data = completed.map((a) => ({ name: a.title, pct: a.percentage ?? 0, pass: a.pass_percentage }));
  return (
    <div>
      <div className="h-48 w-full" role="img" aria-label="Percentage scored in each completed test">
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
            <CartesianGrid vertical={false} stroke="#dde5ee" />
            <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#5a86ac' }} tickLine={false} axisLine={false} interval={0} />
            <YAxis domain={[0, 100]} tick={{ fontSize: 11, fill: '#5a86ac' }} tickLine={false} axisLine={false} />
            <Tooltip formatter={(v) => [`${v}%`, 'Score']} cursor={{ fill: '#eef3f9' }} />
            <ReferenceLine y={data[0]?.pass ?? 60} stroke="#a8690f" strokeDasharray="4 4" />
            <Bar dataKey="pct" radius={[4, 4, 0, 0]} maxBarSize={44}>
              {data.map((d) => (
                <Cell key={d.name} fill={d.pct >= d.pass ? '#1f8a54' : '#2b7fc9'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-1 text-xs text-navy-400">Dashed line marks the pass percentage.</p>
      <ul className="mt-4 divide-y divide-line text-sm">
        {completed.slice(-4).reverse().map((a) => (
          <li key={a.id} className="flex items-center justify-between py-2">
            <span className="font-medium">{a.title}</span>
            <span className="text-navy-500 tabular-nums">{a.score}/{a.total} · {formatDuration(a.time_taken_sec)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
