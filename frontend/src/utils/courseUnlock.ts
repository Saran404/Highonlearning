import type { Course, LockStatus } from '../types';

const STORAGE_PREFIX = 'exampro_course_unlocks_';

export interface StoredCourseState {
  lock_status: LockStatus;
  completed: boolean;
  slug: string;
  updatedAt: string;
}

/**
 * Read cached course unlock states from localStorage.
 */
export function getStoredCourseUnlocks(userId?: number | null): Record<string, StoredCourseState> {
  if (typeof window === 'undefined') return {};
  const key = `${STORAGE_PREFIX}${userId ?? 'guest'}`;
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return {};
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

/**
 * Save current course unlock states to localStorage.
 */
export function saveCourseUnlocks(courses: Course[], userId?: number | null): void {
  if (typeof window === 'undefined' || !courses.length) return;
  const key = `${STORAGE_PREFIX}${userId ?? 'guest'}`;
  try {
    const map: Record<string, StoredCourseState> = {};
    for (const c of courses) {
      const isCompleted = c.lock_status === 'COMPLETED';
      map[c.slug] = {
        lock_status: c.lock_status ?? 'AVAILABLE',
        completed: isCompleted,
        slug: c.slug,
        updatedAt: new Date().toISOString(),
      };
    }
    localStorage.setItem(key, JSON.stringify(map));
  } catch (err) {
    console.error('Failed to save course unlocks to localStorage:', err);
  }
}

/**
 * Mark a course as completed in localStorage (e.g. after passing a graded assessment).
 */
export function markCourseCompletedInStorage(courseSlug: string, userId?: number | null): void {
  if (typeof window === 'undefined') return;
  const current = getStoredCourseUnlocks(userId);
  current[courseSlug] = {
    lock_status: 'COMPLETED',
    completed: true,
    slug: courseSlug,
    updatedAt: new Date().toISOString(),
  };
  const key = `${STORAGE_PREFIX}${userId ?? 'guest'}`;
  try {
    localStorage.setItem(key, JSON.stringify(current));
  } catch (err) {
    console.error('Failed to update course completion in localStorage:', err);
  }
}

/**
 * Pure sequential course unlock resolver:
 * 1. Only Course 1 is unlocked initially (AVAILABLE or IN_PROGRESS).
 * 2. Course N requires Course N-1 to be fully COMPLETED.
 * 3. Courses 2 through 8 are locked until their respective prerequisite is completed.
 * 4. Merges authoritative API counts with client localStorage cache for instant persistence.
 */
export function resolveCourseUnlocks(courses: Course[], userId?: number | null): Course[] {
  if (!courses || courses.length === 0) return [];

  // Sort by order_index, then id to ensure deterministic sequence
  const sorted = [...courses].sort((a, b) => (a.order_index - b.order_index) || (a.id - b.id));
  const cached = getStoredCourseUnlocks(userId);

  let previousDone = true; // Course 1 is unlocked initially
  let prevTitle: string | null = null;
  let prevSlug: string | null = null;

  const resolved = sorted.map((c, index) => {
    const isCachedDone = cached[c.slug]?.completed === true;
    const isApiDone = c.lock_status === 'COMPLETED';
    const isCompleted = isApiDone || isCachedDone;

    let status: LockStatus;
    let requiredPrevTitle: string | null = null;
    let requiredPrevSlug: string | null = null;

    if (isCompleted) {
      status = 'COMPLETED';
      requiredPrevTitle = prevTitle;
      requiredPrevSlug = prevSlug;
      previousDone = true;
    } else if (previousDone) {
      // First course or previous course completed -> this course is unlocked!
      const hasProgress = c.completed_count > 0 || c.enrolled || c.lock_status === 'IN_PROGRESS';
      status = hasProgress ? 'IN_PROGRESS' : 'AVAILABLE';
      requiredPrevTitle = prevTitle;
      requiredPrevSlug = prevSlug;
      previousDone = false; // Next course cannot unlock until this one completes
    } else {
      // Previous course not yet complete -> this course is LOCKED
      status = 'LOCKED';
      requiredPrevTitle = prevTitle;
      requiredPrevSlug = prevSlug;
      previousDone = false;
    }

    prevTitle = c.title;
    prevSlug = c.slug;

    return {
      ...c,
      lock_status: status,
      previous_course_title: requiredPrevTitle ?? c.previous_course_title,
      previous_course_slug: requiredPrevSlug ?? c.previous_course_slug,
    };
  });

  // Sync back to localStorage
  saveCourseUnlocks(resolved, userId);

  return resolved;
}
