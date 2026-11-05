import { AnimatePresence, motion } from 'framer-motion';
import {
  ArrowRight,
  Award,
  BookOpen,
  CheckCircle2,
  Clock,
  Sparkles,
  Trophy,
  X,
  Play,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useResumeSessionStore } from '../../store/resumeSessionStore';
import Button from './Button';

export default function ResumeSessionModal() {
  const { isOpen, resumeData, closeResumeModal } = useResumeSessionStore();
  const navigate = useNavigate();

  if (!isOpen || !resumeData) return null;

  const isTamil = localStorage.getItem('exampro_lang') === 'ta';
  const {
    userName,
    lastActiveTimeText,
    practiceFinished,
    practiceInProgress,
    assessmentFinished,
    assessmentInProgress,
    nextActionItem,
  } = resumeData;

  const handleResumeClick = () => {
    closeResumeModal();
    if (nextActionItem?.to) {
      navigate(nextActionItem.to);
    } else {
      navigate('/courses');
    }
  };

  const handleGoToDashboard = () => {
    closeResumeModal();
    navigate('/dashboard');
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
        >
          {/* Backdrop Scrim */}
          <div
            className="absolute inset-0 bg-navy-950/75 backdrop-blur-sm"
            onClick={closeResumeModal}
            aria-hidden
          />

          {/* Modal Container */}
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-labelledby="resume-modal-title"
            className="relative w-full max-w-xl overflow-hidden rounded-3xl border border-sky-200/90 bg-white shadow-2xl"
            initial={{ scale: 0.92, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.92, opacity: 0, y: 20 }}
            transition={{ type: 'spring', damping: 26, stiffness: 320 }}
          >
            {/* Top Accent Gradient Bar */}
            <div className="h-2 w-full bg-gradient-to-r from-sky-500 via-navy-600 to-amber-500" />

            {/* Close Button */}
            <button
              onClick={closeResumeModal}
              className="absolute right-4 top-5 rounded-full p-1.5 text-navy-400 hover:bg-navy-50 hover:text-navy-700 transition-colors"
              aria-label={isTamil ? 'மூடுக' : 'Close'}
            >
              <X className="h-5 w-5" />
            </button>

            <div className="p-5 sm:p-7">
              {/* Header */}
              <div className="flex items-start gap-3.5">
                <div className="flex h-12 w-12 sm:h-14 sm:w-14 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-500 to-navy-700 text-white shadow-md">
                  <Sparkles className="h-6 w-6 sm:h-7 sm:w-7 text-amber-300" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="inline-flex items-center gap-1.5 rounded-full bg-sky-50 px-2.5 py-0.5 text-xs font-semibold text-sky-800 border border-sky-200">
                      <Clock className="h-3.5 w-3.5 text-sky-600" />
                      {isTamil
                        ? `முந்தைய வருகை: ${lastActiveTimeText}`
                        : `Last active: ${lastActiveTimeText}`}
                    </span>
                  </div>
                  <h2
                    id="resume-modal-title"
                    className="mt-1 text-xl sm:text-2xl font-bold text-navy-950 leading-tight"
                  >
                    {isTamil
                      ? `மீண்டும் வருக, ${userName}!`
                      : `Welcome Back, ${userName}!`}
                  </h2>
                  <p className="text-xs sm:text-sm text-navy-500 mt-0.5">
                    {isTamil
                      ? 'உங்கள் முந்தைய அமர்வில் முடித்த விவரங்கள் மற்றும் தொடர வேண்டியவை:'
                      : 'Pick up right where you left off in your last study session:'}
                  </p>
                </div>
              </div>

              {/* Accomplishments from last login */}
              <div className="mt-5 space-y-3">
                <div className="text-[11px] font-bold uppercase tracking-wider text-navy-400">
                  {isTamil ? 'முந்தைய அமர்வில் நீங்கள் செய்தவை' : 'Finished in Your Last Login'}
                </div>

                <div className="grid gap-2.5 sm:grid-cols-1">
                  {/* Graded Assessment Card */}
                  {assessmentFinished && (
                    <div className="group relative flex items-center justify-between gap-3 rounded-2xl border border-emerald-200 bg-gradient-to-r from-emerald-50/70 via-emerald-50/30 to-white p-3.5 sm:p-4 shadow-2xs">
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-100 text-emerald-700">
                          <Trophy className="h-5 w-5" />
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5">
                            <span className="rounded bg-emerald-100 px-1.5 py-0.5 text-[10px] font-bold text-emerald-800 uppercase tracking-wider">
                              {isTamil ? 'மதிப்பீட்டுத் தேர்வு' : 'Graded Test'}
                            </span>
                            <span className="flex items-center gap-0.5 text-[11px] font-semibold text-emerald-700">
                              <CheckCircle2 className="h-3 w-3" />
                              {isTamil ? 'முடிந்தது' : 'Completed'}
                            </span>
                          </div>
                          <div className="truncate font-bold text-navy-900 text-sm sm:text-base mt-0.5">
                            {isTamil && assessmentFinished.title_ta
                              ? assessmentFinished.title_ta
                              : assessmentFinished.title}
                          </div>
                        </div>
                      </div>

                      {assessmentFinished.score !== null &&
                        assessmentFinished.total !== null && (
                          <div className="text-right shrink-0">
                            <div className="text-base font-extrabold text-navy-950 tabular-nums">
                              {assessmentFinished.score}/{assessmentFinished.total}
                            </div>
                            <div className="text-xs font-semibold text-emerald-700">
                              {assessmentFinished.percentage}%
                            </div>
                          </div>
                        )}
                    </div>
                  )}

                  {/* Practice Set Card */}
                  {practiceFinished && (
                    <div className="group relative flex items-center justify-between gap-3 rounded-2xl border border-sky-200 bg-gradient-to-r from-sky-50/70 via-sky-50/30 to-white p-3.5 sm:p-4 shadow-2xs">
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-100 text-sky-700">
                          <BookOpen className="h-5 w-5" />
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5">
                            <span className="rounded bg-sky-100 px-1.5 py-0.5 text-[10px] font-bold text-sky-800 uppercase tracking-wider">
                              {isTamil ? 'பயிற்சித் தொகுப்பு' : 'Practice Set'}
                            </span>
                            <span className="flex items-center gap-0.5 text-[11px] font-semibold text-sky-700">
                              <CheckCircle2 className="h-3 w-3" />
                              {isTamil ? 'முடிந்தது' : 'Completed'}
                            </span>
                          </div>
                          <div className="truncate font-bold text-navy-900 text-sm sm:text-base mt-0.5">
                            {isTamil && practiceFinished.title_ta
                              ? practiceFinished.title_ta
                              : practiceFinished.title}
                          </div>
                        </div>
                      </div>

                      <div className="text-right shrink-0">
                        <div className="text-base font-extrabold text-navy-950 tabular-nums">
                          {practiceFinished.correctCount}/{practiceFinished.totalQuestions}
                        </div>
                        <div className="text-xs font-semibold text-sky-700">
                          {practiceFinished.percentage}% accuracy
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Practice in Progress Card */}
                  {practiceInProgress && (
                    <div className="group relative flex items-center justify-between gap-3 rounded-2xl border border-sky-300 bg-gradient-to-r from-sky-50 via-sky-50/50 to-white p-3.5 sm:p-4 shadow-2xs">
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-100 text-sky-700">
                          <BookOpen className="h-5 w-5 animate-pulse" />
                        </div>
                        <div className="min-w-0">
                          <div className="flex items-center gap-1.5 flex-wrap">
                            <span className="rounded bg-sky-100 px-1.5 py-0.5 text-[10px] font-bold text-sky-800 uppercase tracking-wider">
                              {isTamil ? 'பயிற்சி தொடர்கிறது' : 'Practice In Progress'}
                            </span>
                            <span className="flex items-center gap-1 rounded bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-800 border border-amber-200">
                              <Clock className="h-3 w-3 text-amber-600" />
                              {isTamil
                                ? `வினா ${(practiceInProgress.lastQuestionIndex ?? practiceInProgress.answeredCount ?? 0) + 1}-ல் தொடர்கிறது`
                                : `Left at Question ${(practiceInProgress.lastQuestionIndex ?? practiceInProgress.answeredCount ?? 0) + 1}`}
                            </span>
                          </div>
                          <div className="truncate font-bold text-navy-900 text-sm sm:text-base mt-1">
                            {isTamil && practiceInProgress.title_ta
                              ? practiceInProgress.title_ta
                              : practiceInProgress.title}
                          </div>
                        </div>
                      </div>

                      <div className="text-right shrink-0">
                        <div className="text-base font-extrabold text-navy-950 tabular-nums">
                          {practiceInProgress.answeredCount}/{practiceInProgress.totalQuestions}
                        </div>
                        <div className="text-xs font-semibold text-sky-700">
                          {isTamil ? 'வினாக்கள் செய்யப்பட்டன' : 'answered so far'}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Assessment in Progress Alert Card */}
                  {assessmentInProgress && (
                    <div className="group relative flex items-center justify-between gap-3 rounded-2xl border border-amber-300 bg-gradient-to-r from-amber-50 to-orange-50/30 p-3.5 sm:p-4 shadow-2xs">
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-100 text-amber-700">
                          <Clock className="h-5 w-5 animate-pulse" />
                        </div>
                        <div className="min-w-0">
                          <span className="rounded bg-amber-100 px-1.5 py-0.5 text-[10px] font-bold text-amber-800 uppercase tracking-wider">
                            {isTamil ? 'நடைபெறும் தேர்வு' : 'Test In Progress'}
                          </span>
                          <div className="truncate font-bold text-navy-900 text-sm sm:text-base mt-0.5">
                            {isTamil && assessmentInProgress.title_ta
                              ? assessmentInProgress.title_ta
                              : assessmentInProgress.title}
                          </div>
                        </div>
                      </div>
                      <span className="shrink-0 text-xs font-semibold text-amber-800 bg-amber-100 px-2.5 py-1 rounded-lg">
                        {isTamil ? 'தொடரலாம்' : 'Ongoing'}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              {/* Next Step / Recommended Action Box */}
              {nextActionItem && (
                <div className="mt-5 rounded-2xl border border-navy-100 bg-navy-50/80 p-4 sm:p-4.5">
                  <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-navy-700">
                    <Play className="h-3.5 w-3.5 text-sky-600 fill-sky-600" />
                    <span>{isTamil ? 'அடுத்து தொடர வேண்டியது' : 'Recommended Next Step'}</span>
                  </div>
                  <div className="mt-1 flex items-center justify-between gap-2">
                    <div className="min-w-0">
                      <div className="truncate text-base font-bold text-navy-950">
                        {isTamil && nextActionItem.title_ta
                          ? nextActionItem.title_ta
                          : nextActionItem.title}
                      </div>
                      {nextActionItem.courseTitle && (
                        <div className="truncate text-xs text-navy-500">
                          {nextActionItem.courseTitle}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="mt-6 flex flex-col-reverse gap-2.5 sm:flex-row sm:justify-end">
                <Button
                  variant="secondary"
                  onClick={handleGoToDashboard}
                  className="w-full sm:w-auto"
                >
                  {isTamil ? 'முகப்புப் பக்கம்' : 'Go to Dashboard'}
                </Button>

                <Button
                  variant="primary"
                  onClick={handleResumeClick}
                  className="w-full sm:w-auto bg-gradient-to-r from-navy-900 via-sky-900 to-sky-700 hover:from-navy-800 hover:to-sky-800 text-white shadow-md font-bold px-6"
                  icon={<ArrowRight className="h-4 w-4" />}
                >
                  {isTamil ? 'தொடர்ந்து பயில்க' : 'Resume Learning'}
                </Button>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
