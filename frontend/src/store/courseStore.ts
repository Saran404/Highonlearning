import { create } from 'zustand';
import { coursesApi } from '../api/courses';
import type { AssessmentItem, Course, DashboardData } from '../types';
import { resolveCourseUnlocks, markCourseCompletedInStorage } from '../utils/courseUnlock';
import { useAuthStore } from './authStore';

interface CourseState {
  courses: Course[];
  assessmentsBySlug: Record<string, AssessmentItem[]>;
  dashboard: DashboardData | null;
  loading: boolean;
  fetchCourses: () => Promise<Course[]>;
  fetchAssessments: (slug: string) => Promise<AssessmentItem[]>;
  fetchDashboard: () => Promise<DashboardData>;
  markCourseCompleted: (slug: string) => void;
  reset: () => void;
}

export const useCourseStore = create<CourseState>((set, get) => ({
  courses: [],
  assessmentsBySlug: {},
  dashboard: null,
  loading: false,

  fetchCourses: async () => {
    set({ loading: true });
    try {
      const raw = await coursesApi.list();
      const userId = useAuthStore.getState().user?.id;
      const resolved = resolveCourseUnlocks(raw, userId);
      set({ courses: resolved });
      return resolved;
    } finally {
      set({ loading: false });
    }
  },

  fetchAssessments: async (slug) => {
    const items = await coursesApi.assessments(slug);
    set({ assessmentsBySlug: { ...get().assessmentsBySlug, [slug]: items } });
    return items;
  },

  fetchDashboard: async () => {
    const dashboard = await coursesApi.dashboard();
    set({ dashboard });
    return dashboard;
  },

  markCourseCompleted: (slug: string) => {
    const userId = useAuthStore.getState().user?.id;
    markCourseCompletedInStorage(slug, userId);
    const updated = resolveCourseUnlocks(get().courses, userId);
    set({ courses: updated });
  },

  reset: () => set({ courses: [], assessmentsBySlug: {}, dashboard: null }),
}));

