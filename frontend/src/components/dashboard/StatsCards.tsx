import type { DashboardStats } from '../../types';
import { formatPercent } from '../../utils/format';

/** The four headline numbers as one band: dividers, not four separate cards. */
export default function StatsCards({ stats }: { stats: DashboardStats }) {
  const coursesValue = stats.courses_completed !== undefined && stats.courses_total
    ? `${stats.courses_completed}/${stats.courses_total}`
    : String(stats.courses_enrolled);
  const coursesLabel = stats.courses_completed !== undefined ? 'Courses completed' : 'Courses enrolled';

  const items = [
    { label: coursesLabel, value: coursesValue },
    { label: 'Tests completed', value: `${stats.assessments_completed}/${stats.assessments_total}` },
    { label: 'Average score', value: stats.assessments_completed ? formatPercent(stats.avg_percentage) : '—' },
    { label: 'Best rank', value: stats.best_rank ? `#${stats.best_rank}` : '—' },
  ];
  return (
    <dl className="panel grid grid-cols-2 divide-line sm:grid-cols-4 sm:divide-x border-line">
      {items.map((it, i) => (
        <div key={it.label} className={`px-4 py-4 sm:px-5 ${i < 2 ? 'border-b border-line sm:border-b-0' : ''} ${i % 2 === 0 ? 'border-r border-line sm:border-r-0' : ''}`}>
          <dd className="text-2xl font-bold tracking-tight text-navy-900 tabular-nums">{it.value}</dd>
          <dt className="mt-1 text-xs font-medium text-navy-500">{it.label}</dt>
        </div>
      ))}
    </dl>
  );
}
