"""Import every model so ``Base.metadata`` is complete."""
from app.models.answer import Answer
from app.models.assessment import Assessment
from app.models.attempt import Attempt
from app.models.audit_log import AuditLog
from app.models.base import Base
from app.models.course import Course
from app.models.course_reflection import CourseReflection
from app.models.enrollment import Enrollment
from app.models.malpractice_log import MalpracticeLog
from app.models.proctoring_snapshot import ProctoringSnapshot
from app.models.question import Question
from app.models.session import ActiveSession
from app.models.user import User

__all__ = [
    "ActiveSession", "Answer", "Assessment", "Attempt", "AuditLog", "Base", "Course",
    "CourseReflection", "Enrollment", "MalpracticeLog", "ProctoringSnapshot", "Question", "User",
]
