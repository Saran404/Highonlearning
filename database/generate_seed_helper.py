import json

def sql_escape(s):
    if s is None:
        return 'NULL'
    return "N'" + s.replace("'", "''") + "'"

def generate_sql():
    sql = """/* ============================================================================
   ExamPro LMS - Percentage Course Seed Script (Bilingual: English & Tamil)
   - 1 Course: Percentage / சதவீதம்
   - 4 Assessments:
       1. Percentage - Practice Set (English)   [60 Questions: 30 Worked + 30 Independent]
       2. Percentage - Graded Assessment (English) [30 Questions: Assessment Q1-30]
       3. சதவீதம் - பயிற்சித் தொகுப்பு (Tamil)      [60 Questions: 30 Worked + 30 Independent]
       4. சதவீதம் - மதிப்பீட்டுத் தேர்வு (Tamil)     [30 Questions: Assessment Q1-30]
   ============================================================================ */
USE ExamProLMS;
GO
SET QUOTED_IDENTIFIER ON;
GO

BEGIN TRANSACTION;

-- Clean existing Percentage course if present
DELETE FROM dbo.Courses WHERE Slug IN (N'percentage', N'quantitative-aptitude');

-- Insert Course
INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)
VALUES (
    N'Percentage / சதவீதம்',
    N'percentage',
    N'Comprehensive arithmetic module on percentages for TNPSC Group 1, UPSC CSAT, SSC CGL & Banking exams in English & Tamil.',
    1
);

DECLARE @CourseId INT = SCOPE_IDENTITY();

-- Insert Assessments
INSERT INTO dbo.Assessments (
    CourseId, Title, Slug, Description, Topic, Difficulty,
    DefaultDurationMinutes, MinDurationMinutes, TotalQuestions, PassPercentage,
    AttemptType, SequentialUnlock, LockdownEnabled, ProctoringEnabled, OrderIndex
)
VALUES
    (@CourseId, N'Percentage - Practice Set', N'percentage-practice-en', N'60 practice questions (Worked Examples + Independent Practice) with instant feedback & step-by-step solutions.', N'Percentage', N'EASY', 60, 10, 60, 0, N'PRACTICE', 0, 0, 0, 1),
    (@CourseId, N'Percentage - Graded Assessment', N'percentage-graded-en', N'Official proctored & timed assessment on Percentage (30 Questions). Pass with 60% to master this topic.', N'Percentage', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 2),
    (@CourseId, N'சதவீதம் - பயிற்சித் தொகுப்பு (Tamil)', N'percentage-practice-ta', N'60 பயிற்சிக் கணக்குகள் (தீர்க்கப்பட்ட எடுத்துக்காட்டுகள் + சுயப்பயிற்சி) உடனடித் தீர்வுகளுடன்.', N'சதவீதம்', N'EASY', 60, 10, 60, 0, N'PRACTICE', 0, 0, 0, 3),
    (@CourseId, N'சதவீதம் - மதிப்பீட்டுத் தேர்வு (Tamil)', N'percentage-graded-ta', N'சதவீதத்திற்கான அதிகாரப்பூர்வக் கண்காணிப்புடன் கூடிய தேர்வு (30 வினாக்கள்). தேர்ச்சி 60%.', N'சதவீதம்', N'MEDIUM', 45, 15, 30, 60, N'GRADED', 1, 1, 1, 4);

DECLARE @prac_en INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage-practice-en');
DECLARE @grad_en INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage-graded-en');
DECLARE @prac_ta INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage-practice-ta');
DECLARE @grad_ta INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage-graded-ta');
"""

    return sql

print("Helper ready")
