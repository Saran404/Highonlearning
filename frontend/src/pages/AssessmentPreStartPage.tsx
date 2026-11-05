import { ChevronLeft, Clock, ListChecks, Target } from 'lucide-react';
import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { assessmentsApi } from '../api/assessments';
import { attemptsApi } from '../api/attempts';
import { toApiError } from '../api/client';
import DurationPicker from '../components/assessment/DurationPicker';
import PreStartCheck from '../components/assessment/PreStartCheck';
import RuleAcknowledgement from '../components/assessment/RuleAcknowledgement';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import EmptyState from '../components/common/EmptyState';
import { PageSkeleton } from '../components/common/Skeleton';
import type { AssessmentItem } from '../types';

export default function AssessmentPreStartPage() {
  const { id } = useParams();
  const assessmentId = Number(id);
  const navigate = useNavigate();
  const [a, setA] = useState<AssessmentItem | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [minutes, setMinutes] = useState(0);
  const [checksOk, setChecksOk] = useState(false);
  const [ack, setAck] = useState({ no_minimize: false, consent_camera: false, single_attempt: false });
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    assessmentsApi
      .get(assessmentId)
      .then((res) => {
        setA(res);
        setMinutes(res.default_duration_minutes);
      })
      .catch((e) => setError(toApiError(e).message));
  }, [assessmentId]);

  if (error) return <Card><EmptyState title="Assessment not found" description={error} action={<Link to="/courses" className="text-sky-700 underline">Back to courses</Link>} /></Card>;
  if (!a) return <PageSkeleton />;
  if (a.attempt_type === 'PRACTICE') return <Navigate to={`/practice/${a.id}`} replace />;

  const back = <Link to={`/courses/${a.course_slug}`} className="inline-flex items-center gap-1 text-sm text-sky-700 hover:underline"><ChevronLeft className="h-4 w-4" />{a.course_title}</Link>;

  if (a.lock_status !== 'AVAILABLE') {
    const content = {
      COMPLETED: { title: 'You have already taken this test', text: 'Each graded test is a single attempt. Your result and solutions are ready.', to: `/results/${a.attempt_id}`, cta: 'View result' },
      IN_PROGRESS: { title: 'Your attempt is still running', text: 'The timer did not stop. Continue where you left off.', to: `/attempts/${a.attempt_id}`, cta: 'Resume test' },
      LOCKED: { title: 'This test is locked', text: 'Finish the previous test in this course to unlock it.', to: `/courses/${a.course_slug}`, cta: 'Back to course' },
    }[a.lock_status as 'COMPLETED' | 'IN_PROGRESS' | 'LOCKED'];
    return (
      <div className="space-y-4">{back}<Card><EmptyState title={content.title} description={content.text} action={<Link to={content.to}><Button>{content.cta}</Button></Link>} /></Card></div>
    );
  }

  const ready = checksOk && ack.no_minimize && ack.consent_camera && ack.single_attempt;

  const onStart = async () => {
    setStarting(true);
    // Fullscreen must be requested inside the click (user gesture) - before any await that hits the network.
    if (a.lockdown_enabled) {
      try {
        await document.documentElement.requestFullscreen();
      } catch {
        /* the exam page asks again if this was refused */
      }
    }
    try {
      const state = await attemptsApi.start({ assessment_id: a.id, chosen_duration_minutes: minutes, acknowledgments: ack });
      navigate(`/attempts/${state.attempt_id}`, { replace: true });
    } catch (e) {
      if (document.fullscreenElement) void document.exitFullscreen();
      const err = toApiError(e);
      if (err.code === 'ATTEMPT_EXISTS') {
        const existing = (err.details as { attempt_id?: number; status?: string } | undefined) ?? {};
        toast.error('You already have an attempt for this test.');
        if (existing.attempt_id) navigate(existing.status === 'IN_PROGRESS' ? `/attempts/${existing.attempt_id}` : `/results/${existing.attempt_id}`, { replace: true });
      } else {
        toast.error(err.message);
      }
      setStarting(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl space-y-5">
      {back}
      <div>
        <h1 className="text-2xl">{a.title}</h1>
        {a.description && <p className="mt-1 text-sm text-navy-500">{a.description}</p>}
        <div className="mt-3 flex flex-wrap gap-x-5 gap-y-1 text-sm text-navy-600">
          <span className="inline-flex items-center gap-1.5"><ListChecks className="h-4 w-4" />{a.total_questions} questions</span>
          <span className="inline-flex items-center gap-1.5"><Clock className="h-4 w-4" />{a.min_duration_minutes}–{a.default_duration_minutes} minutes</span>
          <span className="inline-flex items-center gap-1.5"><Target className="h-4 w-4" />Pass mark {a.pass_percentage}%</span>
        </div>
      </div>

      <Card><DurationPicker min={a.min_duration_minutes} max={a.default_duration_minutes} value={minutes} onChange={setMinutes} /></Card>
      <Card><PreStartCheck requireCamera={a.proctoring_enabled} requireFullscreen={a.lockdown_enabled} onChange={setChecksOk} /></Card>
      <Card><RuleAcknowledgement value={ack} onChange={setAck} /></Card>

      <div className="sticky bottom-16 z-10 lg:bottom-4">
        <Button size="lg" fullWidth disabled={!ready} loading={starting} onClick={onStart}>Start test · {minutes} min</Button>
        {!ready && <p className="mt-2 text-center text-xs text-navy-500">Pass the system check and accept all three rules to begin.</p>}
      </div>
    </div>
  );
}
