import { Radio, RefreshCw } from 'lucide-react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { adminApi } from '../api/admin';
import { toApiError } from '../api/client';
import AlertFeed from '../components/admin/AlertFeed';
import AttemptDrilldown from '../components/admin/AttemptDrilldown';
import StudentTable from '../components/admin/StudentTable';
import AdminReflectionSection from '../components/admin/AdminReflectionSection';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import EmptyState from '../components/common/EmptyState';
import { useWebSocket } from '../hooks/useWebSocket';
import { useAuthStore } from '../store/authStore';
import type { AdminEvent, AlertRow, AttemptRow, FeedItem, LiveAttemptRow, Page, StudentRow } from '../types';
import { MALPRACTICE_LABEL, getWsUrl } from '../utils/constants';
import { formatDate, formatMarks, formatPercent } from '../utils/format';

type Tab = 'live' | 'attempts' | 'students' | 'reflections';

function Pager({ page, size, total, onPage }: { page: number; size: number; total: number; onPage: (p: number) => void }) {
  const pages = Math.max(1, Math.ceil(total / size));
  return (
    <div className="flex items-center justify-between border-t border-line px-4 py-3 text-sm text-navy-500">
      <span>{total} total</span>
      <div className="flex items-center gap-2">
        <Button size="sm" variant="secondary" disabled={page <= 1} onClick={() => onPage(page - 1)}>Prev</Button>
        <span className="tabular-nums">{page} / {pages}</span>
        <Button size="sm" variant="secondary" disabled={page >= pages} onClick={() => onPage(page + 1)}>Next</Button>
      </div>
    </div>
  );
}

const alertToEvent = (a: AlertRow): AdminEvent => ({ type: 'MALPRACTICE_ALERT', attempt_id: a.attempt_id, user_email: a.user_email, count: a.malpractice_count, latest_type: a.type, terminated: a.attempt_status === 'FLAGGED' });

