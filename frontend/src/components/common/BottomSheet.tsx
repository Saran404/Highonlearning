import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';
import { ReactNode, useEffect } from 'react';

interface Props {
  open: boolean;
  onClose: () => void;
  title?: ReactNode;
  children: ReactNode;
  action?: ReactNode;
  maxHeight?: string;
}

export default function BottomSheet({
  open,
  onClose,
  title,
  children,
  action,
  maxHeight = 'max-h-[85vh]',
}: Props) {
  useEffect(() => {
    if (!open) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = prev;
      window.removeEventListener('keydown', onKey);
    };
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex flex-col justify-end">
          {/* Backdrop Scrim */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
            className="absolute inset-0 bg-navy-950/60 backdrop-blur-[2px]"
            aria-hidden="true"
          />

          {/* M3 Modal Bottom Sheet */}
          <motion.div
            role="dialog"
            aria-modal="true"
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: 'spring', damping: 28, stiffness: 320 }}
            className={`relative z-10 flex w-full flex-col rounded-t-3xl border-t border-line bg-white shadow-2xl pb-[calc(env(safe-area-inset-bottom)+1rem)] ${maxHeight}`}
          >
            {/* Drag Handle Indicator (M3 Spec) */}
            <div className="flex w-full cursor-grab justify-center py-2.5 active:cursor-grabbing" onClick={onClose}>
              <div className="h-1.5 w-10 rounded-full bg-navy-200" />
            </div>

            {/* Header */}
            {(title || action) && (
              <div className="flex items-center justify-between border-b border-line px-5 pb-3">
                <div className="text-lg font-bold text-navy">{title}</div>
                <div className="flex items-center gap-2">
                  {action}
                  <button
                    type="button"
                    onClick={onClose}
                    className="flex h-10 w-10 items-center justify-center rounded-full text-navy-500 hover:bg-navy-50 active:bg-navy-100"
                    aria-label="Close sheet"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
              </div>
            )}

            {/* Content Container */}
            <div className="overflow-y-auto px-5 py-4 overscroll-contain">
              {children}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
