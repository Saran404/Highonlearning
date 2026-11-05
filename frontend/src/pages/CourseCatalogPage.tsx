import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock,
  Lock,
  PlayCircle,
  RefreshCw,
  Settings,
  Sparkles,
  Trophy,
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { toApiError } from '../api/client';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import EmptyState from '../components/common/EmptyState';
import ProgressBar from '../components/common/ProgressBar';
import ServerConfigModal from '../components/common/ServerConfigModal';
import { PageSkeleton } from '../components/common/Skeleton';
import { useCourseStore } from '../store/courseStore';
import type { Course, LockStatus } from '../types';

export default function CourseCatalogPage() {
  const { courses, fetchCourses } = useCourseStore();
  const [loading, setLoading] = useState(courses.length === 0);
  const [retrying, setRetrying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showServerConfig, setShowServerConfig] = useState(false);

  useEffect(() => {
    fetchCourses()
      .catch((e) => setError(toApiError(e).message))
      .finally(() => setLoading(false));
  }, [fetchCourses]);

  const handleRetry = async () => {
    setRetrying(true);
    setError(null);
    try {
      await fetchCourses();
    } catch (e) {
      setError(toApiError(e).message);
    } finally {
      setRetrying(false);
      setLoading(false);
    }
  };

  if (loading && courses.length === 0) return <PageSkeleton />;
  if (error && courses.length === 0) {
    return (
      <>
        <Card>
          <EmptyState
            title="Couldn't load courses"
            description={error}
            action={
              <div className="flex flex-wrap items-center justify-center gap-3">
                <Button
                  onClick={handleRetry}
                  loading={retrying}
                  icon={<RefreshCw className="h-4 w-4" />}
                >
                  Try again
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => setShowServerConfig(true)}
                  icon={<Settings className="h-4 w-4" />}
                >
                  Server Settings
                </Button>
              </div>
            }
          />
        </Card>
        {showServerConfig && (
          <ServerConfigModal
            onClose={() => setShowServerConfig(false)}
            onSaved={() => {
              setShowServerConfig(false);
              void handleRetry();
            }}
          />
        )}
      </>
    );
  }

  // Derive stats across the sequential path
  const totalCourses = courses.length || 8;
  const completedCourses = courses.filter((c) => c.lock_status === 'COMPLETED').length;
  const currentActiveCourse = courses.find(
    (c) => c.lock_status === 'IN_PROGRESS' || c.lock_status === 'AVAILABLE'
  );
  const overallPathPercentage = Math.round((completedCourses / (totalCourses || 1)) * 100);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div>
            <h1 className="text-2xl font-bold text-navy">Courses & Learning Path</h1>
            <p className="mt-1 text-sm text-navy-500">
              Complete each course's graded assessment to unlock the next topic in the 8-course sequence.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-2 rounded-xl bg-sky-50 px-3.5 py-1.5 border border-sky-100 text-sky-900 text-xs font-semibold">
              <Trophy className="h-4 w-4 text-sky-600" />
              <span>
                {completedCourses} of {totalCourses} Courses Completed
              </span>
            </div>
            <button
              type="button"
              onClick={() => setShowServerConfig(true)}
              className="flex items-center gap-1.5 rounded-xl border border-line bg-white px-3 py-1.5 text-xs font-medium text-navy-600 hover:bg-navy-50 hover:text-navy transition-all shadow-2xs"
              title="Configure API Server URL"
            >
              <Settings className="h-3.5 w-3.5 text-navy-400" />
              <span className="hidden sm:inline">Server</span>
            </button>
          </div>
        </div>
      </div>

      {/* Sequential Journey Progression Stepper */}
      {courses.length > 0 && (
        <div className="rounded-2xl border border-line bg-white p-4 sm:p-5 shadow-xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-line">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-sky-700">
                Curriculum Progression
              </span>
              <h2 className="text-base font-semibold text-navy">
                {currentActiveCourse
                  ? `Current Lesson: ${currentActiveCourse.title}`
                  : completedCourses === totalCourses
                  ? 'All Lessons Completed! 🎉'
                  : 'Start Lesson 1 to Begin'}
              </h2>
            </div>
            <div className="w-full sm:w-48">
              <div className="flex justify-between text-xs text-navy-500 mb-1">
                <span>Journey Completion</span>
                <span className="font-semibold text-navy">{overallPathPercentage}%</span>
              </div>
              <ProgressBar
                value={overallPathPercentage}
                tone={overallPathPercentage === 100 ? 'mint' : 'sky'}
                label="Overall syllabus completion"
              />
            </div>
          </div>

          {/* Stepper Dots (Swipeable on mobile, Grid on desktop) */}
          <div className="mt-4 flex gap-2.5 overflow-x-auto pb-2 pt-1 overscroll-x-contain snap-x sm:grid sm:grid-cols-8 sm:gap-2 sm:overflow-visible no-scrollbar">
            {courses.map((c, idx) => {
              const status: LockStatus = c.lock_status ?? 'LOCKED';
              const isCompleted = status === 'COMPLETED';
              const isInProgress = status === 'IN_PROGRESS';
              const isAvailable = status === 'AVAILABLE';
              const isLocked = status === 'LOCKED';

              return (
                <div
                  key={c.id}
                  className={`relative flex flex-col items-center justify-between rounded-xl p-2.5 min-h-[6.75rem] text-center transition-all shrink-0 w-28 snap-start sm:w-auto m3-touch ${
                    isCompleted
                      ? 'bg-mint-50/70 border border-mint-200 text-mint-900'
                      : isInProgress || isAvailable
                      ? 'bg-sky-50 border-2 border-sky-500 text-sky-950 shadow-xs'
                      : 'bg-navy-50/50 border border-dashed border-navy-200 text-navy-400 opacity-75'
                  }`}
                  title={`${c.title}: ${status}`}
                >
                  <div
                    className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${
                      isCompleted
                        ? 'bg-mint-600 text-white'
                        : isInProgress
                        ? 'bg-sky-600 text-white animate-pulse'
                        : isAvailable
                        ? 'bg-sky-500 text-white'
                        : 'bg-navy-200 text-navy-500'
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircle2 className="h-4 w-4" />
                    ) : isLocked ? (
                      <Lock className="h-3.5 w-3.5" />
                    ) : (
                      idx + 1
                    )}
                  </div>
                  <span className="mt-1 text-[11px] font-medium leading-tight line-clamp-2 text-center flex-1 flex items-center justify-center">
                    {c.title.split('/')[0].trim()}
                  </span>
                  <span className="text-[10px] uppercase font-semibold text-navy-400 mt-auto pt-1">
                    Lesson {idx + 1}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Courses List Grid */}
      {courses.length === 0 ? (
        <Card className="mt-5">
          <EmptyState
            icon={<BookOpen className="h-10 w-10 text-navy-400" />}
            title="No courses yet"
            description="Course curriculum is currently being prepared. Check back shortly."
          />
        </Card>
      ) : (
        <div className="grid gap-5 sm:grid-cols-2">
          {courses.map((c, idx) => {
            const status: LockStatus = c.lock_status ?? (idx === 0 ? 'AVAILABLE' : 'LOCKED');
            const isCompleted = status === 'COMPLETED';
            const isInProgress = status === 'IN_PROGRESS';
            const isAvailable = status === 'AVAILABLE';
            const isLocked = status === 'LOCKED';

            const pct = c.graded_count ? Math.round((100 * c.completed_count) / c.graded_count) : 0;

            // Render Card Content
            const cardContent = (
              <div className="flex h-full flex-col justify-between p-5">
                <div>
                  {/* Top Badges */}
                  <div className="flex items-center justify-between gap-2">
                    <span className="inline-flex items-center rounded-md bg-navy-100/80 px-2.5 py-0.5 text-[11px] font-bold uppercase tracking-wider text-navy-700">
                      Course {idx + 1} of {totalCourses}
                    </span>

                    {/* Status Pill */}
                    {isCompleted && (
                      <span className="inline-flex items-center gap-1.5 rounded-full bg-mint-50 px-2.5 py-0.5 text-xs font-semibold text-mint-800 border border-mint-200">
                        <CheckCircle2 className="h-3.5 w-3.5 text-mint-600" />
                        Completed
                      </span>
                    )}
                    {isInProgress && (
                      <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 px-2.5 py-0.5 text-xs font-semibold text-amber-800 border border-amber-200">
                        <PlayCircle className="h-3.5 w-3.5 text-amber-600" />
                        In Progress
                      </span>
                    )}
                    {isAvailable && (
                      <span className="inline-flex items-center gap-1.5 rounded-full bg-sky-50 px-2.5 py-0.5 text-xs font-semibold text-sky-800 border border-sky-200">
                        <Sparkles className="h-3.5 w-3.5 text-sky-600" />
                        Available
                      </span>
                    )}
                    {isLocked && (
                      <span className="inline-flex items-center gap-1.5 rounded-full bg-navy-100 px-2.5 py-0.5 text-xs font-semibold text-navy-600 border border-navy-200">
                        <Lock className="h-3.5 w-3.5 text-navy-500" />
                        Locked
                      </span>
                    )}
                  </div>

                  {/* Course Title & Description */}
                  <h2 className={`mt-3 text-lg font-bold ${isLocked ? 'text-navy-600' : 'text-navy'}`}>
                    {c.title}
                  </h2>
                  {c.description && (
                    <p className={`mt-1.5 line-clamp-2 text-sm ${isLocked ? 'text-navy-400' : 'text-navy-600'}`}>
                      {c.description}
                    </p>
                  )}
                </div>

                <div className="mt-5 space-y-4">
                  {/* Progress & Stats */}
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs text-navy-500">
                      <span>{c.graded_count} graded · {c.practice_count} practice sets</span>
                      <span className="font-semibold tabular-nums text-navy-700">
                        {isCompleted
                          ? 'Course Completed'
                          : c.completed_count >= c.graded_count && c.graded_count > 0
                          ? 'Reflection Pending'
                          : `${c.completed_count}/${c.graded_count} done`}
                      </span>
                    </div>
                    <ProgressBar
                      value={isCompleted ? 100 : c.completed_count >= c.graded_count && c.graded_count > 0 ? 90 : pct}
                      tone={isCompleted ? 'mint' : 'sky'}
                      label={`${c.title} progress`}
                    />
                  </div>

                  {/* Action / State Indicator Footer */}
                  {isLocked ? (
                    <div className="rounded-xl bg-navy-100/60 p-3 border border-dashed border-navy-200 text-xs text-navy-600">
                      <div className="flex items-center gap-2 font-medium">
                        <Lock className="h-4 w-4 text-navy-400 shrink-0" />
                        <span>
                          Locked — Complete {c.previous_course_title ? `"${c.previous_course_title}"` : `Course ${idx}`} to unlock.
                        </span>
                      </div>
                    </div>
                  ) : (
                    <div className="pt-1">
                      <div className="flex items-center justify-between text-xs font-semibold text-sky-700 group-hover:text-sky-800">
                        <span>
                          {isCompleted
                            ? 'Review Course & Practice'
                            : c.completed_count >= c.graded_count && c.graded_count > 0
                            ? 'Complete Reflection'
                            : isInProgress
                            ? 'Continue Learning'
                            : 'Start Course'}
                        </span>
                        <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );

            return (
              <div key={c.id}>
                {isLocked ? (
                  // Locked Card: NOT clickable / NOT accessible, visually greyed out
                  <div
                    className="panel h-full opacity-65 bg-navy-50/40 border-dashed border-navy-300 select-none cursor-not-allowed shadow-none"
                    aria-disabled="true"
                    title={`Complete ${c.previous_course_title || `Course ${idx}`} to unlock this course`}
                  >
                    {cardContent}
                  </div>
                ) : (
                  // Unlocked Card: Clickable link to CourseDetailPage
                  <Link
                    to={`/courses/${c.slug}`}
                    className={`panel group block h-full transition-all duration-200 hover:shadow-md ${
                      isInProgress
                        ? 'border-sky-300 ring-2 ring-sky-100/70 hover:border-sky-400'
                        : isCompleted
                        ? 'border-mint-200 hover:border-mint-300'
                        : 'hover:border-sky-300'
                    }`}
                  >
                    {cardContent}
                  </Link>
                )}
              </div>
            );
          })}
        </div>
      )}

      {showServerConfig && (
        <ServerConfigModal
          onClose={() => setShowServerConfig(false)}
          onSaved={() => {
            setShowServerConfig(false);
            void handleRetry();
          }}
        />
      )}
    </div>
  );
}
