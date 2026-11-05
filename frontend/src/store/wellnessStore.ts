import { create } from 'zustand';
import {
  CATEGORY_CONFIG,
  CategoryMeta,
  getRandomWellnessQuote,
  WellnessCategory,
} from '../utils/wellnessQuotes';

const SESSION_START_KEY = 'exampro_session_start_time';
const LAST_TRIGGERS_KEY = 'exampro_wellness_triggers';

export interface ActiveReminder {
  id: string;
  category: WellnessCategory;
  quote: string;
  config: CategoryMeta;
  elapsedMinutes: number;
  triggeredAt: number;
}

interface LastTriggers {
  eyeCare: number;
  hydration: number;
  movement: number;
  mental: number;
  lastAnyTime: number;
}

interface WellnessState {
  sessionStartTime: number | null;
  elapsedSeconds: number;
  elapsedMinutes: number;
  activeReminder: ActiveReminder | null;
  isEndOfSessionOpen: boolean;
  onLogoutConfirmed: (() => void) | null;
  endOfSessionQuote: string;
  isAssessmentActive: boolean;

  // Actions
  initSession: () => void;
  resetSession: () => void;
  setAssessmentActive: (active: boolean) => void;
  checkIntervals: () => void;
  dismissReminder: () => void;
  triggerManualReminder: (category: WellnessCategory) => void;
  triggerEndOfSession: (onConfirm: () => void) => void;
  dismissEndOfSession: () => void;
  fastForwardMinutes: (minutes: number) => void;
}

function loadSessionStartTime(): number {
  try {
    const stored = sessionStorage.getItem(SESSION_START_KEY);
    if (stored) {
      const parsed = parseInt(stored, 10);
      if (!isNaN(parsed) && parsed > 0 && parsed <= Date.now()) {
        return parsed;
      }
    }
  } catch {
    /* storage unavailable */
  }
  const now = Date.now();
  try {
    sessionStorage.setItem(SESSION_START_KEY, String(now));
  } catch {
    /* noop */
  }
  return now;
}

