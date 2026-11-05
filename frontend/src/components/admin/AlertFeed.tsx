import { CheckCircle2, PlayCircle, ShieldAlert } from 'lucide-react';
import type { FeedItem } from '../../types';
import { MALPRACTICE_LABEL } from '../../utils/constants';
import { timeAgo } from '../../utils/format';
import EmptyState from '../common/EmptyState';

function line(item: FeedItem) {
  const e = item.event;
  switch (e.type) {
    case 'MALPRACTICE_ALERT':
      return {
        icon: <ShieldAlert className="h-4 w-4 text-danger-600" />,
        tone: e.terminated ? 'bg-danger' : 'bg-cream',
        text: (
          <>
            <strong>{e.user_email}</strong> — {MALPRACTICE_LABEL[e.latest_type] ?? e.latest_type} (warning {e.count})
            {e.terminated && <span className="ml-1 font-semibold text-danger-700">· auto-submitted</span>}
          </>
        ),
      };
    case 'ATTEMPT_SUBMITTED':
      return {
        icon: <CheckCircle2 className="h-4 w-4 text-mint-600" />,
        tone: 'bg-white',
        text: (
          <>
            <strong>{e.user_email}</strong> submitted — {e.score} marks ({e.percentage}%)
          </>
        ),
      };
    default:
      return {
        icon: <PlayCircle className="h-4 w-4 text-sky" />,
        tone: 'bg-white',
        text: (
          <>
            <strong>{e.user_email}</strong> started “{e.assessment}”
          </>
        ),
      };
  }
}

/** Newest-first stream of WebSocket events. Click an item to open that attempt. */
export default function AlertFeed({ items, onOpen }: { items: FeedItem[]; onOpen: (attemptId: number) => void }) {
  if (items.length === 0) return <EmptyState title="Quiet for now" description="Live starts, warnings and submissions appear here as they happen." />;
  return (
    <ul className="divide-y divide-line" aria-live="polite">
      {items.map((it) => {
        const l = line(it);
        return (
          <li key={it.id}>
            <button onClick={() => onOpen(it.event.attempt_id)} className={`flex w-full items-start gap-3 px-4 py-3 text-left text-sm hover:bg-navy-50 ${l.tone}`}>
              <span className="mt-0.5">{l.icon}</span>
              <span className="min-w-0 flex-1 break-words">{l.text}</span>
              <span className="shrink-0 text-xs text-navy-400">{timeAgo(it.at)}</span>
            </button>
          </li>
        );
      })}
    </ul>
  );
}
