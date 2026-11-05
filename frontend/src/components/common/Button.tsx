import { Loader2 } from 'lucide-react';
import type { ButtonHTMLAttributes, ReactNode } from 'react';

type Variant = 'primary' | 'secondary' | 'danger' | 'ghost' | 'success' | 'accent';
type Size = 'sm' | 'md' | 'lg';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  loading?: boolean;
  icon?: ReactNode;
  fullWidth?: boolean;
}

const variants: Record<Variant, string> = {
  primary: 'bg-navy text-white hover:bg-navy-800 disabled:bg-navy-200 shadow-xs active:bg-navy-950',
  secondary: 'bg-white text-navy border border-line hover:bg-sky-50/60 hover:border-sky-200 disabled:text-navy-300 active:bg-sky-100',
  accent: 'bg-gradient-to-r from-amber-500 to-orange-500 text-white hover:from-amber-600 hover:to-orange-600 shadow-sm disabled:opacity-50 active:from-amber-700 active:to-orange-700',
  success: 'bg-mint-600 text-white hover:bg-mint-700 disabled:opacity-50 active:bg-mint-800',
  danger: 'bg-danger-600 text-white hover:bg-danger-700 disabled:opacity-50 active:bg-danger-800',
  ghost: 'bg-transparent text-sky-700 hover:bg-sky-50 disabled:text-navy-300 active:bg-sky-100/70',
};
const sizes: Record<Size, string> = {
  sm: 'min-h-[2.75rem] px-3.5 py-2 text-sm gap-1.5',
  md: 'min-h-[3rem] px-4 py-2.5 text-sm gap-2',
  lg: 'min-h-[3.25rem] px-5 py-3 text-base gap-2',
};

export default function Button({ variant = 'primary', size = 'md', loading, icon, fullWidth, className = '', children, disabled, type = 'button', ...rest }: Props) {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center rounded-xl font-semibold m3-touch transition-all disabled:cursor-not-allowed select-none ${variants[variant]} ${sizes[size]} ${fullWidth ? 'w-full' : ''} ${className}`}
      {...rest}
    >
      {loading ? <Loader2 className="h-4 w-4 animate-spin shrink-0" aria-hidden /> : icon}
      {children}
    </button>
  );
}
