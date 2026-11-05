/**
 * Session Activity Tracker.
 * Tracks practice sets and assessments completed during a user's login session,
 * and persists the session summary so that upon next login, the user can be shown
 * a popup modal resuming where they left off and summarizing what they finished.
 */

export interface PracticeSessionRecord {
  assessmentId: number;
  title: string;
  title_ta?: string | null;
  courseSlug?: string | null;
  courseTitle?: string | null;
  totalQuestions: number;
  answeredCount: number;
  correctCount: number;
  percentage: number;
  lastQuestionIndex?: number;
  completed: boolean;
  timestamp: number;
}

export interface AssessmentSessionRecord {
  attemptId?: number | null;
  assessmentId: number;
  title: string;
  title_ta?: string | null;
  courseSlug?: string | null;
  courseTitle?: string | null;
  score?: number | null;
  total?: number | null;
  percentage?: number | null;
  timeTakenSec?: number | null;
  status: 'IN_PROGRESS' | 'COMPLETED';
  completed: boolean;
  timestamp: number;
}

export interface LastSessionSummary {
  userId: number;
  userName: string;
  sessionEndedAt: number;
  practiceCompleted?: PracticeSessionRecord | null;
  practiceInProgress?: PracticeSessionRecord | null;
  assessmentCompleted?: AssessmentSessionRecord | null;
  assessmentInProgress?: AssessmentSessionRecord | null;
  lastCourseSlug?: string | null;
  lastCourseTitle?: string | null;
}

const STORAGE_PREFIX_LAST_SESSION = 'exampro_last_session_';
const STORAGE_PREFIX_CURRENT_SESSION = 'exampro_current_session_';

/**
 * Get active session buffer for the current login.
 */
