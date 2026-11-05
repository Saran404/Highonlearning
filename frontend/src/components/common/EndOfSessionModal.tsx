import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Clock, LogOut, Moon, RefreshCw, Sparkles, Trophy, X } from 'lucide-react';
import { useWellnessStore } from '../../store/wellnessStore';
import { getRandomWellnessQuote } from '../../utils/wellnessQuotes';

function formatDuration(minutes: number, seconds: number): string {
  if (minutes < 1) {
    return `${seconds} seconds`;
  }
  const hours = Math.floor(minutes / 60);
  const remainingMins = minutes % 60;
  if (hours > 0) {
    return `${hours} hr ${remainingMins} min`;
  }
  return `${minutes} min`;
}

export default function EndOfSessionModal() {
  const {
    isEndOfSessionOpen,
    dismissEndOfSession,
    onLogoutConfirmed,
    endOfSessionQuote,
    elapsedMinutes,
    elapsedSeconds,
  } = useWellnessStore();

  const [currentQuote, setCurrentQuote] = useState('');
  const activeQuote = currentQuote || endOfSessionQuote;

  const handleRefreshQuote = () => {
    setCurrentQuote(getRandomWellnessQuote('END_OF_SESSION'));
  };

  const handleConfirmLogout = () => {
    dismissEndOfSession();
    if (onLogoutConfirmed) {
      onLogoutConfirmed();
    }
  };

  return (
    <AnimatePresence>
      {isEndOfSessionOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
        >
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-navy-950/70 backdrop-blur-sm"
            onClick={dismissEndOfSession}
            aria-hidden
          />

          {/* Modal Container */}
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-labelledby="end-session-title"
            className="relative w-full max-w-lg overflow-hidden rounded-2xl border border-amber-200/80 bg-white p-6 shadow-2xl"
            initial={{ scale: 0.93, opacity: 0, y: 15 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.93, opacity: 0, y: 15 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          >
            {/* Top Close button */}
            <button
              onClick={dismissEndOfSession}
              className="absolute right-4 top-4 rounded-lg p-1.5 text-navy-400 hover:bg-navy-50 hover:text-navy-700"
              aria-label="Cancel and continue studying"
            >
              <X className="h-5 w-5" />
            </button>

            {/* Header with decorative badge */}
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-amber-600 shadow-xs">
                <Trophy className="h-6 w-6" />
              </div>
              <div>
                <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 px-2.5 py-0.5 text-xs font-semibold text-amber-800 border border-amber-200">
                  <Sparkles className="h-3.5 w-3.5 text-amber-600" />
                  Study Session Complete
                </span>
                <h3
                  id="end-session-title"
                  className="mt-0.5 text-xl font-bold text-navy-900"
                >
                  Great Work Today!
                </h3>
              </div>
            </div>

            {/* Session Stats Banner */}
            <div className="my-5 flex items-center justify-between rounded-xl bg-navy-50/70 p-4 border border-navy-100">
              <div className="flex items-center gap-2.5 text-navy-800">
                <Clock className="h-5 w-5 text-sky-600" />
                <div>
                  <div className="text-xs font-medium text-navy-500 uppercase tracking-wider">
                    Session Duration
                  </div>
                  <div className="text-lg font-bold text-navy-950">
                    {formatDuration(elapsedMinutes, elapsedSeconds)}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-1.5 text-xs font-medium text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
                <span>Progress Saved</span>
                <span className="text-base leading-none">✓</span>
              </div>
            </div>

            {/* Motivational / Rest Quote Box */}
            <div className="relative rounded-xl border border-amber-200 bg-gradient-to-br from-amber-50/90 via-orange-50/40 to-yellow-50/60 p-4 shadow-xs">
              <div className="flex items-center justify-between pb-1">
                <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-amber-800">
                  <Moon className="h-3.5 w-3.5 text-amber-600" />
                  Mindset & Rest Reminder
                </div>
                <button
                  onClick={handleRefreshQuote}
                  title="Show another inspiring quote"
                  className="flex items-center gap-1 rounded-md px-1.5 py-0.5 text-xs text-amber-700 hover:bg-amber-100/70 transition-colors"
                >
                  <RefreshCw className="h-3 w-3" />
                  <span>New quote</span>
                </button>
              </div>

              <blockquote className="my-2 text-center text-lg font-bold italic text-navy-900">
                "{activeQuote}"
              </blockquote>

              <p className="text-center text-xs text-navy-600">
                Rest and good sleep reinforce the neural connections formed during your study session.
              </p>
            </div>

            {/* Footer Buttons */}
            <div className="mt-6 flex flex-col-reverse gap-2.5 sm:flex-row sm:justify-end">
              <button
                type="button"
                onClick={dismissEndOfSession}
                className="w-full rounded-xl border border-navy-200 px-4 py-2.5 text-sm font-semibold text-navy-700 hover:bg-navy-50 transition-colors sm:w-auto"
              >
                Continue Studying
              </button>
              <button
                type="button"
                onClick={handleConfirmLogout}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-navy-900 px-5 py-2.5 text-sm font-semibold text-white shadow-md hover:bg-navy-800 transition-colors sm:w-auto"
              >
                <LogOut className="h-4 w-4" />
                <span>Log Out & Rest</span>
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
