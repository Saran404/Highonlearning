import { create } from 'zustand';
import type { AttemptState, MalpracticeType, Question } from '../types';

export interface LocalAnswer {
  selected: number | null;
  marked: boolean;
}

interface AttemptStoreState {
  attemptId: number | null;
  title: string;
  questions: Question[];
  answers: Record<number, LocalAnswer>;
  currentIndex: number;
  deadlineMs: number;
  /** server clock minus client clock, so the countdown follows the server. */
  offsetMs: number;
  chosenMinutes: number;
  defaultMinutes: number;
  extended: boolean;
  violations: number;
  maxViolations: number;
  lastViolation: MalpracticeType | null;
  lockdown: boolean;
  proctoring: boolean;
  /** question ids whose latest answer has not been confirmed by the server yet */
  dirty: number[];

  init: (state: AttemptState) => void;
  select: (questionId: number, index: number | null) => void;
  toggleMark: (questionId: number) => void;
  goTo: (index: number) => void;
  setDeadline: (iso: string) => void;
  setExtended: () => void;
  setViolations: (count: number, type: MalpracticeType | null) => void;
  markClean: (questionId: number) => void;
  reset: () => void;
}

const empty = {
  attemptId: null,
  title: '',
  questions: [] as Question[],
  answers: {} as Record<number, LocalAnswer>,
  currentIndex: 0,
  deadlineMs: 0,
  offsetMs: 0,
  chosenMinutes: 0,
  defaultMinutes: 0,
  extended: false,
  violations: 0,
  maxViolations: 3,
  lastViolation: null as MalpracticeType | null,
  lockdown: true,
  proctoring: true,
  dirty: [] as number[],
};

export const useAttemptStore = create<AttemptStoreState>((set, get) => ({
  ...empty,

  init: (s) => {
    const answers: Record<number, LocalAnswer> = {};
    s.saved_answers.forEach((a) => {
      answers[a.question_id] = { selected: a.selected_index, marked: a.marked_for_review };
    });
    set({
      ...empty,
      attemptId: s.attempt_id,
      title: s.assessment_title,
      questions: s.questions,
      answers,
      deadlineMs: Date.parse(s.deadline_at),
      offsetMs: Date.parse(s.server_time) - Date.now(),
      chosenMinutes: s.chosen_duration_minutes,
      defaultMinutes: s.default_duration_minutes,
      extended: s.extended,
      violations: s.malpractice_count,
      maxViolations: s.max_malpractice,
      lockdown: s.lockdown_enabled,
      proctoring: s.proctoring_enabled,
    });
  },

  select: (questionId, index) => {
    const prev = get().answers[questionId] ?? { selected: null, marked: false };
    const dirty = get().dirty.includes(questionId) ? get().dirty : [...get().dirty, questionId];
    set({ answers: { ...get().answers, [questionId]: { ...prev, selected: index } }, dirty });
  },

  toggleMark: (questionId) => {
    const prev = get().answers[questionId] ?? { selected: null, marked: false };
    const dirty = get().dirty.includes(questionId) ? get().dirty : [...get().dirty, questionId];
    set({ answers: { ...get().answers, [questionId]: { ...prev, marked: !prev.marked } }, dirty });
  },

  goTo: (index) => set({ currentIndex: Math.min(Math.max(0, index), Math.max(0, get().questions.length - 1)) }),
  setDeadline: (iso) => set({ deadlineMs: Date.parse(iso) }),
  setExtended: () => set({ extended: true }),
  setViolations: (violations, lastViolation) => set({ violations, lastViolation }),
  markClean: (questionId) => set({ dirty: get().dirty.filter((id) => id !== questionId) }),
  reset: () => set({ ...empty }),
}));
