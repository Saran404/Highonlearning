"""Script to create a standalone 'Percentage' Course and reassign percentage assessments."""
from app.database import SessionLocal
from sqlalchemy import text


def run():
    db = SessionLocal()
    try:
        # Check if Percentage course already exists
        row = db.execute(text("SELECT CourseId FROM dbo.Courses WHERE Slug = 'percentage-course' OR Slug = 'percentage'")).fetchone()
        if not row:
            res = db.execute(text("""
                INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)
                OUTPUT INSERTED.CourseId
                VALUES (N'Percentage', N'percentage-course', N'Comprehensive course on Percentage: basics, fractions, percentage increase/decrease, successive changes, and competitive exam questions.', 2)
            """))
            pct_course_id = res.fetchone()[0]
            print(f"Created Course 'Percentage' with CourseId={pct_course_id}")
        else:
            pct_course_id = row[0]
            print(f"Using existing Course 'Percentage' with CourseId={pct_course_id}")

        # Update course description of Quantitative Aptitude to focus on the rest
        db.execute(text("""
            UPDATE dbo.Courses
            SET Description = N'Arithmetic foundations: Time & Work, Profit & Loss, Mixtures, and advanced problem solving.'
            WHERE Slug = 'quantitative-aptitude'
        """))

        # Reassign percentage assessments to the new Percentage course
        db.execute(text(f"""
            UPDATE dbo.Assessments
            SET CourseId = {pct_course_id}
            WHERE Title LIKE '%Percentage%' OR Slug LIKE '%percent%'
        """))

        # Re-index Percentage course assessments
        db.execute(text(f"""
            UPDATE dbo.Assessments SET OrderIndex = 1 WHERE CourseId = {pct_course_id} AND Slug = 'percentage';
            UPDATE dbo.Assessments SET OrderIndex = 2 WHERE CourseId = {pct_course_id} AND Slug = 'percentage-tnpsc-assessment';
            UPDATE dbo.Assessments SET OrderIndex = 3 WHERE CourseId = {pct_course_id} AND Slug = 'percentage-practice';
            UPDATE dbo.Assessments SET OrderIndex = 4 WHERE CourseId = {pct_course_id} AND Slug = 'percentage-tnpsc-worked-examples';
        """))

        # Re-index Quantitative Aptitude assessments
        db.execute(text("""
            UPDATE dbo.Assessments SET OrderIndex = 1 WHERE Slug = 'time-and-work';
            UPDATE dbo.Assessments SET OrderIndex = 2 WHERE Slug = 'profit-and-loss';
            UPDATE dbo.Assessments SET OrderIndex = 3 WHERE Slug = 'mixtures';
        """))

        # Enroll all existing users into the new Percentage course
        users = db.execute(text("SELECT UserId FROM dbo.Users")).fetchall()
        for (uid,) in users:
            db.execute(text(f"""
                IF NOT EXISTS (SELECT 1 FROM dbo.Enrollments WHERE UserId = {uid} AND CourseId = {pct_course_id})
                BEGIN
                    INSERT INTO dbo.Enrollments (UserId, CourseId, EnrolledAt)
                    VALUES ({uid}, {pct_course_id}, SYSUTCDATETIME())
                END
            """))

        db.commit()
        print("Successfully migrated Percentage into its own course and updated enrollments!")
    except Exception as e:
        db.rollback()
        print("Error during migration:", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
