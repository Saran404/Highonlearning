import { useCallback, useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { adminApi } from '../../api/admin';
import { toApiError } from '../../api/client';
import type { AttemptDrilldownData } from '../../types';
import { MALPRACTICE_LABEL } from '../../utils/constants';
import { formatDate, formatDuration, formatMarks, formatPercent } from '../../utils/format';
import Button from '../common/Button';
import ConfirmationModal from '../common/ConfirmationModal';
import Modal from '../common/Modal';
import { PageSkeleton } from '../common/Skeleton';
import SnapshotGallery from './SnapshotGallery';

type Tab = 'summary' | 'answers' | 'malpractice' | 'snapshots';

interface Props {
  attemptId: number | null;
  onClose: () => void;
  /** called after force-submit / reset so the parent can refresh its lists */
  onChanged: () => void;
}

export default function AttemptDrilldown({ attemptId, onClose, onChanged }: Props) {
  const [data, setData] = useState<AttemptDrilldownData | null>(null);
  const [tab, setTab] = useState<Tab>('summary');
  const [confirm, setConfirm] = useState<'force' | 'reset' | null>(null);
  const [busy, setBusy] = useState(false);
  const closeRef = useRef(onClose);
  closeRef.current = onClose;

  const load = useCallback(async () => {
    if (attemptId == null) return;
    try {
      setData(await adminApi.attempt(attemptId));
    } catch (e) {
      toast.error(toApiError(e).message);
      closeRef.current();
    }
  }, [attemptId]);

  useEffect(() => {
    setData(null);
    setTab('summary');
    void load();
  }, [load]);

  const run = async (kind: 'force' | 'reset') => {
    if (attemptId == null) return;
    setBusy(true);
    try {
      if (kind === 'force') {
        await adminApi.forceSubmit(attemptId);
        toast.success('Attempt submitted.');
        await load();
      } else {
        await adminApi.reset(attemptId);
        toast.success('Attempt deleted. The student can start again.');
        onClose();
      }
      onChanged();
    } catch (e) {
      toast.error(toApiError(e).message);
    } finally {
      setBusy(false);
      setConfirm(null);
    }
  };

  const a = data?.attempt;
  const tabs: [Tab, string][] = [['summary', 'Summary'], ['answers', `Answers${data ? ` (${data.answers.length})` : ''}`], ['malpractice', `Warnings${data ? ` (${data.malpractice_logs.length})` : ''}`], ['snapshots', `Snapshots${data ? ` (${data.snapshots.length})` : ''}`]];

  return (
    <>
      <Modal
        open={attemptId != null}
        onClose={onClose}
        size="xl"
        title={a ? `${a.user_name} · ${a.assessment_title}` : 'Attempt'}
        footer={
          a && (
            <>
              {a.status === 'IN_PROGRESS' && <Button variant="secondary" onClick={() => setConfirm('force')}>Force submit</Button>}
              <Button variant="danger" onClick={() => setConfirm('reset')}>Reset attempt</Button>
            </>
          )
        }
      >
        {!data || !a ? (
          <PageSkeleton />
        ) : (
          <div>
            <div className="mb-4 flex gap-1 overflow-x-auto border-b border-line" role="tablist">
              {tabs.map(([key, label]) => (
                <button key={key} role="tab" aria-selected={tab === key} onClick={() => setTab(key)} className={`whitespace-nowrap border-b-2 px-3 py-2 text-sm font-medium ${tab === key ? 'border-navy text-navy' : 'border-transparent text-navy-400 hover:text-navy-700'}`}>
                  {label}
                </button>
              ))}
            </div>

            {tab === 'summary' && (
              <dl className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                {[
                  ['Status', a.status.replace('_', ' ').toLowerCase()],
                  ['Student', a.user_email],
                  ['Score', formatMarks(a.score, a.total)],
                  ['Percentage', formatPercent(a.percentage)],
                  ['Time taken', formatDuration(a.time_taken_sec)],
                  ['Rank', a.rank_position ? `#${a.rank_position}` : '—'],
                  ['Started', formatDate(a.started_at)],
                  ['Submitted', formatDate(a.submitted_at)],
                  ['Warnings', String(a.malpractice_count)],
                ].map(([k, v]) => (
                  <div key={k} className="rounded-lg bg-canvas p-3">
                    <dt className="text-xs text-navy-500">{k}</dt>
                    <dd className="mt-0.5 break-words font-medium">{v}</dd>
                  </div>
                ))}
              </dl>
            )}

            {tab === 'answers' && (
              <ol className="divide-y divide-line">
                {data.answers.map((x, i) => (
                  <li key={x.question_id} className="flex items-start gap-3 py-2.5">
                    <span className={`mt-0.5 rounded-md px-2 py-0.5 text-xs font-semibold ${x.selected_index == null ? 'bg-navy-100 text-navy-500' : x.is_correct ? 'bg-mint text-mint-700' : 'bg-danger text-danger-700'}`}>Q{i + 1}</span>
                    <div className="min-w-0 flex-1">
                      <p className="line-clamp-2">{x.question_text}</p>
                      <p className="mt-0.5 text-xs text-navy-500">
                        Chose {x.selected_index == null ? '—' : String.fromCharCode(65 + x.selected_index)} · correct {String.fromCharCode(65 + x.correct_index)}
                        {x.marked_for_review && ' · marked for review'}
                      </p>
                    </div>
                  </li>
                ))}
              </ol>
            )}

            {tab === 'malpractice' &&
              (data.malpractice_logs.length === 0 ? (
                <p className="py-6 text-center text-navy-500">No violations recorded.</p>
              ) : (
                <ol className="space-y-2">
                  {data.malpractice_logs.map((l, i) => (
                    <li key={l.log_id} className="flex items-center justify-between rounded-lg bg-cream px-3 py-2.5">
                      <span><strong>#{i + 1}</strong> {MALPRACTICE_LABEL[l.type] ?? l.type}</span>
                      <span className="text-xs tabular-nums text-cream-700">{formatDate(l.occurred_at, 'h:mm:ss a')}</span>
                    </li>
                  ))}
                </ol>
              ))}

            {tab === 'snapshots' && <SnapshotGallery snapshots={data.snapshots} />}
          </div>
        )}
      </Modal>

      <ConfirmationModal
        open={confirm === 'force'}
        title="Force-submit this attempt?"
        confirmLabel="Submit attempt"
        loading={busy}
        onCancel={() => setConfirm(null)}
        onConfirm={() => void run('force')}
      >
        The student's saved answers will be scored and ranked now. This is recorded in the audit log.
      </ConfirmationModal>
      <ConfirmationModal
        open={confirm === 'reset'}
        title="Reset this attempt?"
        confirmLabel="Delete attempt"
        danger
        loading={busy}
        onCancel={() => setConfirm(null)}
        onConfirm={() => void run('reset')}
      >
        This permanently deletes the attempt with its answers, warnings and snapshots, and lets the student start over. It cannot be undone. This is recorded in the audit log.
      </ConfirmationModal>
    </>
  );
}
