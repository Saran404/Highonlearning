import { create } from 'zustand';
import { coursesApi } from '../api/courses';
import type { AssessmentItem, User } from '../types';
import { assessmentAction } from '../utils/assessmentAction';
import {
  AssessmentSessionRecord,
  getLastSessionSummary,
  LastSessionSummary,
  PracticeSessionRecord,
} from '../utils/sessionTracker';

export interface NextActionItem {
  id: number;
  title: string;
  title_ta?: string | null;
  type: 'GRADED' | 'PRACTICE';
  status: 'IN_PROGRESS' | 'AVAILABLE';
  to: string;
  label: string;
  courseTitle?: string | null;
}

export interface ResumeData {
  userName: string;
  lastActiveTimeText: string;
  practiceFinished?: PracticeSessionRecord | null;
  practiceInProgress?: PracticeSessionRecord | null;
  assessmentFinished?: AssessmentSessionRecord | null;
  assessmentInProgress?: AssessmentSessionRecord | null;
  nextActionItem?: NextActionItem | null;
}

interface ResumeSessionState {
  isOpen: boolean;
  resumeData: ResumeData | null;
  openResumeModal: (data: ResumeData) => void;
  closeResumeModal: () => void;
  checkAndTriggerResume: (user: User) => Promise<boolean>;
}

function formatRelativeTime(timestamp?: number): string {
  if (!timestamp) return 'recently';
  const diffSec = Math.floor((Date.now() - timestamp) / 1000);
  if (diffSec < 60) return 'just a moment ago';
  const diffMin = Math.floor(diffSec / 60);
  if (diffMin < 60) return `${diffMin} ${diffMin === 1 ? 'minute' : 'minutes'} ago`;
  const diffHours = Math.floor(diffMin / 60);
  if (diffHours < 24) return `${diffHours} ${diffHours === 1 ? 'hour' : 'hours'} ago`;
  const diffDays = Math.floor(diffHours / 24);
  if (diffDays === 1) return 'yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  return new Date(timestamp).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
  });
}

