import React, { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Activity,
  Check,
  Clock,
  Droplets,
  Eye,
  HeartPulse,
  Moon,
  Sparkles,
  Trophy,
  X,
} from 'lucide-react';
import { useLocation } from 'react-router-dom';
import { useWellnessStore } from '../../store/wellnessStore';
import { WellnessCategory } from '../../utils/wellnessQuotes';

function getCategoryIcon(category: WellnessCategory) {
  switch (category) {
    case 'EYE_CARE':
      return <Eye className="h-5 w-5 text-sky-600" />;
    case 'HYDRATION':
      return <Droplets className="h-5 w-5 text-blue-600" />;
    case 'MOVEMENT':
      return <Activity className="h-5 w-5 text-emerald-600" />;
    case 'MENTAL_WELLBEING':
      return <HeartPulse className="h-5 w-5 text-violet-600" />;
    case 'REST_SLEEP':
      return <Moon className="h-5 w-5 text-indigo-600" />;
    case 'MOTIVATION':
      return <Trophy className="h-5 w-5 text-amber-600" />;
    case 'END_OF_SESSION':
      return <Sparkles className="h-5 w-5 text-amber-600" />;
    default:
      return <Sparkles className="h-5 w-5 text-sky-600" />;
  }
}

const AUTO_DISMISS_SECONDS = 18;

export default function WellnessToast() {
  const { activeReminder, dismissReminder } = useWellnessStore();
  const location = useLocation();
  const [progress, setProgress] = useState(100);
  const [isPaused, setIsPaused] = useState(false);

  const isAssessmentRoute =
    location.pathname.startsWith('/attempts') ||
    location.pathname.startsWith('/assessments') ||
    location.pathname.startsWith('/results');

  useEffect(() => {
    if (isAssessmentRoute || !activeReminder) {
      setProgress(100);
      return;
    }

    setProgress(100);
    const startTime = Date.now();
    const duration = AUTO_DISMISS_SECONDS * 1000;

    const interval = setInterval(() => {
      if (isPaused) return;
      const elapsed = Date.now() - startTime;
      const remainingPct = Math.max(0, 100 - (elapsed / duration) * 100);
      setProgress(remainingPct);

      if (elapsed >= duration) {
        clearInterval(interval);
        dismissReminder();
      }
    }, 100);

    return () => clearInterval(interval);
  }, [isAssessmentRoute, activeReminder?.id, isPaused, dismissReminder]);

  // Reminders are strictly disabled during assessments or when no reminder is active
  if (isAssessmentRoute || !activeReminder) {
    return null;
  }

  return (
    <aside aria-label="Wellness Reminders" aria-live="polite">
      <AnimatePresence>
        {activeReminder && (
          <motion.div
            key={activeReminder.id}
            initial={{ opacity: 0, y: 30, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            onMouseEnter={() => setIsPaused(true)}
            onMouseLeave={() => setIsPaused(false)}
            className="fixed bottom-24 right-4 left-4 z-40 sm:left-auto sm:right-6 sm:bottom-6 w-auto sm:w-full sm:max-w-md"
            role="status"
          >
            <div
              className={`relative overflow-hidden rounded-2xl border ${activeReminder.config.colorTheme.border} bg-white/95 p-5 shadow-2xl backdrop-blur-md transition-all`}
            >
              {/* Category Header */}
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`flex h-10 w-10 items-center justify-center rounded-xl ${activeReminder.config.colorTheme.badgeBg}`}
                  >
                    {getCategoryIcon(activeReminder.category)}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold text-navy-900">
                        {activeReminder.config.title}
                      </span>
                      <span
                        className={`rounded-full px-2 py-0.5 text-[11px] font-medium ${activeReminder.config.colorTheme.badgeBg} ${activeReminder.config.colorTheme.badgeText}`}
                      >
                        {activeReminder.config.badge}
                      </span>
                    </div>
                    <div className="flex items-center gap-1 text-xs text-navy-500">
                      <Clock className="h-3 w-3" />
                      <span>
                        Studying for {activeReminder.elapsedMinutes} mins
                      </span>
                    </div>
                  </div>
                </div>

                {/* Top Close Button */}
                <button
                  type="button"
                  onClick={dismissReminder}
                  className="rounded-lg p-1 text-navy-400 transition-colors hover:bg-navy-50 hover:text-navy-700"
                  aria-label="Dismiss reminder"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>

              {/* Quote Content */}
              <div className="my-3.5 rounded-xl bg-slate-50/80 p-3.5 border border-slate-100">
                <p className="text-base font-semibold text-navy-900 leading-snug">
                  "{activeReminder.quote}"
                </p>
                <p className="mt-1 text-xs text-navy-600">
                  {activeReminder.config.actionTip}
                </p>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-end gap-2 pt-1">
                <button
                  type="button"
                  onClick={dismissReminder}
                  className="flex items-center gap-1.5 rounded-lg px-3.5 py-1.5 text-xs font-semibold text-navy-600 transition-colors hover:bg-navy-100"
                >
                  Dismiss
                </button>
                <button
                  type="button"
                  onClick={dismissReminder}
                  className={`flex items-center gap-1.5 rounded-lg px-4 py-1.5 text-xs font-semibold transition-all shadow-xs ${activeReminder.config.colorTheme.button}`}
                >
                  <Check className="h-3.5 w-3.5" />
                  <span>Got it!</span>
                </button>
              </div>

              {/* Animated Progress Bar for Auto-dismiss */}
              <div className="absolute bottom-0 left-0 right-0 h-1 bg-slate-100">
                <motion.div
                  className="h-full bg-navy-500/30"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </aside>
  );
}
