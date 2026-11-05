import { ArrowRight, BookOpen, ChevronDown, Lock, RefreshCw, Settings } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { toApiError } from '../api/client';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import EmptyState from '../components/common/EmptyState';
import FloatingActionButton from '../components/common/FloatingActionButton';
import ProgressRing from '../components/common/ProgressRing';
import ServerConfigModal from '../components/common/ServerConfigModal';
import { PageSkeleton } from '../components/common/Skeleton';
import AssessmentCards from '../components/dashboard/AssessmentCards';
import AssessmentTable from '../components/dashboard/AssessmentTable';
import MotivationalBanner from '../components/dashboard/MotivationalBanner';
import RecentActivity from '../components/dashboard/RecentActivity';
import StatsCards from '../components/dashboard/StatsCards';
import { useIsDesktop } from '../hooks/useMediaQuery';
import { useAuthStore } from '../store/authStore';
import { useCourseStore } from '../store/courseStore';
import { assessmentAction } from '../utils/assessmentAction';
import { dailyQuote } from '../utils/motivations';

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const { dashboard, fetchDashboard } = useCourseStore();
  const isDesktop = useIsDesktop();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(!dashboard);
  const [isPracticeOpen, setIsPracticeOpen] = useState(false);
  const [showServerConfig, setShowServerConfig] = useState(false);

  const load = useCallback(async () => {
    setError(null);
    setLoading(true);
    try {
      await fetchDashboard();
    } catch (e) {
      setError(toApiError(e).message);
    } finally {
      setLoading(false);
    }
  }, [fetchDashboard]);

  useEffect(() => {
    void load();
  }, [load]);

  const rawList = dashboard?.assessments ?? [];

  const deduplicated = useMemo(() => {
    return rawList.filter((item) => {
      const isSplitLang = item.slug.endsWith('-en') || item.slug.endsWith('-ta');
      if (isSplitLang) {
        const baseSlug = item.slug.replace(/-(en|ta)$/, '');
        if (rawList.some((o) => o.slug === baseSlug)) return false;
      }
      if (item.slug.endsWith('-ta') && rawList.some((o) => o.slug === item.slug.replace('-ta', '-en'))) return false;
      return true;
    });
  }, [rawList]);

  const graded = useMemo(() => deduplicated.filter((a) => a.attempt_type === 'GRADED'), [deduplicated]);
  const practice = useMemo(() => deduplicated.filter((a) => a.attempt_type === 'PRACTICE'), [deduplicated]);
  const completed = useMemo(() => graded.filter((a) => a.lock_status === 'COMPLETED'), [graded]);

  if (loading && !dashboard) return <PageSkeleton />;
  if (error && !dashboard) {
    return (
      <>
        <Card>
          <EmptyState
            title="Couldn't load your dashboard"
            description={error}
            action={
              <div className="flex flex-wrap items-center justify-center gap-3">
                <Button onClick={load} icon={<RefreshCw className="h-4 w-4" />}>
                  Try again
                </Button>
                <Button variant="secondary" onClick={() => setShowServerConfig(true)} icon={<Settings className="h-4 w-4" />}>
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
              void load();
            }}
          />
        )}
      </>
    );
  }
  if (!dashboard || !user) return null;

  const next = dashboard.continue_item;
  const nextAction = next ? assessmentAction(next) : null;

  return (
    <div className="space-y-5">
      <MotivationalBanner name={user.name} quote={dailyQuote()} />
      <StatsCards stats={dashboard.stats} />

      <div className="grid gap-5 lg:grid-cols-3">
        <div className="space-y-5 lg:col-span-2">
          <Card title="Your assessments" padded={false}>
            {graded.length === 0 ? (
              <EmptyState title="No assessments yet" description="Browse the courses to find your first test." action={<Link to="/courses"><Button>Browse courses</Button></Link>} />
            ) : isDesktop ? (
              <AssessmentTable items={graded} />
            ) : (
              <div className="p-3"><AssessmentCards items={graded} /></div>
            )}
          </Card>

          {practice.length > 0 && (
            <div className="panel overflow-hidden transition-all duration-200">
              <button
                type="button"
                onClick={() => setIsPracticeOpen((prev) => !prev)}
                className="flex w-full items-center justify-between gap-3 px-4 py-3.5 sm:px-5 hover:bg-navy-50/70 transition-colors text-left select-none cursor-pointer"
                aria-expanded={isPracticeOpen}
                id="practice-sets-dropdown-toggle"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-sky-50 text-sky-700">
                    <BookOpen className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h2 className="text-base font-semibold text-navy">Practice sets</h2>
                      <span className="rounded-full bg-sky-100 px-2 py-0.5 text-xs font-semibold text-sky-800">
                        {practice.length}
                      </span>
                    </div>
                    <p className="text-xs text-navy-400">
                      {isPracticeOpen
                        ? 'Click to collapse list'
                        : 'Click to expand and view practice sets'}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 text-xs font-semibold text-sky-700">
                  <span className="hidden sm:inline">{isPracticeOpen ? 'Hide' : 'Show practice sets'}</span>
                  <div className={`flex h-7 w-7 items-center justify-center rounded-md bg-navy-50 text-navy-600 transition-transform duration-200 ${isPracticeOpen ? 'rotate-180 bg-sky-100 text-sky-800' : ''}`}>
                    <ChevronDown className="h-4 w-4" />
                  </div>
                </div>
              </button>

              {isPracticeOpen && (
                <div className="border-t border-line bg-white">
                  <ul className="divide-y divide-line">
                    {practice.map((p) => {
                      const isLocked = p.lock_status === 'LOCKED';
                      return (
                        <li
                          key={p.id}
                          className={`flex items-center justify-between gap-3 px-4 py-3 text-sm sm:px-5 transition-colors ${
                            isLocked ? 'bg-navy-50/40 opacity-70 select-none' : 'hover:bg-navy-50/40'
                          }`}
                        >
                          <div className="min-w-0">
                            <div className="flex items-center gap-2">
                              <span className={`truncate font-medium ${isLocked ? 'text-navy-600' : 'text-navy-900'}`}>
                                {p.title}
                              </span>
                              {isLocked && (
                                <span className="inline-flex items-center gap-1 rounded bg-navy-100 px-1.5 py-0.5 text-[10px] font-semibold text-navy-600">
                                  <Lock className="h-3 w-3" /> Locked
                                </span>
                              )}
                            </div>
                            <div className="text-xs text-navy-400">
                              {p.total_questions} questions · {isLocked ? 'Unlocks with course' : 'instant feedback'}
                            </div>
                          </div>
                          {isLocked ? (
                            <Button size="sm" variant="secondary" disabled className="cursor-not-allowed opacity-60">
                              Locked
                            </Button>
                          ) : (
                            <Link to={`/practice/${p.id}`}>
                              <Button size="sm" variant="secondary">Practise</Button>
                            </Link>
                          )}
                        </li>
                      );
                    })}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="space-y-5">
          <Card>
            <div className="flex items-center gap-4">
              <ProgressRing value={dashboard.stats.completion_percentage} size={96} stroke={9} label="Overall completion" />
              <div>
                <h2 className="text-base">Course progress</h2>
                <p className="text-sm text-navy-500">{dashboard.stats.assessments_completed} of {dashboard.stats.assessments_total} graded tests done</p>
              </div>
            </div>
            {next && nextAction?.to && (
              <Link to={nextAction.to} className="mt-4 block">
                <Button
                  fullWidth
                  size="lg"
                  className="min-h-[3.25rem] py-3 px-4 text-center leading-snug whitespace-normal"
                  icon={<ArrowRight className="h-4 w-4 shrink-0" />}
                >
                  <span className="break-words">
                    {next.lock_status === 'IN_PROGRESS' ? 'Resume' : 'Continue'}: {next.title}
                  </span>
                </Button>
              </Link>
            )}
          </Card>
          <Card title="Your scores"><RecentActivity completed={completed} /></Card>
        </div>
      </div>

      {/* Material 3 Floating Action Button (Mobile Only) */}
      {next && nextAction?.to && (
        <FloatingActionButton
          to={nextAction.to}
          icon={<ArrowRight className="h-5 w-5" />}
          label={`${next.lock_status === 'IN_PROGRESS' ? 'Resume' : 'Continue'}: ${next.title.split('-')[0].trim()}`}
        />
      )}
    </div>
  );
}