function getCurrentSessionBuffer(userId: number): Partial<LastSessionSummary> {
  try {
    const raw = localStorage.getItem(`${STORAGE_PREFIX_CURRENT_SESSION}${userId}`);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return {};
}

/**
 * Save active session buffer.
 */
function saveCurrentSessionBuffer(userId: number, buffer: Partial<LastSessionSummary>): void {
  try {
    localStorage.setItem(`${STORAGE_PREFIX_CURRENT_SESSION}${userId}`, JSON.stringify(buffer));
  } catch {
    /* ignore */
  }
}

/**
 * Record practice activity during the session.
 */
export function recordPracticeActivity(
  userId: number,
  record: Omit<PracticeSessionRecord, 'timestamp'>
): void {
  if (!userId) return;
  const current = getCurrentSessionBuffer(userId);
  const fullRecord: PracticeSessionRecord = {
    ...record,
    timestamp: Date.now(),
  };

  if (record.completed) {
    current.practiceCompleted = fullRecord;
    current.practiceInProgress = null;
  } else {
    current.practiceInProgress = fullRecord;
  }

  if (record.courseSlug) current.lastCourseSlug = record.courseSlug;
  if (record.courseTitle) current.lastCourseTitle = record.courseTitle;

  saveCurrentSessionBuffer(userId, current);
}

/**
 * Record graded assessment activity during the session.
 */
export function recordAssessmentActivity(
  userId: number,
  record: Omit<AssessmentSessionRecord, 'timestamp'>
): void {
  if (!userId) return;
  const current = getCurrentSessionBuffer(userId);
  const fullRecord: AssessmentSessionRecord = {
    ...record,
    timestamp: Date.now(),
  };

  if (record.status === 'COMPLETED') {
    current.assessmentCompleted = fullRecord;
    current.assessmentInProgress = null;
  } else {
    current.assessmentInProgress = fullRecord;
  }

  if (record.courseSlug) current.lastCourseSlug = record.courseSlug;
  if (record.courseTitle) current.lastCourseTitle = record.courseTitle;

  saveCurrentSessionBuffer(userId, current);
}

/**
 * Record course visited.
 */
export function recordCourseVisited(
  userId: number,
  courseSlug?: string | null,
  courseTitle?: string | null
): void {
  if (!userId || !courseSlug) return;
  const current = getCurrentSessionBuffer(userId);
  current.lastCourseSlug = courseSlug;
  if (courseTitle) current.lastCourseTitle = courseTitle;
  saveCurrentSessionBuffer(userId, current);
}

/**
 * Called on user logout or session wrap-up to finalize this login session's summary.
 * It copies current session activities into the permanent "last session" storage key.
 */
export function finalizeSessionSummary(userId: number, userName: string): LastSessionSummary | null {
  if (!userId) return null;
  const current = getCurrentSessionBuffer(userId);

  // If nothing was done in this session, check if there was a previous summary so we don't wipe it out entirely
  const previousSummary = getLastSessionSummary(userId);

  const summary: LastSessionSummary = {
    userId,
    userName: userName || previousSummary?.userName || 'Student',
    sessionEndedAt: Date.now(),
    practiceCompleted: current.practiceCompleted ?? previousSummary?.practiceCompleted ?? null,
    practiceInProgress: current.practiceInProgress ?? previousSummary?.practiceInProgress ?? null,
    assessmentCompleted: current.assessmentCompleted ?? previousSummary?.assessmentCompleted ?? null,
    assessmentInProgress: current.assessmentInProgress ?? previousSummary?.assessmentInProgress ?? null,
    lastCourseSlug: current.lastCourseSlug ?? previousSummary?.lastCourseSlug ?? null,
    lastCourseTitle: current.lastCourseTitle ?? previousSummary?.lastCourseTitle ?? null,
  };

  try {
    localStorage.setItem(`${STORAGE_PREFIX_LAST_SESSION}${userId}`, JSON.stringify(summary));
    // Clear the current session working buffer for next login
    localStorage.removeItem(`${STORAGE_PREFIX_CURRENT_SESSION}${userId}`);
  } catch {
    /* ignore */
  }

  return summary;
}

/**
 * Retrieve the last session summary for a user.
 */
export function getLastSessionSummary(userId: number): LastSessionSummary | null {
  if (!userId) return null;
  try {
    const raw = localStorage.getItem(`${STORAGE_PREFIX_LAST_SESSION}${userId}`);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return null;
}

/* ------------------------------------------------------------ Practice Set Granular State */
export interface StoredPracticeProgress {
  assessmentId: number;
  currentIndex: number;
  feedback: Record<number, any>;
  done: boolean;
  totalQuestions: number;
  updatedAt: number;
}

const STORAGE_PREFIX_PRACTICE_STATE = 'exampro_practice_state_';

/**
 * Save user's question-by-question progress in a practice set.
 */
export function savePracticeProgress(
  userId: number,
  assessmentId: number,
  data: {
    currentIndex: number;
    feedback: Record<number, any>;
    done: boolean;
    totalQuestions: number;
  }
): void {
  if (!userId || !assessmentId) return;
  const key = `${STORAGE_PREFIX_PRACTICE_STATE}${userId}_${assessmentId}`;
  try {
    const record: StoredPracticeProgress = {
      assessmentId,
      currentIndex: data.currentIndex,
      feedback: data.feedback,
      done: data.done,
      totalQuestions: data.totalQuestions,
      updatedAt: Date.now(),
    };
    localStorage.setItem(key, JSON.stringify(record));
  } catch {
    /* ignore */
  }
}

/**
 * Retrieve saved practice progress for a user and assessment.
 */
export function getPracticeProgress(
  userId: number,
  assessmentId: number
): StoredPracticeProgress | null {
  if (!userId || !assessmentId) return null;
  const key = `${STORAGE_PREFIX_PRACTICE_STATE}${userId}_${assessmentId}`;
  try {
    const raw = localStorage.getItem(key);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return null;
}

/**
 * Clear saved practice progress (e.g. when user clicks restart).
 */
export function clearPracticeProgress(userId: number, assessmentId: number): void {
  if (!userId || !assessmentId) return;
  const key = `${STORAGE_PREFIX_PRACTICE_STATE}${userId}_${assessmentId}`;
  try {
    localStorage.removeItem(key);
  } catch {
    /* ignore */
  }
}