export const useResumeSessionStore = create<ResumeSessionState>((set) => ({
  isOpen: false,
  resumeData: null,

  openResumeModal: (data) => set({ isOpen: true, resumeData: data }),
  closeResumeModal: () => set({ isOpen: false }),

  checkAndTriggerResume: async (user: User) => {
    if (!user || !user.id) return false;

    // Check if already shown in the current browser session
    const shownKey = `exampro_resume_shown_${user.id}`;
    if (sessionStorage.getItem(shownKey) === 'true') {
      return false;
    }

    const summary: LastSessionSummary | null = getLastSessionSummary(user.id);

    // Fetch authoritative backend dashboard state
    let continueItem: AssessmentItem | null = null;
    let latestCompletedAssessmentFromApi: AssessmentItem | null = null;
    let activeInProgressFromApi: AssessmentItem | null = null;

    try {
      const dashboard = await coursesApi.dashboard();
      if (dashboard) {
        continueItem = dashboard.continue_item;
        const allAssessments = dashboard.assessments || [];
        const completed = allAssessments.filter((a) => a.lock_status === 'COMPLETED');
        if (completed.length > 0) {
          latestCompletedAssessmentFromApi = completed[completed.length - 1];
        }
        activeInProgressFromApi =
          allAssessments.find((a) => a.lock_status === 'IN_PROGRESS') || null;
      }
    } catch {
      /* network or auth fallback */
    }

    // Determine practice finished
    const practiceFinished = summary?.practiceCompleted || null;
    const practiceInProgress = summary?.practiceInProgress || null;

    // Determine assessment finished
    let assessmentFinished: AssessmentSessionRecord | null =
      summary?.assessmentCompleted || null;

    if (!assessmentFinished && latestCompletedAssessmentFromApi) {
      assessmentFinished = {
        attemptId: latestCompletedAssessmentFromApi.attempt_id,
        assessmentId: latestCompletedAssessmentFromApi.id,
        title: latestCompletedAssessmentFromApi.title,
        title_ta: latestCompletedAssessmentFromApi.title_ta,
        courseSlug: latestCompletedAssessmentFromApi.course_slug,
        courseTitle: latestCompletedAssessmentFromApi.course_title,
        score: latestCompletedAssessmentFromApi.score,
        total: latestCompletedAssessmentFromApi.total,
        percentage: latestCompletedAssessmentFromApi.percentage,
        timeTakenSec: latestCompletedAssessmentFromApi.time_taken_sec,
        status: 'COMPLETED',
        completed: true,
        timestamp: summary?.sessionEndedAt || Date.now(),
      };
    }

    // Determine assessment in progress
    let assessmentInProgress: AssessmentSessionRecord | null =
      summary?.assessmentInProgress || null;

    if (!assessmentInProgress && activeInProgressFromApi) {
      assessmentInProgress = {
        attemptId: activeInProgressFromApi.attempt_id,
        assessmentId: activeInProgressFromApi.id,
        title: activeInProgressFromApi.title,
        title_ta: activeInProgressFromApi.title_ta,
        courseSlug: activeInProgressFromApi.course_slug,
        courseTitle: activeInProgressFromApi.course_title,
        status: 'IN_PROGRESS',
        completed: false,
        timestamp: Date.now(),
      };
    }

    // Determine next action / continue recommendation
    let nextActionItem: NextActionItem | null = null;
    const isTamil = localStorage.getItem('exampro_lang') === 'ta';

    if (activeInProgressFromApi) {
      const act = assessmentAction(activeInProgressFromApi);
      if (act.to) {
        nextActionItem = {
          id: activeInProgressFromApi.id,
          title: activeInProgressFromApi.title,
          title_ta: activeInProgressFromApi.title_ta,
          type: activeInProgressFromApi.attempt_type,
          status: 'IN_PROGRESS',
          to: act.to,
          label: isTamil
            ? `தேர்வைத் தொடர்க: ${activeInProgressFromApi.title_ta || activeInProgressFromApi.title}`
            : `Resume Test: ${activeInProgressFromApi.title}`,
          courseTitle: activeInProgressFromApi.course_title,
        };
      }
    } else if (practiceInProgress && !practiceInProgress.completed) {
      const nextQ = (practiceInProgress.lastQuestionIndex ?? practiceInProgress.answeredCount ?? 0) + 1;
      nextActionItem = {
        id: practiceInProgress.assessmentId,
        title: practiceInProgress.title,
        title_ta: practiceInProgress.title_ta,
        type: 'PRACTICE',
        status: 'IN_PROGRESS',
        to: `/practice/${practiceInProgress.assessmentId}`,
        label: isTamil
          ? `பயிற்சியைத் தொடர்க (வினா ${nextQ})`
          : `Resume Practice (Question ${nextQ})`,
        courseTitle: practiceInProgress.courseTitle,
      };
    } else if (continueItem) {
      const act = assessmentAction(continueItem);
      if (act.to) {
        nextActionItem = {
          id: continueItem.id,
          title: continueItem.title,
          title_ta: continueItem.title_ta,
          type: continueItem.attempt_type,
          status: continueItem.lock_status === 'IN_PROGRESS' ? 'IN_PROGRESS' : 'AVAILABLE',
          to: act.to,
          label:
            continueItem.lock_status === 'IN_PROGRESS'
              ? (isTamil ? `தொடர்க: ${continueItem.title_ta || continueItem.title}` : `Resume: ${continueItem.title}`)
              : (isTamil ? `அடுத்தது: ${continueItem.title_ta || continueItem.title}` : `Continue: ${continueItem.title}`),
          courseTitle: continueItem.course_title,
        };
      }
    } else if (summary?.lastCourseSlug) {
      nextActionItem = {
        id: 0,
        title: summary.lastCourseTitle || 'Course Curriculum',
        type: 'PRACTICE',
        status: 'AVAILABLE',
        to: `/courses/${summary.lastCourseSlug}`,
        label: isTamil ? `${summary.lastCourseTitle || 'பாடம்'} தொடர்க` : `Continue ${summary.lastCourseTitle || 'Course'}`,
        courseTitle: summary.lastCourseTitle,
      };
    }

    // If user has done practice, done assessment, or has an ongoing assessment:
    const hasLastSessionActivity = Boolean(
      practiceFinished ||
        practiceInProgress ||
        assessmentFinished ||
        assessmentInProgress
    );

    if (!hasLastSessionActivity) {
      return false;
    }

    const lastActiveTimeText = formatRelativeTime(summary?.sessionEndedAt);

    const payload: ResumeData = {
      userName: user.name || 'Student',
      lastActiveTimeText,
      practiceFinished,
      practiceInProgress,
      assessmentFinished,
      assessmentInProgress,
      nextActionItem,
    };

    // Mark as shown for this browser session so it doesn't pop up again on internal navigation
    try {
      sessionStorage.setItem(shownKey, 'true');
    } catch {
      /* ignore */
    }

    set({ isOpen: true, resumeData: payload });
    return true;
  },
}));
