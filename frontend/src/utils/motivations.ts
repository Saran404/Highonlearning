/** Score-banded messages (mirrors the backend) and a daily quote for the dashboard. */
export function getMotivation(pct: number): string {
  if (pct >= 90) return "🌟 Outstanding! You're in the top tier. Keep this momentum — the exam hall will feel easy.";
  if (pct >= 75) return "💪 Great job! You're strong. Focus on the few misses — that's where the next leap comes from.";
  if (pct >= 60) return '✅ You passed! Solid foundation. Review the solutions carefully — mastery is a few revisions away.';
  if (pct >= 40) return '📈 Progress is progress. Every mistake here is a lesson learned. Revisit and practice again.';
  return "🌱 Every expert was once a beginner. This attempt showed you exactly what to study next. Don't quit.";
}

const QUOTES = [
  'One focused hour today beats three distracted ones.',
  'Revise what you got wrong. That is where the marks are hiding.',
  'Speed comes from accuracy. Accuracy comes from repetition.',
  'A mock test is a rehearsal. Treat it like the real hall.',
  'Small daily practice compounds into rank.',
  'Read the question twice, answer once.',
  'Consistency is the most underrated exam skill.',
];

export function dailyQuote(date = new Date()): string {
  const day = Math.floor(date.getTime() / 86_400_000);
  return QUOTES[day % QUOTES.length];
}
