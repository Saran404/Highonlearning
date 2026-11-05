/* ============================================================================
   ExamPro LMS - reference & operational queries
   These are the same queries the API runs (via SQLAlchemy) plus a few
   handy ones for DBAs. Replace the @variables before running.
   ============================================================================ */
USE ExamProLMS;
GO

/* 1. RANK of a finished attempt (used on submit) ------------------------------ */
DECLARE @aid INT = 1, @myScore INT = 4, @myTime INT = 900;
SELECT COUNT(*) + 1 AS RankPosition
FROM   dbo.Attempts a2
WHERE  a2.AssessmentId = @aid
  AND  a2.Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED')
  AND (a2.Score > @myScore OR (a2.Score = @myScore AND a2.TimeTakenSec < @myTime));

/* 2. LEADERBOARD - top 50 for one assessment ---------------------------------- */
SELECT TOP 50 u.Name, a.Score, a.Total, a.Percentage, a.TimeTakenSec, a.RankPosition
FROM   dbo.Attempts a
JOIN   dbo.Users u ON u.UserId = a.UserId
WHERE  a.AssessmentId = @aid
  AND  a.Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED')
ORDER BY a.Score DESC, a.TimeTakenSec ASC;

/* 3. Same thing using the view (also shows total participants) ---------------- */
SELECT TOP 50 * FROM dbo.vw_AssessmentRanking WHERE AssessmentId = @aid ORDER BY LiveRank, Name;

/* 4. STUDENT DASHBOARD - one row per graded assessment ------------------------ */
DECLARE @uid INT = 2;
SELECT  c.Title AS Course, s.Title AS Assessment, s.OrderIndex,
        a.AttemptId, a.Status, a.Score, a.Total, a.Percentage, a.TimeTakenSec,
        (SELECT COUNT(*) + 1 FROM dbo.Attempts b
          WHERE b.AssessmentId = s.AssessmentId
            AND b.Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED')
            AND (b.Score > a.Score OR (b.Score = a.Score AND b.TimeTakenSec < a.TimeTakenSec))) AS LiveRank,
        (SELECT COUNT(*) FROM dbo.Attempts b
          WHERE b.AssessmentId = s.AssessmentId
            AND b.Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED')) AS TotalParticipants
FROM    dbo.Assessments s
JOIN    dbo.Courses c ON c.CourseId = s.CourseId
LEFT JOIN dbo.Attempts a ON a.AssessmentId = s.AssessmentId AND a.UserId = @uid AND a.IsGraded = 1
WHERE   s.AttemptType = N'GRADED'
ORDER BY c.OrderIndex, s.OrderIndex;

/* 5. SEQUENTIAL UNLOCK - is the previous graded assessment finished? ---------- */
SELECT  s.AssessmentId, s.Title, s.OrderIndex,
        CASE
            WHEN a.Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED') THEN N'COMPLETED'
            WHEN a.Status = N'IN_PROGRESS' THEN N'IN_PROGRESS'
            WHEN s.SequentialUnlock = 0 THEN N'AVAILABLE'
            WHEN prev.AssessmentId IS NULL THEN N'AVAILABLE'                       -- first in the course
            WHEN pa.Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED') THEN N'AVAILABLE'
            ELSE N'LOCKED'
        END AS LockStatus
FROM    dbo.Assessments s
LEFT JOIN dbo.Attempts a ON a.AssessmentId = s.AssessmentId AND a.UserId = @uid AND a.IsGraded = 1
OUTER APPLY (SELECT TOP 1 p.AssessmentId FROM dbo.Assessments p
              WHERE p.CourseId = s.CourseId AND p.AttemptType = N'GRADED' AND p.OrderIndex < s.OrderIndex
              ORDER BY p.OrderIndex DESC) prev
LEFT JOIN dbo.Attempts pa ON pa.AssessmentId = prev.AssessmentId AND pa.UserId = @uid AND pa.IsGraded = 1
WHERE   s.CourseId = 1 AND s.AttemptType = N'GRADED'
ORDER BY s.OrderIndex;

/* 6. LIVE MONITOR - in-progress attempts with time left ----------------------- */
SELECT  a.AttemptId, u.Name, u.Email, s.Title, a.StartedAt, a.DeadlineAt,
        DATEDIFF(SECOND, SYSUTCDATETIME(), a.DeadlineAt) AS SecondsLeft, a.MalpracticeCount
FROM    dbo.Attempts a
JOIN    dbo.Users u ON u.UserId = a.UserId
JOIN    dbo.Assessments s ON s.AssessmentId = a.AssessmentId
WHERE   a.Status = N'IN_PROGRESS'
ORDER BY a.StartedAt;

/* 7. MALPRACTICE ALERTS - latest 100 ----------------------------------------- */
SELECT TOP 100 m.LogId, m.AttemptId, u.Email, m.Type, m.OccurredAt, a.MalpracticeCount
FROM   dbo.MalpracticeLogs m
JOIN   dbo.Attempts a ON a.AttemptId = m.AttemptId
JOIN   dbo.Users u    ON u.UserId = a.UserId
ORDER BY m.OccurredAt DESC;

/* 8. ITEM ANALYSIS - how often each question was answered correctly ---------- */
SELECT  q.QuestionId, q.OrderIndex, LEFT(q.QuestionText, 60) AS Question,
        COUNT(an.AnswerId) AS Answered,
        SUM(CASE WHEN an.SelectedIndex = q.CorrectIndex THEN 1 ELSE 0 END) AS Correct,
        CAST(100.0 * SUM(CASE WHEN an.SelectedIndex = q.CorrectIndex THEN 1 ELSE 0 END)
             / NULLIF(COUNT(an.AnswerId), 0) AS DECIMAL(5,2)) AS PercentCorrect
FROM    dbo.Questions q
LEFT JOIN (SELECT x.AnswerId, x.QuestionId, x.SelectedIndex
            FROM dbo.Answers x
            JOIN dbo.Attempts att ON att.AttemptId = x.AttemptId AND att.Status <> N'IN_PROGRESS') an
       ON an.QuestionId = q.QuestionId
WHERE   q.AssessmentId = @aid
GROUP BY q.QuestionId, q.OrderIndex, q.QuestionText
ORDER BY q.OrderIndex;

/* 9. MAINTENANCE -------------------------------------------------------------- */
-- 9a. Sessions idle for more than 7 days can be purged.
DELETE FROM dbo.ActiveSessions WHERE LastSeenAt < DATEADD(DAY, -7, SYSUTCDATETIME());
-- 9b. Attempts that were abandoned (past the longest possible deadline). The API sweeper does this
--     automatically and computes scores; use this query only to see what is pending.
SELECT AttemptId, UserId, AssessmentId, StartedAt, DeadlineAt
FROM   dbo.Attempts
WHERE  Status = N'IN_PROGRESS'
  AND  DATEADD(MINUTE, DefaultDurationMinutes, StartedAt) < DATEADD(MINUTE, -1, SYSUTCDATETIME());
-- 9c. Recompute stored RankPosition for one assessment (ranks go stale as more students finish).
;WITH r AS (
    SELECT AttemptId, RANK() OVER (ORDER BY Score DESC, TimeTakenSec ASC) AS rk
    FROM   dbo.Attempts
    WHERE  AssessmentId = @aid AND Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED')
)
UPDATE a SET RankPosition = r.rk FROM dbo.Attempts a JOIN r ON r.AttemptId = a.AttemptId;
GO
