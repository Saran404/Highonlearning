import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';
import { ReactNode, useEffect } from 'react';

interface Props {
  open: boolean;
  onClose?: () => void;
  title?: ReactNode;
  children: ReactNode;
  footer?: ReactNode;
  /** false = cannot be closed by Esc / backdrop / X (used for exam-critical dialogs) */
  dismissible?: boolean;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  tone?: 'default' | 'danger' | 'warning';
}

const widths = { sm: 'max-w-sm', md: 'max-w-md', lg: 'max-w-2xl', xl: 'max-w-4xl' };
const tones = { default: 'border-line', danger: 'border-danger-300', warning: 'border-cream-300' };

export default function Modal({ open, onClose, title, children, footer, dismissible = true, size = 'md', tone = 'default' }: Props) {
  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && dismissible) onClose?.();
    };
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener('keydown', onKey);
    };
  }, [open, dismissible, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.15 }}>
          <div className="absolute inset-0 bg-navy/60" onClick={dismissible ? onClose : undefined} aria-hidden />
          <motion.div
            role="dialog"
            aria-modal="true"
            className={`relative m-0 flex max-h-[92vh] w-full flex-col rounded-t-2xl border bg-white shadow-2xl sm:m-4 sm:rounded-2xl ${widths[size]} ${tones[tone]}`}
            initial={{ y: 24, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 24, opacity: 0 }}
            transition={{ duration: 0.18 }}
          >
            {(title || dismissible) && (
              <header className="flex items-start justify-between gap-4 px-5 pt-5">
                <h2 className="text-lg">{title}</h2>
                {dismissible && onClose && (
                  <button onClick={onClose} className="rounded-md p-1 text-navy-400 hover:bg-navy-50" aria-label="Close">
                    <X className="h-5 w-5" />
                  </button>
                )}
              </header>
            )}
            <div className="overflow-y-auto px-5 py-4 text-sm text-navy-700">{children}</div>
            {footer && <footer className="flex flex-col-reverse gap-2 border-t border-line px-5 py-4 sm:flex-row sm:justify-end">{footer}</footer>}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
