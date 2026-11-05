"""Score-banded motivational messages."""
from __future__ import annotations


def get_motivation(score_pct: float) -> str:
    """Return the message for a percentage score (0-100)."""
    if score_pct >= 90:
        return "🌟 Outstanding! You're in the top tier. Keep this momentum — the exam hall will feel easy."
    if score_pct >= 75:
        return "💪 Great job! You're strong. Focus on the few misses — that's where the next leap comes from."
    if score_pct >= 60:
        return "✅ You passed! Solid foundation. Review the solutions carefully — mastery is a few revisions away."
    if score_pct >= 40:
        return "📈 Progress is progress. Every mistake here is a lesson learned. Revisit and practice again."
    return "🌱 Every expert was once a beginner. This attempt showed you exactly what to study next. Don't quit."
