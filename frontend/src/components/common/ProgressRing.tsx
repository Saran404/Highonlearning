import type { ReactNode } from 'react';

interface Props {
  value: number; // 0-100
  size?: number;
  stroke?: number;
  color?: string;
  children?: ReactNode;
  label?: string;
}

export default function ProgressRing({ value, size = 112, stroke = 10, color = '#0284c7', children, label }: Props) {
  const v = Math.min(100, Math.max(0, value));
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }} role="img" aria-label={label ?? `${Math.round(v)} percent`}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={r} stroke="#e2e8f0" strokeWidth={stroke} fill="none" />
        <circle cx={size / 2} cy={size / 2} r={r} stroke={color} strokeWidth={stroke} fill="none" strokeLinecap="round" strokeDasharray={c} strokeDashoffset={c * (1 - v / 100)} style={{ transition: 'stroke-dashoffset .6s ease' }} />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">{children ?? <span className="text-xl font-bold text-navy-900">{Math.round(v)}%</span>}</div>
    </div>
  );
}
