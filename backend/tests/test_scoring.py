"""Scoring, percentage and motivation bands."""
from decimal import Decimal

import pytest

from app.services.motivation_service import get_motivation
from app.services.scoring_service import compute_percentage, compute_score, is_passed


def test_score_counts_only_correct_answers():
    correct = {1: 0, 2: 1, 3: 2, 4: 3}
    selected = {1: 0, 2: 0, 3: 2, 4: None}
    assert compute_score(correct, selected) == (2, 4)


def test_unanswered_and_unknown_questions_score_zero():
    assert compute_score({1: 2, 2: 2}, {}) == (0, 2)
    assert compute_score({1: 2}, {99: 2}) == (0, 1)  # answers for foreign questions are ignored


def test_index_zero_is_a_valid_answer():
    assert compute_score({1: 0}, {1: 0}) == (1, 1)


def test_percentage_rounding_and_bounds():
    assert compute_percentage(24, 30) == Decimal("80.00")
    assert compute_percentage(1, 3) == Decimal("33.33")
    assert compute_percentage(2, 3) == Decimal("66.67")
    assert compute_percentage(0, 0) == Decimal("0.00")
    assert compute_percentage(30, 30) == Decimal("100.00")


@pytest.mark.parametrize("pct,passed", [(59.99, False), (60, True), (100, True)])
def test_pass_mark(pct, passed):
    assert is_passed(pct, 60) is passed


@pytest.mark.parametrize("pct,marker", [(95, "Outstanding"), (90, "Outstanding"), (80, "Great job"), (75, "Great job"),
                                        (65, "passed"), (60, "passed"), (45, "Progress"), (40, "Progress"),
                                        (39.99, "beginner"), (0, "beginner")])
def test_motivation_bands(pct, marker):
    assert marker in get_motivation(pct)