export default function AdminDashboardPage() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const [tab, setTab] = useState<Tab>('live');
  const [feed, setFeed] = useState<FeedItem[]>([]);
  const [live, setLive] = useState<LiveAttemptRow[]>([]);
  const [attempts, setAttempts] = useState<Page<AttemptRow> | null>(null);
  const [students, setStudents] = useState<Page<StudentRow> | null>(null);
  const [status, setStatus] = useState('');
  const [attemptPage, setAttemptPage] = useState(1);
  const [search, setSearch] = useState('');
  const [studentPage, setStudentPage] = useState(1);
  const [open, setOpen] = useState<number | null>(null);
  const seq = useRef(0);

  const pushEvent = useCallback((event: AdminEvent, at = Date.now()) => {
    seq.current += 1;
    setFeed((f) => [{ id: `${at}-${seq.current}`, at, event }, ...f].slice(0, 200));
  }, []);

  const loadLive = useCallback(() => adminApi.live().then(setLive).catch(() => undefined), []);
  const loadAttempts = useCallback(() => adminApi.attempts({ status: status || undefined, page: attemptPage }).then(setAttempts).catch((e) => toast.error(toApiError(e).message)), [status, attemptPage]);
  const loadStudents = useCallback(() => adminApi.students({ search: search || undefined, page: studentPage }).then(setStudents).catch((e) => toast.error(toApiError(e).message)), [search, studentPage]);

  // History for the feed, then live events on top of it.
  useEffect(() => {
    adminApi.alerts().then((rows) => setFeed(rows.map((r, i) => ({ id: `h-${r.log_id}`, at: Date.parse(r.occurred_at) - i, event: alertToEvent(r) })))).catch(() => undefined);
    void loadLive();
    const t = window.setInterval(() => void loadLive(), 30_000);
    return () => window.clearInterval(t);
  }, [loadLive]);

  useEffect(() => { if (tab === 'attempts') void loadAttempts(); }, [tab, loadAttempts]);
  useEffect(() => { if (tab === 'students') void loadStudents(); }, [tab, loadStudents]);

  const wsBase = getWsUrl();
  const socket = useWebSocket(accessToken ? `${wsBase}/ws/admin?token=${encodeURIComponent(accessToken)}` : null, (data) => {
    const e = data as AdminEvent;
    if (!e?.type) return;
    pushEvent(e);
    if (e.type === 'MALPRACTICE_ALERT') toast(`${e.user_email}: ${MALPRACTICE_LABEL[e.latest_type] ?? e.latest_type} (warning ${e.count})`, { icon: e.terminated ? '🚫' : '⚠️' });
    void loadLive();
  });

  const tabs: [Tab, string][] = [['live', 'Live'], ['attempts', 'Attempts'], ['students', 'Students'], ['reflections', 'Reflection Activity']];
  const remaining = useMemo(() => (row: LiveAttemptRow) => Math.max(0, Math.round((Date.parse(row.deadline_at) - Date.now()) / 60000)), []);

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl">Admin</h1>
          <p className="text-sm text-navy-500">Monitor attempts, review warnings and snapshots.</p>
        </div>
        <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium ${socket === 'open' ? 'bg-mint text-mint-700' : 'bg-cream text-cream-700'}`}>
          <Radio className="h-3.5 w-3.5" /> {socket === 'open' ? 'Live feed connected' : 'Reconnecting…'}
        </span>
      </div>

      <div className="flex gap-1 border-b border-line" role="tablist">
        {tabs.map(([k, label]) => (
          <button key={k} role="tab" aria-selected={tab === k} onClick={() => setTab(k)} className={`border-b-2 px-4 py-2.5 text-sm font-medium ${tab === k ? 'border-navy text-navy' : 'border-transparent text-navy-400 hover:text-navy-700'}`}>{label}{k === 'live' && live.length > 0 && <span className="ml-1.5 rounded-full bg-sky px-1.5 py-0.5 text-xs text-white">{live.length}</span>}</button>
        ))}
      </div>

      {tab === 'live' && (
        <div className="grid gap-5 lg:grid-cols-2">
          <Card title="In progress now" padded={false}>
            {live.length === 0 ? <EmptyState title="Nobody is taking a test right now" /> : (
              <ul className="divide-y divide-line">
                {live.map((r) => (
                  <li key={r.attempt_id}>
                    <button onClick={() => setOpen(r.attempt_id)} className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left text-sm hover:bg-navy-50">
                      <span className="min-w-0"><span className="block truncate font-medium">{r.user_name}</span><span className="block truncate text-xs text-navy-400">{r.assessment_title}</span></span>
                      <span className="shrink-0 text-right text-xs"><span className="block tabular-nums text-navy-600">{remaining(r)} min left</span><span className={r.malpractice_count ? 'font-semibold text-danger-700' : 'text-navy-400'}>{r.malpractice_count} warnings</span></span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </Card>
          <Card title="Activity" padded={false}><div className="max-h-[32rem] overflow-y-auto"><AlertFeed items={feed} onOpen={setOpen} /></div></Card>
        </div>
      )}

      {tab === 'attempts' && (
        <Card padded={false} title="All attempts" action={
          <div className="flex items-center gap-2">
            <select className="field !w-auto !py-1.5" value={status} onChange={(e) => { setStatus(e.target.value); setAttemptPage(1); }} aria-label="Filter by status">
              <option value="">All statuses</option><option value="IN_PROGRESS">In progress</option><option value="SUBMITTED">Submitted</option><option value="AUTO_SUBMITTED">Auto-submitted</option><option value="FLAGGED">Flagged</option>
            </select>
            <Button size="sm" variant="secondary" onClick={() => void loadAttempts()} icon={<RefreshCw className="h-4 w-4" />} aria-label="Refresh" />
          </div>
        }>
          {!attempts ? <div className="p-6 text-sm text-navy-500">Loading…</div> : attempts.items.length === 0 ? <EmptyState title="No attempts match" /> : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="border-b border-line text-xs text-navy-500"><tr>{['Student', 'Assessment', 'Status', 'Score', '%', 'Warnings', 'Started'].map((h) => <th key={h} className="whitespace-nowrap px-4 py-3 font-medium">{h}</th>)}</tr></thead>
                <tbody className="divide-y divide-line">
                  {attempts.items.map((a) => (
                    <tr key={a.attempt_id} onClick={() => setOpen(a.attempt_id)} className="cursor-pointer hover:bg-navy-50">
                      <td className="px-4 py-3"><div className="font-medium">{a.user_name}</div><div className="text-xs text-navy-400">{a.user_email}</div></td>
                      <td className="px-4 py-3">{a.assessment_title}</td>
                      <td className="px-4 py-3"><span className={`rounded-full px-2.5 py-1 text-xs font-medium ${a.status === 'FLAGGED' ? 'bg-danger text-danger-700' : a.status === 'IN_PROGRESS' ? 'bg-cream text-cream-700' : 'bg-mint text-mint-700'}`}>{a.status.replace('_', ' ').toLowerCase()}</span></td>
                      <td className="px-4 py-3 tabular-nums">{formatMarks(a.score, a.total)}</td>
                      <td className="px-4 py-3 tabular-nums">{formatPercent(a.percentage)}</td>
                      <td className="px-4 py-3 tabular-nums">{a.malpractice_count}</td>
                      <td className="whitespace-nowrap px-4 py-3 text-navy-500">{formatDate(a.started_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {attempts && <Pager page={attemptPage} size={attempts.page_size} total={attempts.total} onPage={setAttemptPage} />}
        </Card>
      )}

      {tab === 'students' && (
        <Card padded={false} title="Students" action={<input className="field !w-56 !py-1.5" placeholder="Search name or email" value={search} onChange={(e) => { setSearch(e.target.value); setStudentPage(1); }} aria-label="Search students" />}>
          {students ? <StudentTable rows={students.items} /> : <div className="p-6 text-sm text-navy-500">Loading…</div>}
          {students && <Pager page={studentPage} size={students.page_size} total={students.total} onPage={setStudentPage} />}
        </Card>
      )}

      {tab === 'reflections' && <AdminReflectionSection />}

      <AttemptDrilldown attemptId={open} onClose={() => setOpen(null)} onChanged={() => { void loadLive(); if (tab === 'attempts') void loadAttempts(); }} />
    </div>
  );
}
