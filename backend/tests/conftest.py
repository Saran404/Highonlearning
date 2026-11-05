"""Shared fixtures: an in-memory SQLite database that mirrors the ORM models.

The production database is SQL Server, but the scoring/rank/malpractice logic is plain SQLAlchemy,
so SQLite is enough to exercise it without an ODBC driver.
"""
from __future__ import annotations

import json
import os

os.environ.setdefault("ENVIRONMENT", "test")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.constants import ATTEMPT_SUBMITTED
from app.models import Assessment, Attempt, Base, Course, Question, User
from app.schemas.attempt import Acknowledgments, StartAttemptRequest
from app.utils.time import utcnow


@pytest.fixture()
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


_counter = {"n": 0}


def make_user(db, role: str = "STUDENT") -> User:
    _counter["n"] += 1
    n = _counter["n"]
    user = User(name=f"User {n}", email=f"user{n}@exampro.test", hashed_password="x", role=role, is_active=True)
    db.add(user)
    db.commit()
    return user


def make_course(db, slug: str = "course-1") -> Course:
    course = Course(title=slug, slug=slug, order_index=1)
    db.add(course)
    db.commit()
    return course


def make_assessment(db, course: Course, order: int = 1, *, kind: str = "GRADED", questions: int = 4,
                    default: int = 30, minimum: int = 10, sequential: bool = True) -> Assessment:
    a = Assessment(course_id=course.course_id, title=f"Test {order}", slug=f"{course.slug}-t{order}-{kind.lower()}",
                   default_duration_minutes=default, min_duration_minutes=minimum, total_questions=questions,
                   pass_percentage=60, attempt_type=kind, sequential_unlock=sequential, lockdown_enabled=True,
                   proctoring_enabled=True, order_index=order)
    db.add(a)
    db.commit()
    for i in range(questions):
        db.add(Question(assessment_id=a.assessment_id, question_text=f"Q{i + 1}", options_json=json.dumps(["a", "b", "c", "d"]),
                        correct_index=1, explanation="because", order_index=i + 1))
    db.commit()
    return a


def make_finished_attempt(db, user: User, assessment: Assessment, *, score: int, time_taken: int,
                          status: str = ATTEMPT_SUBMITTED) -> Attempt:
    now = utcnow()
    att = Attempt(user_id=user.user_id, assessment_id=assessment.assessment_id, status=status,
                  chosen_duration_minutes=30, default_duration_minutes=30, started_at=now, deadline_at=now,
                  submitted_at=now, time_taken_sec=time_taken, score=score, total=4, percentage=score * 25,
                  malpractice_count=0, extended_duration=False, is_graded=True)
    db.add(att)
    db.commit()
    return att


def start_request(assessment: Assessment, minutes: int | None = None, **ack) -> StartAttemptRequest:
    flags = {"no_minimize": True, "consent_camera": True, "single_attempt": True, **ack}
    return StartAttemptRequest(assessment_id=assessment.assessment_id,
                               chosen_duration_minutes=minutes or assessment.default_duration_minutes,
                               acknowledgments=Acknowledgments(**flags))
