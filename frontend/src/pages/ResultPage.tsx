import { ChevronLeft, Trophy, BookOpen, Sparkles, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link, Navigate, useParams } from 'react-router-dom';
import { attemptsApi } from '../api/attempts';
import { coursesApi } from '../api/courses';
import { toApiError } from '../api/client';
import { rankApi } from '../api/rank';
import ResultScoreCard from '../components/assessment/ResultScoreCard';
import SolutionReveal from '../components/assessment/SolutionReveal';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import EmptyState from '../components/common/EmptyState';
import Modal from '../components/common/Modal';
import { PageSkeleton } from '../components/common/Skeleton';
import type { LeaderboardResponse, ResultResponse } from '../types';
import { formatDuration } from '../utils/format';
import { useCourseStore } from '../store/courseStore';
import { useAuthStore } from '../store/authStore';
import { recordAssessmentActivity } from '../utils/sessionTracker';

function LeaderboardModal({ assessmentId, open, onClose }: { assessmentId: number; open: boolean; onClose: () => void }) {
  const [data, setData] = useState<LeaderboardResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    if (!open) return;
    setData(null);
    rankApi.leaderboard(assessmentId).then(setData).catch((e) => setError(toApiError(e).message));
  }, [open, assessmentId]);

  return (
    <Modal open={open} onClose={onClose} size="lg" title="Leaderboard">
      {error ? <p className="text-danger-700">{error}</p> : !data ? <PageSkeleton /> : (
        <div>
          <p className="mb-3 text-xs text-navy-500">Top {data.entries.length} of {data.total_participants} · ordered by score, then time</p>
          <table className="w-full text-left text-sm">
            <thead className="border-b border-line text-xs text-navy-500"><tr><th className="py-2 pr-2">#</th><th className="py-2">Name</th><th className="py-2 text-right">Score</th><th className="py-2 text-right">Time</th></tr></thead>
            <tbody className="divide-y divide-line">
              {data.entries.map((e, i) => (
                <tr key={i} className={e.is_me ? 'bg-sky-50 font-semibold' : ''}>
                  <td className="py-2 pr-2 tabular-nums">{e.rank}</td>
                  <td className="py-2">{e.name}{e.is_me && ' (you)'}</td>
                  <td className="py-2 text-right tabular-nums">{e.score}/{e.total}</td>
                  <td className="py-2 text-right tabular-nums">{formatDuration(e.time_taken_sec)}</td>
                </tr>
              ))}
              {data.me && !data.entries.some((e) => e.is_me) && (
                <tr className="bg-sky-50 font-semibold"><td className="py-2 pr-2 tabular-nums">{data.me.rank}</td><td className="py-2">{data.me.name} (you)</td><td className="py-2 text-right tabular-nums">{data.me.score}/{data.me.total}</td><td className="py-2 text-right tabular-nums">{formatDuration(data.me.time_taken_sec)}</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </Modal>
  );
}

export default function ResultPage() {
  const { attemptId } = useParams();
  const id = Number(attemptId);
  const [result, setResult] = useState<ResultResponse | null>(null);
  const [error, setError] = useState<{ code: string; message: string } | null>(null);
  const [board, setBoard] = useState(false);
  const [reflectionState, setReflectionState] = useState<{ submitted: boolean; loading: boolean }>({
    submitted: false,
    loading: true,
  });

  const courses = useCourseStore((s) => s.courses);

  useEffect(() => {
    if (!id || isNaN(id)) {
      setError({ code: 'INVALID_ID', message: 'Invalid or missing attempt ID.' });
      return;
    }
    attemptsApi.result(id).then((r) => {
      setResult(r);
      // Refresh course unlock progression in store and localStorage
      useCourseStore.getState().fetchCourses().catch(() => {});
      const userId = useAuthStore.getState().user?.id;
      if (userId) {
        recordAssessmentActivity(userId, {
          attemptId: id,
          assessmentId: r.attempt.assessment_id,
          title: r.attempt.assessment_title,
          score: r.attempt.score,
          total: r.attempt.total,
          percentage: r.attempt.percentage,
          timeTakenSec: r.attempt.time_taken_sec,
          status: 'COMPLETED',
          completed: true,
        });
      }
    }).catch((e) => setError(toApiError(e)));
  }, [id]);

  const attempt = result?.attempt;

  // Resolve target course slug from attempt or store
  const targetCourseSlug =
    attempt?.course_slug ||
    courses.find((c) => c.id === attempt?.course_id)?.slug ||
    courses.find((c) => {
      const aTitle = attempt?.assessment_title.toLowerCase() || '';
      const cTitle = c.title.toLowerCase();
      return cTitle.includes(aTitle) || aTitle.includes(cTitle);
    })?.slug ||
    courses[0]?.slug;

  useEffect(() => {
    if (!targetCourseSlug) return;
    coursesApi
      .reflection(targetCourseSlug)
      .then((res) => {
        setReflectionState({ submitted: res.submitted, loading: false });
      })
      .catch(() => {
        setReflectionState({ submitted: false, loading: false });
      });
  }, [targetCourseSlug]);

  if (error?.code === 'RESULT_NOT_AVAILABLE') {
    return (
      <div className="mx-auto max-w-xl py-6">
        <Card className="text-center p-6">
          <EmptyState
            title="Result not available yet"
            description="Your test is currently still running or being submitted. Resume the test or return to the dashboard."
            action={
              <div className="flex flex-col sm:flex-row items-center justify-center gap-3 mt-2">
                <Link to={`/attempts/${id}`}><Button variant="primary">Resume Test</Button></Link>
                <Link to="/dashboard"><Button variant="secondary">Back to Dashboard</Button></Link>
              </div>
            }
          />
        </Card>
      </div>
    );
  }
  if (error) return <Card><EmptyState title="Result not available" description={error.message} action={<Link to="/dashboard" className="text-sky-700 underline">Back to dashboard</Link>} /></Card>;
  if (!result || !attempt) return <PageSkeleton />;

  const language = localStorage.getItem('exampro_lang') === 'ta' ? 'ta' : 'en';

  return (
    <div className="mx-auto max-w-3xl space-y-5">
      <Link to="/dashboard" className="inline-flex items-center gap-1 text-sm text-sky-700 hover:underline"><ChevronLeft className="h-4 w-4" />Dashboard</Link>
      <ResultScoreCard attempt={attempt} />
      <div className="rounded-xl border border-cream-300 bg-cream px-4 py-3.5 text-cream-700">{result.motivational_message}</div>

      {/* Featured Call-To-Action: Finish Reflective Activity */}
      {targetCourseSlug && (
        <div className="overflow-hidden rounded-2xl border-2 border-purple-200 bg-gradient-to-br from-purple-50 via-white to-indigo-50 p-5 shadow-sm sm:p-6 transition-all hover:shadow-md">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-3.5">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 text-white shadow-md shadow-purple-500/25">
                <Sparkles className="h-6 w-6 animate-pulse" />
              </div>
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="text-base font-bold text-navy sm:text-lg">
                    {language === 'ta' ? 'சிந்தனைச் செயல்பாட்டை முடிக்கவும்' : 'Finish the Reflective Activity'}
                  </h3>
                  {reflectionState.submitted ? (
                    <span className="inline-flex items-center gap-1 rounded-full bg-mint-100 px-2.5 py-0.5 text-xs font-semibold text-mint-800 border border-mint-200">
                      <CheckCircle2 className="h-3.5 w-3.5" /> {language === 'ta' ? 'நிறைவுற்றது' : 'Completed'}
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1 rounded-full bg-purple-100 px-2.5 py-0.5 text-xs font-bold text-purple-800 border border-purple-200 animate-pulse">
                      {language === 'ta' ? 'முடிக்கவும்' : 'Action Required'}
                    </span>
                  )}
                </div>
                <p className="mt-1 text-xs sm:text-sm text-navy-600 leading-relaxed">
                  {reflectionState.submitted
                    ? (language === 'ta'
                        ? 'நீங்கள் இப்பாடத்தின் சிந்தனைச் செயல்பாட்டை முடித்துவிட்டீர்கள். உங்கள் பதில்களை மீண்டும் பார்க்கலாம் அல்லது திருத்தலாம்.'
                        : 'You have completed your reflection for this course. You can review or edit your answers anytime.')
                    : (language === 'ta'
                        ? 'தேர்வை முடித்ததற்கு வாழ்த்துகள்! அடுத்த பாடத்தைத் திறக்க மற்றும் கற்றல் உத்திகளைப் பதிவு செய்ய இந்த சிந்தனைச் செயல்பாட்டை முடிக்கவும்.'
                        : 'Congratulations on finishing the assessment! To complete this course and unlock the next topic, please complete the Reflective Activity now.')}
                </p>
                <p className="mt-0.5 text-xs font-medium text-purple-700">
                  {language === 'ta'
                    ? 'சுய மதிப்பீடு மற்றும் உத்திகள் (Self-Assessment & Metacognition)'
                    : 'Self-Assessment & Learning Strategy Reflection'}
                </p>
              </div>
            </div>

            <div className="shrink-0 sm:self-center">
              <Link to={`/courses/${targetCourseSlug}?tab=reflection#reflection`}>
                <Button
                  size="lg"
                  className="w-full sm:w-auto bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold shadow-lg shadow-purple-500/20 gap-2"
                  icon={<ArrowRight className="h-4 w-4" />}
                >
                  {reflectionState.submitted
                    ? (language === 'ta' ? 'சிந்தனைச் செயல்பாட்டைப் பார்' : 'Review Reflection')
                    : (language === 'ta' ? 'சிந்தனைச் செயல்பாட்டிற்குச் செல்' : 'Finish Reflective Activity')}
                </Button>
              </Link>
            </div>
          </div>
        </div>
      )}

      <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
        {targetCourseSlug && (
          <Link to={`/courses/${targetCourseSlug}?tab=reflection#reflection`} className="order-first sm:order-none">
            <Button
              variant="primary"
              icon={<Sparkles className="h-4 w-4" />}
              className="w-full sm:w-auto bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold shadow-md ring-2 ring-purple-300 ring-offset-1"
            >
              {language === 'ta' ? 'சிந்தனைச் செயல்பாடு' : 'Finish Reflective Activity'}
            </Button>
          </Link>
        )}
        <Button variant="secondary" icon={<Trophy className="h-4 w-4" />} onClick={() => setBoard(true)}>View leaderboard</Button>
        <Link to="/courses"><Button variant="secondary" icon={<BookOpen className="h-4 w-4" />}>Courses Catalog</Button></Link>
        <Link to="/dashboard"><Button variant="ghost">Back to dashboard</Button></Link>
      </div>

      <section>
        <h2 className="mb-3 text-lg">Solutions</h2>
        <SolutionReveal questions={result.questions} />
      </section>

      <LeaderboardModal assessmentId={attempt.assessment_id} open={board} onClose={() => setBoard(false)} />
    </div>
  );
}
