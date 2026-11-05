"""Practice mode: stateless, instant feedback, never touches the Attempts table.

Every lookup is restricted to PRACTICE assessments - otherwise this endpoint could be used to read
the answers of graded questions.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.constants import LOCK_LOCKED, TYPE_PRACTICE
from app.core.exceptions import ForbiddenError, NotFoundError
from app.models import Assessment, Course, Question
from app.schemas.practice import PracticeAnswerResponse
from app.services import attempt_service, catalog_service


def practice_questions(db: Session, user_id: int, assessment_id: int) -> list[Question]:
    assessment = db.get(Assessment, assessment_id)
    if assessment is None:
        raise NotFoundError("Assessment not found.", code="ASSESSMENT_NOT_FOUND")
    if assessment.attempt_type != TYPE_PRACTICE:
        raise ForbiddenError("This is a graded assessment.", code="NOT_PRACTICE")
    course = getattr(assessment, "course", None) or db.get(Course, assessment.course_id)
    if course is not None:
        c_status, prev_title, _ = catalog_service.course_lock_status(db, user_id, course)
        if c_status == LOCK_LOCKED:
            raise ForbiddenError(
                f"Complete {prev_title or 'the previous course'} before accessing practice sets in this course.",
                code="COURSE_LOCKED",
                details={"previous_course": prev_title},
            )
    catalog_service.ensure_enrolled(db, user_id, assessment.course_id)
    db.commit()
    return attempt_service.load_questions(db, assessment_id)


def check_answer(db: Session, question_id: int, selected_index: int) -> PracticeAnswerResponse:
    row = db.execute(
        select(Question, Assessment.attempt_type).join(Assessment, Assessment.assessment_id == Question.assessment_id)
        .where(Question.question_id == question_id)
    ).first()
    if row is None:
        raise NotFoundError("Question not found.", code="QUESTION_NOT_FOUND")
    question, attempt_type = row
    if attempt_type != TYPE_PRACTICE:
        raise ForbiddenError("Instant feedback is only available in practice mode.", code="NOT_PRACTICE")
    return PracticeAnswerResponse(
        correct=selected_index == question.correct_index,
        correct_index=question.correct_index,
        explanation=question.explanation or "",
        explanation_ta=getattr(question, "explanation_ta", None) or "",
        selected_index=selected_index,
    )
