export type WellnessCategory =
  | 'EYE_CARE'
  | 'HYDRATION'
  | 'MOVEMENT'
  | 'MENTAL_WELLBEING'
  | 'REST_SLEEP'
  | 'MOTIVATION'
  | 'END_OF_SESSION';

export interface CategoryMeta {
  category: WellnessCategory;
  title: string;
  badge: string;
  actionTip: string;
  colorTheme: {
    bgLight: string;
    border: string;
    badgeBg: string;
    badgeText: string;
    accent: string;
    button: string;
  };
}

export const WELLNESS_QUOTES: Record<WellnessCategory, string[]> = {
  EYE_CARE: [
    'Give your eyes a little rest!',
    'Look away from the screen!',
    'Blink often, relax your eyes!',
    'Follow the 20-20-20 rule!',
    'Your eyes deserve a break!',
  ],
  HYDRATION: [
    'Time to drink some water! 💧',
    'Stay hydrated, stay focused!',
    'Take a quick water break!',
    'A sip of water, a fresh start!',
    'Keep your water bottle nearby!',
    // Nutrition quotes mapped into hydration / fuel
    'Eat healthy, think clearly!',
    'Fuel your brain with nutritious food!',
    'Choose fruits for a healthy snack!',
    'Don\'t skip your meals!',
    'Healthy food, healthy mind!',
  ],
  MOVEMENT: [
    'Stand up and stretch!',
    'Take a short movement break!',
    'Relax your neck and shoulders!',
    'Check your sitting posture!',
    'Move a little, feel refreshed!',
  ],
  MENTAL_WELLBEING: [
    'Breathe in, breathe out!',
    'Pause, relax, and restart!',
    'Your mental health matters!',
    'It\'s okay to take a break!',
    'Stay calm and keep learning!',
  ],
  REST_SLEEP: [
    'Rest well, learn better!',
    'Quality sleep supports memory!',
    'Avoid late-night screen time!',
    'Give your brain time to recharge!',
    'Sleep is part of success!',
  ],
  MOTIVATION: [
    'Small steps lead to big success!',
    'Stay consistent, not stressed!',
    'Focus on progress, not perfection!',
    'Celebrate your small achievements!',
    'A refreshed mind learns better!',
  ],
  END_OF_SESSION: [
    // Rest/Sleep quotes
    'Rest well, learn better!',
    'Quality sleep supports memory!',
    'Avoid late-night screen time!',
    'Give your brain time to recharge!',
    'Sleep is part of success!',
    // Motivation quotes
    'Small steps lead to big success!',
    'Stay consistent, not stressed!',
    'Focus on progress, not perfection!',
    'Celebrate your small achievements!',
    'A refreshed mind learns better!',
  ],
};

export const CATEGORY_CONFIG: Record<WellnessCategory, CategoryMeta> = {
  EYE_CARE: {
    category: 'EYE_CARE',
    title: 'Eye Care Reminder',
    badge: '20-20-20 Rule',
    actionTip: 'Look at something 20 feet away for 20 seconds to reduce screen fatigue.',
    colorTheme: {
      bgLight: 'bg-sky-50/90',
      border: 'border-sky-300',
      badgeBg: 'bg-sky-100',
      badgeText: 'text-sky-800',
      accent: 'text-sky-600',
      button: 'bg-sky-600 hover:bg-sky-700 text-white',
    },
  },
  HYDRATION: {
    category: 'HYDRATION',
    title: 'Hydration & Nutrition',
    badge: 'Hydrate & Refuel',
    actionTip: 'Drink a glass of water and nourish your brain for peak concentration.',
    colorTheme: {
      bgLight: 'bg-blue-50/90',
      border: 'border-blue-300',
      badgeBg: 'bg-blue-100',
      badgeText: 'text-blue-800',
      accent: 'text-blue-600',
      button: 'bg-blue-600 hover:bg-blue-700 text-white',
    },
  },
  MOVEMENT: {
    category: 'MOVEMENT',
    title: 'Movement & Posture',
    badge: 'Stretch Break',
    actionTip: 'Roll your shoulders, align your spine, and stand up for a 60-second stretch.',
    colorTheme: {
      bgLight: 'bg-emerald-50/90',
      border: 'border-emerald-300',
      badgeBg: 'bg-emerald-100',
      badgeText: 'text-emerald-800',
      accent: 'text-emerald-600',
      button: 'bg-emerald-600 hover:bg-emerald-700 text-white',
    },
  },
  MENTAL_WELLBEING: {
    category: 'MENTAL_WELLBEING',
    title: 'Mental Well-being',
    badge: 'Mindful Pause',
    actionTip: 'Take 3 deep breaths. Inhale for 4 seconds, hold for 4, exhale slowly.',
    colorTheme: {
      bgLight: 'bg-violet-50/90',
      border: 'border-violet-300',
      badgeBg: 'bg-violet-100',
      badgeText: 'text-violet-800',
      accent: 'text-violet-600',
      button: 'bg-violet-600 hover:bg-violet-700 text-white',
    },
  },
  REST_SLEEP: {
    category: 'REST_SLEEP',
    title: 'Rest & Recovery',
    badge: 'Recharge Time',
    actionTip: 'Your brain consolidates memory and learning while resting.',
    colorTheme: {
      bgLight: 'bg-indigo-50/90',
      border: 'border-indigo-300',
      badgeBg: 'bg-indigo-100',
      badgeText: 'text-indigo-800',
      accent: 'text-indigo-600',
      button: 'bg-indigo-600 hover:bg-indigo-700 text-white',
    },
  },
  MOTIVATION: {
    category: 'MOTIVATION',
    title: 'Study Motivation',
    badge: 'Milestone',
    actionTip: 'Every practice problem solved brings you closer to your goal.',
    colorTheme: {
      bgLight: 'bg-amber-50/90',
      border: 'border-amber-300',
      badgeBg: 'bg-amber-100',
      badgeText: 'text-amber-800',
      accent: 'text-amber-600',
      button: 'bg-amber-600 hover:bg-amber-700 text-white',
    },
  },
  END_OF_SESSION: {
    category: 'END_OF_SESSION',
    title: 'Session Wrap-up & Rest',
    badge: 'Great Effort!',
    actionTip: 'Outstanding dedication today. Take time to relax and recharge your mind.',
    colorTheme: {
      bgLight: 'bg-amber-50/95',
      border: 'border-amber-300',
      badgeBg: 'bg-amber-100',
      badgeText: 'text-amber-900',
      accent: 'text-amber-600',
      button: 'bg-navy-900 hover:bg-navy-800 text-white',
    },
  },
};

const lastPickedQuote: Partial<Record<WellnessCategory, string>> = {};

/** Randomly selects a quote from the requested category, avoiding immediate repeating. */
export function getRandomWellnessQuote(category: WellnessCategory): string {
  const quotes = WELLNESS_QUOTES[category] || WELLNESS_QUOTES.MOTIVATION;
  if (quotes.length === 1) return quotes[0];

  const previous = lastPickedQuote[category];
  const candidates = quotes.filter((q) => q !== previous);
  const picked = candidates[Math.floor(Math.random() * candidates.length)] || quotes[0];
  lastPickedQuote[category] = picked;
  return picked;
}
