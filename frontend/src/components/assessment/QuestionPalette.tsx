import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';
import type { LocalAnswer } from '../../store/attemptStore';
import type { Question } from '../../types';
import { useIsDesktop } from '../../hooks/useMediaQuery';

interface Props {
  questions: Question[];
  answers: Record<number, LocalAnswer>;
  current: number;
  onGo: (index: number) => void;
  /** mobile bottom-sheet state (ignored on desktop, where the palette is a sidebar) */
  open: boolean;
  onClose: () => void;
}

function Grid({ questions, answers, current, onGo }: Omit<Props, 'open' | 'onClose'>) {
  const answered = questions.filter((q) => answers[q.id]?.selected != null).length;
  const marked = questions.filter((q) => answers[q.id]?.marked).length;
  return (
    <div>
      <div className="grid grid-cols-5 gap-2 sm:grid-cols-6 lg:grid-cols-5" role="list">
        {questions.map((q, i) => {
          const a = answers[q.id];
          const isCurrent = i === current;
          const cls = isCurrent
            ? 'bg-navy text-white border-navy'
            : a?.marked
              ? 'bg-cream text-cream-700 border-cream-300'
              : a?.selected != null
                ? 'bg-mint text-mint-700 border-mint-300'
                : 'bg-white text-navy-600 border-line';
          return (
            <button
              key={q.id}
              role="listitem"
              onClick={() => onGo(i)}
              aria-label={`Question ${i + 1}${a?.selected != null ? ', answered' : ''}${a?.marked ? ', marked for review' : ''}`}
              aria-current={isCurrent}
              className={`relative flex h-10 items-center justify-center rounded-lg border text-sm font-semibold tabular-nums ${cls}`}
            >
              {i + 1}
              {a?.marked && a.selected != null && !isCurrent && <span className="absolute right-1 top-1 h-1.5 w-1.5 rounded-full bg-cream-600" />}
            </button>
          );
        })}
      </div>
      <dl className="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
        <div className="rounded-lg bg-mint px-2 py-2 text-mint-700"><dd className="text-base font-semibold">{answered}</dd><dt>Answered</dt></div>
        <div className="rounded-lg bg-canvas px-2 py-2"><dd className="text-base font-semibold">{questions.length - answered}</dd><dt>Left</dt></div>
        <div className="rounded-lg bg-cream px-2 py-2 text-cream-700"><dd className="text-base font-semibold">{marked}</dd><dt>Review</dt></div>
      </dl>
    </div>
  );
}

/** The "answer sheet": a numbered grid coloured by state. Sidebar on desktop, bottom sheet on mobile. */
export default function QuestionPalette(props: Props) {
  const desktop = useIsDesktop();
  if (desktop) {
    return (
      <aside className="panel sticky top-20 w-64 shrink-0 self-start p-4" aria-label="Question palette">
        <h2 className="mb-3 text-sm">Question palette</h2>
        <Grid {...props} />
      </aside>
    );
  }
  return (
    <AnimatePresence>
      {props.open && (
        <motion.div className="fixed inset-0 z-50 flex items-end" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
          <div className="absolute inset-0 bg-navy-950/60 backdrop-blur-xs" onClick={props.onClose} aria-hidden />
          <motion.div
            className="relative max-h-[80vh] w-full overflow-y-auto rounded-t-3xl border-t border-line bg-white p-5 pb-[calc(1.5rem+env(safe-area-inset-bottom))]"
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ type: 'spring', damping: 28, stiffness: 300 }}
          >
            <div className="mx-auto mb-2.5 h-1.5 w-10 rounded-full bg-navy-200" onClick={props.onClose} />
            <div className="mb-4 flex items-center justify-between border-b border-line pb-2.5">
              <h2 className="text-base font-bold text-navy">Question Palette</h2>
              <button
                onClick={props.onClose}
                aria-label="Close palette"
                className="flex h-10 w-10 items-center justify-center rounded-full text-navy-500 hover:bg-navy-50 active:bg-navy-100 m3-touch"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <Grid {...props} onGo={(i) => { props.onGo(i); props.onClose(); }} />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
