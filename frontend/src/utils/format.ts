import { format, formatDistanceToNowStrict, parseISO } from 'date-fns';

/** 3725 -> "1:02:05", 125 -> "02:05". */
export function formatTime(totalSeconds: number): string {
  const s = Math.max(0, Math.floor(totalSeconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  const mm = String(m).padStart(2, '0');
  const ss = String(sec).padStart(2, '0');
  return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
}

/** 2520 -> "42m", 3900 -> "1h 5m", 45 -> "45s". */
export function formatDuration(totalSeconds: number | null | undefined): string {
  if (totalSeconds == null) return '—';
  const s = Math.max(0, Math.round(totalSeconds));
  if (s < 60) return `${s}s`;
  const h = Math.floor(s / 3600);
  const m = Math.round((s % 3600) / 60);
  return h > 0 ? `${h}h ${m}m` : `${m}m`;
}

export function formatDate(iso: string | null | undefined, pattern = 'dd MMM yyyy, h:mm a'): string {
  if (!iso) return '—';
  try {
    return format(parseISO(iso), pattern);
  } catch {
    return '—';
  }
}

export function timeAgo(iso: string | number): string {
  const d = typeof iso === 'number' ? new Date(iso) : parseISO(iso);
  return `${formatDistanceToNowStrict(d)} ago`;
}

export function formatRank(rank?: number | null, total?: number | null): string {
  if (!rank) return '—';
  return total ? `#${rank} of ${total}` : `#${rank}`;
}

export function formatMarks(score?: number | null, total?: number | null): string {
  return score == null || total == null ? '—' : `${score}/${total}`;
}

export function formatPercent(p?: number | null): string {
  return p == null ? '—' : `${Number.isInteger(p) ? p : p.toFixed(1)}%`;
}
