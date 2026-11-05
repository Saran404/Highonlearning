import { ReactNode } from 'react';
import { Link } from 'react-router-dom';

interface Props {
  to?: string;
  onClick?: () => void;
  icon: ReactNode;
  label?: string;
  className?: string;
}

export default function FloatingActionButton({
  to,
  onClick,
  icon,
  label,
  className = '',
}: Props) {
  const content = (
    <div
      className={`flex items-center gap-2.5 rounded-2xl bg-gradient-to-r from-navy to-sky-800 text-white shadow-m3-fab px-4 py-3.5 text-sm font-bold border border-white/20 m3-touch active:scale-95 transition-all select-none ${className}`}
    >
      <span className="shrink-0 text-amber-300">{icon}</span>
      {label && <span className="max-w-[200px] truncate">{label}</span>}
    </div>
  );

  return (
    <div className="fixed bottom-20 right-4 z-20 sm:hidden pb-[env(safe-area-inset-bottom)]">
      {to ? (
        <Link to={to} aria-label={label || 'Quick action'}>
          {content}
        </Link>
      ) : (
        <button type="button" onClick={onClick} aria-label={label || 'Quick action'}>
          {content}
        </button>
      )}
    </div>
  );
}
