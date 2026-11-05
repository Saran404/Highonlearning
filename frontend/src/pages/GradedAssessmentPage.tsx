import { AlertTriangle, ChevronLeft, ChevronRight, Flag, Grid3x3, ShieldAlert, Maximize, UserX } from 'lucide-react';
import { useCallback, useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { attemptsApi } from '../api/attempts';
import { toApiError } from '../api/client';
import CameraPreview from '../components/assessment/CameraPreview';
import DurationExtensionModal from '../components/assessment/DurationExtensionModal';
import MalpracticeModal from '../components/assessment/MalpracticeModal';
import QuestionCard from '../components/assessment/QuestionCard';
import QuestionPalette from '../components/assessment/QuestionPalette';
import TimerPill from '../components/assessment/TimerPill';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import ConfirmationModal from '../components/common/ConfirmationModal';
import EmptyState from '../components/common/EmptyState';
import { PageSkeleton } from '../components/common/Skeleton';
import { useLockdown } from '../hooks/useLockdown';
import { useProctoring } from '../hooks/useProctoring';
import { useTimer } from '../hooks/useTimer';
import { useAttemptStore } from '../store/attemptStore';
import { useAuthStore } from '../store/authStore';
import type { MalpracticeType } from '../types';
import { EXTENSION_DECISION_SECONDS } from '../utils/constants';
import { recordAssessmentActivity } from '../utils/sessionTracker';

const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

/**
 * The proctored exam screen. Everything time-critical is server-driven: the deadline comes from the
 * server, answers autosave on every tap, and the final submit resends every answer as a safety net.
 */
export default function GradedAssessmentPage() {
  const { attemptId: idParam } = useParams();
  const attemptId = Number(idParam);
  const navigate = useNavigate();

  const s = useAttemptStore();
  const [ready, setReady] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [finished, setFinished] = useState(false);
  const finishedRef = useRef(false);
  const [confirmSubmit, setConfirmSubmit] = useState(false);
  const [warningOpen, setWarningOpen] = useState(false);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [showExtension, setShowExtension] = useState(false);
  const [extending, setExtending] = useState(false);
  const [decisionLeft, setDecisionLeft] = useState(EXTENSION_DECISION_SECONDS);
  const [language, setLanguage] = useState<'en' | 'ta'>(() => {
    const saved = localStorage.getItem('exampro_lang');
    return saved === 'ta' ? 'ta' : 'en';
  });

  const handleLanguageChange = (lang: 'en' | 'ta') => {
    setLanguage(lang);
    localStorage.setItem('exampro_lang', lang);
  };

  /* ------------------------------------------------------------ load / resume */
  useEffect(() => {
    let cancelled = false;
    attemptsApi
      .get(attemptId)
      .then((state) => {
        if (cancelled) return;
        if (state.status !== 'IN_PROGRESS') {
          navigate(`/results/${attemptId}`, { replace: true });
          return;
        }
        useAttemptStore.getState().init(state);
        setReady(true);
        const userId = useAuthStore.getState().user?.id;
        if (userId) {
          recordAssessmentActivity(userId, {
            attemptId,
            assessmentId: state.assessment_id,
            title: state.assessment_title,
            status: 'IN_PROGRESS',
            completed: false,
          });
        }
      })
      .catch((e) => !cancelled && setLoadError(toApiError(e).message));
    return () => {
      cancelled = true;
      useAttemptStore.getState().reset();
    };
  }, [attemptId, navigate]);

  /* ------------------------------------------------------------ proctoring */
  const proctorOn = ready && s.proctoring && !finished;
  const proctor = useProctoring({ enabled: proctorOn, attemptId });

  const goToResult = useCallback(async () => {
    if (document.fullscreenElement) await document.exitFullscreen().catch(() => undefined);
    navigate(`/results/${attemptId}`, { replace: true });
  }, [attemptId, navigate]);

  /* ------------------------------------------------------------ lockdown + strikes */
  const handleViolation = useCallback(
    async (type: MalpracticeType, meta?: Record<string, unknown>) => {
      if (finishedRef.current) return;
      void proctor.capture('MALPRACTICE');
      try {
        const res = await attemptsApi.malpractice(attemptId, { type, metadata: meta });
        useAttemptStore.getState().setViolations(res.malpractice_count, type);
        if (res.should_terminate) {
          finishedRef.current = true;
          setFinished(true);
          toast.error('Too many warnings. Your test was submitted.');
          await goToResult();
          return;
        }
        setWarningOpen(true);
      } catch (e) {
        if (toApiError(e).code === 'ATTEMPT_NOT_ACTIVE') {
          finishedRef.current = true;
          setFinished(true);
          await goToResult();
        }
      }
    },
    [attemptId, proctor, goToResult],
  );

  const lockdownOn = ready && s.lockdown && !submitting && !finished;
  const { isFullscreen, fullscreenSupported, enterFullscreen } = useLockdown({ enabled: lockdownOn, onViolation: handleViolation });

  /* ------------------------------------------------------------ autosave */
  const persist = useCallback(
    async (questionId: number) => {
      const a = useAttemptStore.getState().answers[questionId];
      if (!a) return;
      try {
        await attemptsApi.answer(attemptId, { question_id: questionId, selected_index: a.selected, marked_for_review: a.marked });
        useAttemptStore.getState().markClean(questionId);
      } catch {
        /* stays in the dirty list; retried below and sent again on submit */
      }
    },
    [attemptId],
  );

  useEffect(() => {
    if (!ready) return;
    const id = window.setInterval(() => {
      useAttemptStore.getState().dirty.forEach((qid) => void persist(qid));
    }, 8000);
    return () => window.clearInterval(id);
  }, [ready, persist]);

  /* ------------------------------------------------------------ submit */
  const doSubmit = useCallback(
    async (auto: boolean) => {
      if (finishedRef.current) return;
      finishedRef.current = true;
      setSubmitting(true);
      setConfirmSubmit(false);
      setShowExtension(false);

      if (useAttemptStore.getState().proctoring) await Promise.race([proctor.capture('END'), sleep(2500)]);

      const st = useAttemptStore.getState();
      const answers = st.questions.map((q) => ({ question_id: q.id, selected_index: st.answers[q.id]?.selected ?? null }));
      for (let attempt = 1; attempt <= 5; attempt += 1) {
        try {
          await attemptsApi.submit(attemptId, { answers, auto });
          setFinished(true);
          toast.success(auto ? "Time's up — your test was submitted." : 'Test submitted.');
          await goToResult();
          return;
        } catch (e) {
          const err = toApiError(e);
          const retryable = err.status === 0 || err.status >= 500;
          if (!retryable || attempt === 5) {
            finishedRef.current = false;
            setSubmitting(false);
            toast.error(err.message || 'Could not submit. Please try again.');
            return;
          }
          await sleep(2000);
        }
      }
    },
    [attemptId, proctor, goToResult],
  );

  /* ------------------------------------------------------------ timer + extension */
  const canExtend = !s.extended && s.chosenMinutes < s.defaultMinutes;
  const { remaining, isLow, isCritical } = useTimer({
    deadlineMs: s.deadlineMs,
    offsetMs: s.offsetMs,
    canExtend,
    onExtensionAvailable: () => {
      setDecisionLeft(EXTENSION_DECISION_SECONDS);
      setShowExtension(true);
    },
    onExpire: () => void doSubmit(true),
  });

  useEffect(() => {
    if (!showExtension) return;
    const id = window.setInterval(() => setDecisionLeft((v) => v - 1), 1000);
    return () => window.clearInterval(id);
  }, [showExtension]);

  useEffect(() => {
    if (showExtension && decisionLeft <= 0) void doSubmit(true);
  }, [showExtension, decisionLeft, doSubmit]);

  const onExtend = async () => {
    setExtending(true);
    try {
      const res = await attemptsApi.extend(attemptId);
      useAttemptStore.getState().setDeadline(res.deadline_at);
      useAttemptStore.getState().setExtended();
      setShowExtension(false);
      toast.success('Extra time added.');
    } catch (e) {
      toast.error(toApiError(e).message);
    } finally {
      setExtending(false);
    }
  };

  /* ------------------------------------------------------------ render */
  if (loadError) {
    return (
      <div className="mx-auto max-w-lg p-6">
        <Card><EmptyState title="Couldn't open this test" description={loadError} action={<Link to="/dashboard" className="text-sky-700 underline">Back to dashboard</Link>} /></Card>
      </div>
    );
  }
  if (!ready || s.questions.length === 0) return <div className="mx-auto max-w-3xl p-6"><PageSkeleton /></div>;

  const q = s.questions[s.currentIndex];
  const local = s.answers[q.id] ?? { selected: null, marked: false };
  const total = s.questions.length;
  const answered = s.questions.filter((x) => s.answers[x.id]?.selected != null).length;
  const marked = s.questions.filter((x) => s.answers[x.id]?.marked).length;
  const isLast = s.currentIndex === total - 1;
  const needsFullscreen = s.lockdown && fullscreenSupported && !isFullscreen && !finished && !submitting;

  const onSelect = (idx: number) => {
    s.select(q.id, idx);
    void persist(q.id);
  };
  const onClear = () => {
    s.select(q.id, null);
    void persist(q.id);
  };
  const onMark = () => {
    s.toggleMark(q.id);
    void persist(q.id);
  };

  return (
    <div className="no-select flex min-h-screen flex-col bg-canvas">
      <header className="sticky top-0 z-30 bg-navy text-white">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-3 px-3 sm:px-4">
          <div className="min-w-0">
            <h1 className="truncate text-sm font-semibold sm:text-base">{s.title}</h1>
            <p className="text-xs text-navy-200">{answered}/{total} answered</p>
          </div>
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Exam Language Selector */}
            <div className="flex items-center rounded-lg bg-white/10 p-0.5 text-xs font-semibold">
              <button
                type="button"
                onClick={() => handleLanguageChange('en')}
                className={`rounded px-2 py-1 transition-all ${
                  language === 'en' ? 'bg-sky-500 text-white shadow-xs' : 'text-white/70 hover:text-white'
                }`}
              >
                EN
              </button>
              <button
                type="button"
                onClick={() => handleLanguageChange('ta')}
                className={`rounded px-2 py-1 transition-all ${
                  language === 'ta' ? 'bg-sky-500 text-white shadow-xs' : 'text-white/70 hover:text-white'
                }`}
              >
                தமிழ்
              </button>
            </div>

            <span className={`hidden items-center gap-1 rounded-full px-2.5 py-1.5 text-xs font-medium sm:inline-flex ${s.violations ? 'bg-danger text-danger-700' : 'bg-white/10'}`} title="Warnings used">
              <ShieldAlert className="h-3.5 w-3.5" /> {s.violations}/{s.maxViolations}
            </span>
            <TimerPill remaining={remaining} low={isLow} critical={isCritical} />
            {s.proctoring && (
              <CameraPreview
                webcamRef={proctor.webcamRef}
                ready={proctor.cameraReady}
                error={proctor.cameraError}
                personVisible={proctor.personVisible}
                onUserMedia={proctor.onUserMedia}
                onUserMediaError={proctor.onUserMediaError}
              />
            )}
            <Button size="sm" variant="secondary" className="hidden sm:inline-flex" onClick={() => setConfirmSubmit(true)} disabled={submitting}>Submit</Button>
          </div>
        </div>
      </header>

      {s.proctoring && proctor.cameraError && (
        <div className="flex items-center justify-center gap-2 bg-cream px-4 py-2 text-center text-sm text-cream-700" role="alert">
          <AlertTriangle className="h-4 w-4 shrink-0" /> {proctor.cameraError} Reconnect your camera so snapshots can be captured.
        </div>
      )}

      {/* Real-time Camera Presence Warning - Both Web and Mobile */}
      {s.proctoring && proctor.cameraReady && !proctor.personVisible && (
        <div
          className="sticky top-16 z-30 flex items-center justify-between gap-3 border-b-2 border-danger-700 bg-gradient-to-r from-danger-600 via-rose-600 to-danger-700 px-3 py-2.5 text-white shadow-xl animate-in slide-in-from-top duration-200 sm:px-6 sm:py-3.5"
          role="alert"
        >
          <div className="flex items-center gap-2.5 sm:gap-3.5">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-white/20 ring-4 ring-white/10 animate-pulse">
              <UserX className="h-5 w-5 text-white" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2 font-bold text-xs sm:text-sm tracking-wide text-white">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-yellow-300 opacity-75" />
                  <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-yellow-400" />
                </span>
                <span>
                  {language === 'ta'
                    ? 'எச்சரிக்கை: கேமராவில் முகம் தெரியவில்லை!'
                    : 'WARNING: PERSON NOT VISIBLE IN CAMERA!'}
                </span>
              </div>
              <p className="mt-0.5 text-xs text-white/95 leading-snug">
                {language === 'ta'
                  ? 'உங்கள் முகம் முழுமையாகத் தெரியும்படி கேமராவின் முன் நேராக அமரவும். இல்லையெனில் தேர்வு ரத்தாகலாம்.'
                  : 'Please position yourself directly in front of the camera. Continuous visual presence is required.'}
              </p>
            </div>
          </div>
          <div className="hidden shrink-0 items-center gap-1.5 rounded-full bg-black/30 px-3 py-1.5 text-xs font-semibold text-white/90 sm:flex">
            <span className="h-2 w-2 rounded-full bg-danger-400 animate-ping" />
            <span>Camera Alert</span>
          </div>
        </div>
      )}

      {/* Mobile-specific floating warning pill when scrolling */}
      {s.proctoring && proctor.cameraReady && !proctor.personVisible && (
        <div className="fixed bottom-14 inset-x-3 z-30 sm:hidden animate-in fade-in slide-in-from-bottom-2 duration-150">
          <div className="flex items-center gap-2 rounded-xl bg-danger-800/95 px-3 py-2 text-white shadow-2xl backdrop-blur-xs ring-2 ring-danger-400/80">
            <UserX className="h-4 w-4 shrink-0 text-yellow-300 animate-pulse" />
            <span className="text-xs font-bold truncate">
              {language === 'ta' ? 'கேமராவில் முகம் தெரியவில்லை!' : 'Face not visible in camera!'}
            </span>
            <span className="ml-auto text-[10px] bg-white/20 px-2 py-0.5 rounded-full font-semibold shrink-0">
              {language === 'ta' ? 'கேமராவைப் பார்க்கவும்' : 'Look at camera'}
            </span>
          </div>
        </div>
      )}

      <div className="mx-auto flex w-full max-w-6xl flex-1 gap-5 px-3 pb-28 pt-4 sm:px-4">
        <main className="min-w-0 flex-1">
          <QuestionCard
            question={q}
            index={s.currentIndex}
            total={total}
            selected={local.selected}
            marked={local.marked}
            onSelect={onSelect}
            disabled={submitting}
            language={language}
            onToggleLanguage={() => handleLanguageChange(language === 'en' ? 'ta' : 'en')}
          />
        </main>
        <QuestionPalette questions={s.questions} answers={s.answers} current={s.currentIndex} onGo={s.goTo} open={paletteOpen} onClose={() => setPaletteOpen(false)} />
      </div>

      <footer className="fixed inset-x-0 bottom-0 z-30 border-t border-line bg-white pb-[env(safe-area-inset-bottom)]">
        <div className="mx-auto flex max-w-6xl items-center gap-2 px-3 py-2.5 sm:px-4">
          <Button variant="secondary" size="sm" className="lg:hidden" onClick={() => setPaletteOpen(true)} icon={<Grid3x3 className="h-4 w-4" />} aria-label="Open question palette">{marked ? `${marked} ⚑` : ''}</Button>
          <Button variant="secondary" size="sm" onClick={onMark} icon={<Flag className="h-4 w-4" />}>{local.marked ? 'Unmark' : 'Mark'}<span className="hidden sm:inline">&nbsp;for review</span></Button>
          <Button variant="ghost" size="sm" onClick={onClear} disabled={local.selected == null}>Clear</Button>
          <div className="ml-auto flex items-center gap-2">
            <Button variant="secondary" size="sm" onClick={() => s.goTo(s.currentIndex - 1)} disabled={s.currentIndex === 0} icon={<ChevronLeft className="h-4 w-4" />} aria-label="Previous question" />
            {isLast ? (
              <Button size="sm" onClick={() => setConfirmSubmit(true)} disabled={submitting}>Submit test</Button>
            ) : (
              <Button size="sm" onClick={() => s.goTo(s.currentIndex + 1)} icon={<ChevronRight className="h-4 w-4" />}>Next</Button>
            )}
          </div>
        </div>
      </footer>

      {/* Fullscreen gate: shown after a refresh or when fullscreen was left */}
      {needsFullscreen && !warningOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-navy px-6 text-center text-white" role="alertdialog" aria-labelledby="fs-title">
          <div className="max-w-sm">
            <Maximize className="mx-auto h-10 w-10 text-sky-200" />
            <h2 id="fs-title" className="mt-3 text-xl">Return to fullscreen</h2>
            <p className="mt-2 text-sm text-navy-200">This test must be taken in fullscreen. Your timer is still running.</p>
            <Button className="mt-5" size="lg" onClick={() => void enterFullscreen()}>Continue test</Button>
          </div>
        </div>
      )}

      <MalpracticeModal
        open={warningOpen && !finished}
        count={s.violations}
        max={s.maxViolations}
        type={s.lastViolation}
        onContinue={() => {
          setWarningOpen(false);
          void enterFullscreen();
        }}
      />

      <DurationExtensionModal
        open={showExtension}
        chosenMinutes={s.chosenMinutes}
        defaultMinutes={s.defaultMinutes}
        secondsLeftToDecide={Math.max(0, decisionLeft)}
        loading={extending}
        onExtend={() => void onExtend()}
        onSubmit={() => void doSubmit(true)}
      />

      <ConfirmationModal open={confirmSubmit} title="Submit your test?" confirmLabel="Submit test" loading={submitting} onCancel={() => setConfirmSubmit(false)} onConfirm={() => void doSubmit(false)}>
        <ul className="space-y-1">
          <li><strong>{answered}</strong> answered</li>
          <li><strong>{total - answered}</strong> not answered{total - answered > 0 && <span className="text-danger-700"> — these score zero</span>}</li>
          {marked > 0 && <li><strong>{marked}</strong> marked for review</li>}
        </ul>
        <p className="mt-3 text-xs text-navy-500">You can't reopen the test after submitting.</p>
      </ConfirmationModal>

      {submitting && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-white/80 text-navy" role="status">
          <p className="rounded-xl bg-white px-5 py-3 text-sm font-medium shadow-panel">Submitting your answers…</p>
        </div>
      )}
    </div>
  );
}
