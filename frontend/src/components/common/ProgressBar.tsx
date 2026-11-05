interface Props {
  value: number; // 0-100
  tone?: 'sky' | 'mint' | 'danger' | 'cream';
  label?: string;
  className?: string;
}

const tones = { sky: 'bg-sky', mint: 'bg-mint-600', danger: 'bg-danger-600', cream: 'bg-cream-600' };

export default function ProgressBar({ value, tone = 'sky', label, className = '' }: Props) {
  const v = Math.min(100, Math.max(0, value));
  return (
    <div className={`h-2 w-full overflow-hidden rounded-full bg-navy-100 ${className}`} role="progressbar" aria-valuenow={Math.round(v)} aria-valuemin={0} aria-valuemax={100} aria-label={label}>
      <div className={`h-full rounded-full transition-[width] duration-500 ${tones[tone]}`} style={{ width: `${v}%` }} />
    </div>
  );
}
