from __future__ import annotations

from app.schemas.reflection import ReflectionAnswerItem
from app.services import reflection_service
from tests.conftest import make_course, make_user


def test_reflection_submission_and_retrieval(db):
    user = make_user(db)
    course = make_course(db, slug="percentage")

    # Initial state: not submitted
    res1 = reflection_service.get_user_course_reflection(db, user.user_id, "percentage")
    assert res1.submitted is False
    assert len(res1.answers) == 0

    answers = [
        ReflectionAnswerItem(
            question_number=1,
            question="Which type of multi-step percentage question did you find most challenging?",
            selected_option="Successive percentage changes (two or more steps)",
        ),
        ReflectionAnswerItem(
            question_number=2,
            question="Which strategy helped you solve multi-step percentage problems more efficiently?",
            selected_option="Converting each percentage change into a multiplying factor",
        ),
    ]

    # Save reflection
    res2 = reflection_service.save_user_course_reflection(db, user.user_id, "percentage", answers)
    assert res2.submitted is True
    assert len(res2.answers) == 2
    assert res2.answers[0].selected_option == "Successive percentage changes (two or more steps)"

    # Retrieve again
    res3 = reflection_service.get_user_course_reflection(db, user.user_id, "percentage")
    assert res3.submitted is True
    assert len(res3.answers) == 2

    # Admin listing
    admin_list = reflection_service.list_admin_reflections(db)
    assert len(admin_list) >= 1
    user_item = next(u for u in admin_list if u.user_id == user.user_id)
    assert user_item.total_reflections == 1
    assert user_item.courses[0].course_slug == "percentage"
    assert len(user_item.courses[0].answers) == 2
