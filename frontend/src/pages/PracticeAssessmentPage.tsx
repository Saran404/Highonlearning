import { ChevronLeft, RotateCcw } from 'lucide-react';
import { useCallback, useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { Link, useParams } from 'react-router-dom';
import { assessmentsApi } from '../api/assessments';
import { toApiError } from '../api/client';
import { PracticeFeedback, practiceApi } from '../api/practice';
import OptionButton, { OptionState } from '../components/assessment/OptionButton';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import EmptyState from '../components/common/EmptyState';
import ProgressBar from '../components/common/ProgressBar';
import { PageSkeleton } from '../components/common/Skeleton';
import { useAuthStore } from '../store/authStore';
import type { AssessmentItem, Question } from '../types';
import {
  clearPracticeProgress,
  getPracticeProgress,
  recordCourseVisited,
  recordPracticeActivity,
  savePracticeProgress,
} from '../utils/sessionTracker';

export default function PracticeAssessmentPage() {
  const { id } = useParams();
  const assessmentId = Number(id);
  const user = useAuthStore((s) => s.user);
  const [assessment, setAssessment] = useState<AssessmentItem | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [feedback, setFeedback] = useState<Record<number, PracticeFeedback>>({});
  const [index, setIndex] = useState(0);
  const [done, setDone] = useState(false);
  const [loading, setLoading] = useState(true);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<'en' | 'ta'>(() => {
    const saved = localStorage.getItem('exampro_lang');
    return saved === 'ta' ? 'ta' : 'en';
  });

  const handleLanguageChange = (lang: 'en' | 'ta') => {
    setLanguage(lang);
    localStorage.setItem('exampro_lang', lang);
  };

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [a, qs] = await Promise.all([assessmentsApi.get(assessmentId), practiceApi.questions(assessmentId)]);
      setAssessment(a);
      setQuestions(qs);

      // Check if user has saved in-progress practice for this assessment
      const saved = user?.id ? getPracticeProgress(user.id, assessmentId) : null;
      if (saved && !saved.done && Object.keys(saved.feedback || {}).length > 0) {
        setFeedback(saved.feedback);
        const resumeIndex = Math.min(Math.max(0, saved.currentIndex), qs.length - 1);
        setIndex(resumeIndex);
        setDone(false);
      } else {
        setFeedback({});
        setIndex(0);
        setDone(false);
      }

      if (user?.id && a) {
        recordCourseVisited(user.id, a.course_slug, a.course_title);
      }
    } catch (e) {
      setError(toApiError(e).message);
    } finally {
      setLoading(false);
    }
  }, [assessmentId, user?.id]);

  useEffect(() => {
    void load();
  }, [load]);

  const restart = async () => {
    if (user?.id) {
      clearPracticeProgress(user.id, assessmentId);
    }
    try {
      await practiceApi.reset(assessmentId);
    } catch {
      /* stateless on the server - safe to ignore */
    }
    await load();
  };

  if (loading) return <PageSkeleton />;
  if (error || !assessment) return <Card><EmptyState title="Couldn't open this practice set" description={error ?? undefined} action={<Link to="/courses" className="text-sky-700 underline">Back to courses</Link>} /></Card>;
  if (questions.length === 0) return <Card><EmptyState title="No questions yet" description="This practice set is empty." /></Card>;

  const back = <Link to={`/courses/${assessment.course_slug}`} className="inline-flex items-center gap-1 text-sm text-sky-700 hover:underline"><ChevronLeft className="h-4 w-4" />{assessment.course_title}</Link>;

  if (done) {
    const correct = Object.values(feedback).filter((f) => f.correct).length;
    const pct = Math.round((100 * correct) / questions.length);
    return (
      <div className="mx-auto max-w-2xl space-y-5">
        {back}
        <Card>
          <div className="py-4 text-center">
            <p className="text-5xl font-semibold tabular-nums">{correct}<span className="text-2xl text-navy-400">/{questions.length}</span></p>
            <p className="mt-2 text-navy-600">
              {language === 'ta'
                ? pct >= 80
                  ? 'மிகச் சிறப்பு! நீங்கள் தயாராக இருக்கும்போது மதிப்பீட்டுத் தேர்வை எழுதுங்கள்.'
                  : pct >= 50
                  ? 'நல்ல முன்னேற்றம். தவறவிட்ட கணக்குகளை மீண்டும் ஒருமுறை பயிற்சி செய்யுங்கள்.'
                  : 'தொடர்ந்து பயிற்சி செய்யுங்கள் — மீண்டும் இத்தொகுப்பைச் செய்து விளக்கங்களை வாசியுங்கள்.'
                : pct >= 80
                ? 'Very strong. Try the graded test when you feel ready.'
                : pct >= 50
                ? 'Good progress. Go through the ones you missed once more.'
                : 'Keep going — repeat the set and read each explanation.'}
            </p>
            <div className="mt-5 flex flex-col justify-center gap-2 sm:flex-row">
              <Button onClick={restart} icon={<RotateCcw className="h-4 w-4" />}>
                {language === 'ta' ? 'மீண்டும் பயிற்சி செய்' : 'Practise again'}
              </Button>
              <Link to={`/courses/${assessment.course_slug}`}>
                <Button variant="secondary" fullWidth>
                  {language === 'ta' ? 'பாடத்திற்குத் திரும்பு' : 'Back to course'}
                </Button>
              </Link>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  const q = questions[index];
  const fb = feedback[q.id];
  const stateFor = (i: number): OptionState => {
    if (!fb) return 'idle';
    if (i === fb.correct_index) return fb.selected_index === i ? 'correct' : 'missed';
    return i === fb.selected_index ? 'wrong' : 'idle';
  };

  const choose = async (i: number) => {
    if (fb || checking) return;
    setChecking(true);
    try {
      const res = await practiceApi.answer({ question_id: q.id, selected_index: i });
      const updatedFb = { ...feedback, [q.id]: res };
      setFeedback(updatedFb);

      if (user?.id && assessment) {
        const correctCount = Object.values(updatedFb).filter((f) => f.correct).length;
        const pct = Math.round((100 * correctCount) / questions.length);

        savePracticeProgress(user.id, assessment.id, {
          currentIndex: index,
          feedback: updatedFb,
          done: false,
          totalQuestions: questions.length,
        });

        recordPracticeActivity(user.id, {
          assessmentId: assessment.id,
          title: assessment.title,
          title_ta: assessment.title_ta,
          courseSlug: assessment.course_slug,
          courseTitle: assessment.course_title,
          totalQuestions: questions.length,
          answeredCount: Object.keys(updatedFb).length,
          correctCount,
          percentage: pct,
          lastQuestionIndex: index,
          completed: false,
        });
      }
    } catch (e) {
      toast.error(toApiError(e).message);
    } finally {
      setChecking(false);
    }
  };

  const goToIndex = (newIndex: number) => {
    setIndex(newIndex);
    if (user?.id && assessment) {
      savePracticeProgress(user.id, assessment.id, {
        currentIndex: newIndex,
        feedback,
        done: false,
        totalQuestions: questions.length,
      });

      const correctCount = Object.values(feedback).filter((f) => f.correct).length;
      const pct = questions.length ? Math.round((100 * correctCount) / questions.length) : 0;
      recordPracticeActivity(user.id, {
        assessmentId: assessment.id,
        title: assessment.title,
        title_ta: assessment.title_ta,
        courseSlug: assessment.course_slug,
        courseTitle: assessment.course_title,
        totalQuestions: questions.length,
        answeredCount: Object.keys(feedback).length,
        correctCount,
        percentage: pct,
        lastQuestionIndex: newIndex,
        completed: false,
      });
    }
  };

  const handleFinish = () => {
    setDone(true);
    if (user?.id && assessment) {
      const correctCount = Object.values(feedback).filter((f) => f.correct).length;
      const pct = Math.round((100 * correctCount) / questions.length);

      savePracticeProgress(user.id, assessment.id, {
        currentIndex: index,
        feedback,
        done: true,
        totalQuestions: questions.length,
      });

      recordPracticeActivity(user.id, {
        assessmentId: assessment.id,
        title: assessment.title,
        title_ta: assessment.title_ta,
        courseSlug: assessment.course_slug,
        courseTitle: assessment.course_title,
        totalQuestions: questions.length,
        answeredCount: Object.keys(feedback).length,
        correctCount,
        percentage: pct,
        lastQuestionIndex: index,
        completed: true,
      });
    }
  };

  const isLast = index === questions.length - 1;

  const displayQuestionText = language === 'ta' && q.text_ta ? q.text_ta : q.text;
  const displayOptions = language === 'ta' && q.options_ta && q.options_ta.length === q.options.length ? q.options_ta : q.options;
  const displayTitle = language === 'ta' && assessment.title_ta ? assessment.title_ta : assessment.title;
  const displayExplanation = fb ? (language === 'ta' && fb.explanation_ta ? fb.explanation_ta : fb.explanation) : '';

  return (
    <div className="mx-auto max-w-2xl space-y-4">
      <div className="flex items-center justify-between">
        {back}
        <div className="flex items-center gap-2">
          {Object.keys(feedback).length > 0 && (
            <button
              type="button"
              onClick={restart}
              className="flex items-center gap-1 text-xs text-navy-500 hover:text-navy-800 rounded px-2 py-1 hover:bg-navy-100/60 transition-colors"
              title={language === 'ta' ? 'மீண்டும் தொடக்கத்திலிருந்து செய்' : 'Restart from question 1'}
            >
              <RotateCcw className="h-3.5 w-3.5 text-navy-400" />
              <span className="hidden sm:inline">{language === 'ta' ? 'மீளமை' : 'Restart'}</span>
            </button>
          )}

          {/* Language Switcher */}
          <div className="flex items-center gap-1 rounded-lg bg-navy-50 p-1 border border-line text-xs font-semibold">
            <button
              type="button"
              onClick={() => handleLanguageChange('en')}
              className={`rounded px-2.5 py-1 transition-all ${
                language === 'en' ? 'bg-sky-600 text-white shadow-xs' : 'text-navy-600 hover:bg-navy-200/50'
              }`}
            >
              🇬🇧 EN
            </button>
            <button
              type="button"
              onClick={() => handleLanguageChange('ta')}
              className={`rounded px-2.5 py-1 transition-all ${
                language === 'ta' ? 'bg-sky-600 text-white shadow-xs' : 'text-navy-600 hover:bg-navy-200/50'
              }`}
            >
              🇮🇳 தமிழ்
            </button>
          </div>
        </div>
      </div>

      <div>
        <div className="flex items-center gap-2 flex-wrap">
          <h1 className="text-xl font-bold text-navy">{displayTitle}</h1>
          {Object.keys(feedback).length > 0 && (
            <span className="rounded-full bg-sky-50 px-2.5 py-0.5 text-[11px] font-semibold text-sky-700 border border-sky-200">
              {language === 'ta'
                ? `${Object.keys(feedback).length} வினாக்கள் செய்யப்பட்டன`
                : `${Object.keys(feedback).length} answered so far`}
            </span>
          )}
        </div>
        <p className="text-xs text-navy-500 mt-0.5">
          {language === 'ta'
            ? 'பயிற்சி முறை · நேர வரம்பில்லை · உடனடித் தீர்வுகள்'
            : 'Practice mode · no timer · instant feedback'}
        </p>
        <ProgressBar value={(100 * (index + (fb ? 1 : 0))) / questions.length} className="mt-3" label="Practice progress" />
      </div>

      <article className="panel p-4 sm:p-6">
        <div className="mb-3 flex items-center justify-between text-sm text-navy-500">
          <span>
            {language === 'ta'
              ? `வினா ${index + 1} / ${questions.length}`
              : `Question ${index + 1} of ${questions.length}`}
          </span>
          {q.text_ta && (
            <button
              type="button"
              onClick={() => handleLanguageChange(language === 'en' ? 'ta' : 'en')}
              className="text-xs text-sky-700 hover:underline font-medium"
            >
              {language === 'en' ? 'தமிழில் காண்க' : 'View in English'}
            </button>
          )}
        </div>
        <h2 className="paper mb-5 font-normal tracking-normal text-navy-900 leading-relaxed">{displayQuestionText}</h2>
        <div className="space-y-2.5">
          {displayOptions.map((opt, i) => (
            <OptionButton
              key={i}
              letter={String.fromCharCode(65 + i)}
              text={opt}
              state={stateFor(i)}
              disabled={Boolean(fb) || checking}
              onClick={() => void choose(i)}
            />
          ))}
        </div>
        {fb && (
          <div className={`mt-4 rounded-lg px-4 py-3 text-sm ${fb.correct ? 'bg-mint text-mint-700' : 'bg-danger text-danger-700'}`} role="status">
            <p className="font-semibold">
              {fb.correct
                ? (language === 'ta' ? 'சரியான விடை!' : 'Correct!')
                : (language === 'ta' ? `தவறு — சரியான விடை ${String.fromCharCode(65 + fb.correct_index)}.` : `Not quite — the answer is ${String.fromCharCode(65 + fb.correct_index)}.`)}
            </p>
            {displayExplanation && <p className="mt-1.5 text-navy-800 leading-relaxed">{displayExplanation}</p>}
          </div>
        )}
      </article>

      <div className="flex justify-between">
        <Button variant="secondary" onClick={() => goToIndex(index - 1)} disabled={index === 0} icon={<ChevronLeft className="h-4 w-4" />}>
          {language === 'ta' ? 'முந்தையது' : 'Previous'}
        </Button>
        {isLast ? (
          <Button onClick={handleFinish} disabled={!fb}>
            {language === 'ta' ? 'முடிக்க' : 'Finish'}
          </Button>
        ) : (
          <Button onClick={() => goToIndex(index + 1)}>
            {fb ? (language === 'ta' ? 'அடுத்தது' : 'Next') : (language === 'ta' ? 'தவிர்க்க' : 'Skip')}
          </Button>
        )}
      </div>
    </div>
  );
}