function loadLastTriggers(): LastTriggers {
  try {
    const raw = sessionStorage.getItem(LAST_TRIGGERS_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    /* noop */
  }
  return {
    eyeCare: 0,
    hydration: 0,
    movement: 0,
    mental: 0,
    lastAnyTime: 0,
  };
}

function saveLastTriggers(data: LastTriggers): void {
  try {
    sessionStorage.setItem(LAST_TRIGGERS_KEY, JSON.stringify(data));
  } catch {
    /* noop */
  }
}

export const useWellnessStore = create<WellnessState>((set, get) => ({
  sessionStartTime: null,
  elapsedSeconds: 0,
  elapsedMinutes: 0,
  activeReminder: null,
  isEndOfSessionOpen: false,
  onLogoutConfirmed: null,
  endOfSessionQuote: '',
  isAssessmentActive: false,

  setAssessmentActive: (active: boolean) => {
    set({ isAssessmentActive: active });
    if (active) {
      set({ activeReminder: null });
    }
  },

  initSession: () => {
    const startTime = loadSessionStartTime();
    const elapsedSec = Math.floor((Date.now() - startTime) / 1000);
    const elapsedMin = Math.floor(elapsedSec / 60);
    set({
      sessionStartTime: startTime,
      elapsedSeconds: elapsedSec,
      elapsedMinutes: elapsedMin,
    });
  },

  resetSession: () => {
    try {
      sessionStorage.removeItem(SESSION_START_KEY);
      sessionStorage.removeItem(LAST_TRIGGERS_KEY);
    } catch {
      /* noop */
    }
    set({
      sessionStartTime: null,
      elapsedSeconds: 0,
      elapsedMinutes: 0,
      activeReminder: null,
      isEndOfSessionOpen: false,
      onLogoutConfirmed: null,
      isAssessmentActive: false,
    });
  },

  checkIntervals: () => {
    const { sessionStartTime, activeReminder, isEndOfSessionOpen, isAssessmentActive } = get();
    // Do not trigger wellness reminders during assessments or when session wrap-up is open
    if (!sessionStartTime || isEndOfSessionOpen || isAssessmentActive) return;

    const now = Date.now();
    const elapsedSec = Math.max(0, Math.floor((now - sessionStartTime) / 1000));
    const elapsedMin = Math.floor(elapsedSec / 60);

    set({ elapsedSeconds: elapsedSec, elapsedMinutes: elapsedMin });

    // If a reminder is already active, don't overlap with another
    if (activeReminder) return;

    const triggers = loadLastTriggers();

    // Spam-prevention cooldown: minimum 2 minutes between any automatic reminders
    const cooldownMs = 2 * 60 * 1000;
    if (triggers.lastAnyTime && now - triggers.lastAnyTime < cooldownMs) {
      return;
    }

    let categoryToTrigger: WellnessCategory | null = null;

    // Trigger Priority & Intervals:
    // 1. Eye care: Every 20 minutes (20, 40, 60, 80...)
    if (elapsedMin >= 20 && elapsedMin - triggers.eyeCare >= 20) {
      categoryToTrigger = 'EYE_CARE';
      triggers.eyeCare = elapsedMin;
    }
    // 2. Hydration & Nutrition: Every 30-45 minutes (chosen interval: 35 minutes)
    else if (elapsedMin >= 35 && elapsedMin - triggers.hydration >= 35) {
      categoryToTrigger = 'HYDRATION';
      triggers.hydration = elapsedMin;
    }
    // 3. Movement & Stretching: Every 45-60 minutes (chosen interval: 50 minutes)
    else if (elapsedMin >= 50 && elapsedMin - triggers.movement >= 50) {
      categoryToTrigger = 'MOVEMENT';
      triggers.movement = elapsedMin;
    }
    // 4. Long Session Logic: If session exceeds 60 minutes, trigger Mental Well-being periodically (every 45 mins after first hour)
    else if (
      elapsedMin >= 60 &&
      (triggers.mental === 0 || elapsedMin - triggers.mental >= 45)
    ) {
      categoryToTrigger = 'MENTAL_WELLBEING';
      triggers.mental = elapsedMin;
    }

    if (categoryToTrigger) {
      triggers.lastAnyTime = now;
      saveLastTriggers(triggers);

      const quote = getRandomWellnessQuote(categoryToTrigger);
      const config = CATEGORY_CONFIG[categoryToTrigger];

      set({
        activeReminder: {
          id: `${categoryToTrigger}-${now}`,
          category: categoryToTrigger,
          quote,
          config,
          elapsedMinutes: elapsedMin,
          triggeredAt: now,
        },
      });
    }
  },

  dismissReminder: () => {
    set({ activeReminder: null });
  },

  triggerManualReminder: (category: WellnessCategory) => {
    if (get().isAssessmentActive) return;
    const { elapsedMinutes } = get();
    const quote = getRandomWellnessQuote(category);
    const config = CATEGORY_CONFIG[category];
    const now = Date.now();

    set({
      activeReminder: {
        id: `manual-${category}-${now}`,
        category,
        quote,
        config,
        elapsedMinutes: elapsedMinutes || 1,
        triggeredAt: now,
      },
    });
  },

  triggerEndOfSession: (onConfirm: () => void) => {
    const quote = getRandomWellnessQuote('END_OF_SESSION');
    set({
      isEndOfSessionOpen: true,
      onLogoutConfirmed: onConfirm,
      endOfSessionQuote: quote,
      activeReminder: null, // close any toast so modal has full focus
    });
  },

  dismissEndOfSession: () => {
    set({ isEndOfSessionOpen: false, onLogoutConfirmed: null });
  },

  fastForwardMinutes: (minutes: number) => {
    const { sessionStartTime } = get();
    const currentStart = sessionStartTime || Date.now();
    const adjustedStart = currentStart - minutes * 60 * 1000;
    try {
      sessionStorage.setItem(SESSION_START_KEY, String(adjustedStart));
    } catch {
      /* noop */
    }
    set({ sessionStartTime: adjustedStart });
    get().checkIntervals();
  },
}));
