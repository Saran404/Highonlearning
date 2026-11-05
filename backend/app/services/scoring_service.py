"""Pure scoring helpers (no database access, easy to unit-test)."""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Mapping, Optional


def compute_score(correct_by_question: Mapping[int, int], selected_by_question: Mapping[int, Optional[int]]) -> tuple[int, int]:
    """Return ``(score, total)``.

    ``total`` is the number of questions in the assessment. A question scores 1 when the selected
    index equals the correct index; unanswered (``None`` / missing) and wrong answers score 0.
    Answers for question ids that are not part of the assessment are ignored.
    """
    score = sum(
        1
        for qid, correct in correct_by_question.items()
        if selected_by_question.get(qid) is not None and selected_by_question[qid] == correct
    )
    return score, len(correct_by_question)


def compute_percentage(score: int, total: int) -> Decimal:
    """``score / total * 100`` rounded half-up to 2 decimals (fits ``DECIMAL(5,2)``). 0 when total is 0."""
    if total <= 0:
        return Decimal("0.00")
    return (Decimal(score) * Decimal(100) / Decimal(total)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def is_passed(percentage: Decimal | float, pass_percentage: int) -> bool:
    return float(percentage) >= pass_percentage
