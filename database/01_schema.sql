/* ============================================================================
   ExamPro LMS - SQL Server schema (T-SQL)
   Run once against SQL Server 2019+ (SSMS, Azure Data Studio or sqlcmd):
       sqlcmd -S localhost -U sa -P "<password>" -C -i 01_schema.sql
   Idempotent: every object is created only if it does not already exist.
   ============================================================================ */
IF DB_ID(N'ExamProLMS') IS NULL
    CREATE DATABASE ExamProLMS;
GO
USE ExamProLMS;
GO
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;   -- required for filtered indexes
GO

/* ---------------------------------------------------------------- Users ---- */
IF OBJECT_ID(N'dbo.Users', N'U') IS NULL
CREATE TABLE dbo.Users (
    UserId          INT IDENTITY(1,1)  NOT NULL CONSTRAINT PK_Users PRIMARY KEY,
    Name            NVARCHAR(150)      NOT NULL,
    Email           NVARCHAR(200)      NOT NULL,
    HashedPassword  NVARCHAR(255)      NOT NULL,
    Role            NVARCHAR(20)       NOT NULL CONSTRAINT DF_Users_Role DEFAULT N'STUDENT',
    AvatarUrl       NVARCHAR(500)      NULL,
    IsActive        BIT                NOT NULL CONSTRAINT DF_Users_IsActive DEFAULT 1,
    CreatedAt       DATETIME2          NOT NULL CONSTRAINT DF_Users_CreatedAt DEFAULT SYSUTCDATETIME(),
    UpdatedAt       DATETIME2          NOT NULL CONSTRAINT DF_Users_UpdatedAt DEFAULT SYSUTCDATETIME(),
    CONSTRAINT UQ_Users_Email UNIQUE (Email),
    CONSTRAINT CK_Users_Role  CHECK (Role IN (N'STUDENT', N'ADMIN', N'INSTRUCTOR'))
);
GO

/* ------------------------------------------------------- ActiveSessions ---- */
IF OBJECT_ID(N'dbo.ActiveSessions', N'U') IS NULL
CREATE TABLE dbo.ActiveSessions (
    SessionId         UNIQUEIDENTIFIER NOT NULL CONSTRAINT PK_ActiveSessions PRIMARY KEY
                                       CONSTRAINT DF_ActiveSessions_Id DEFAULT NEWID(),
    UserId            INT              NOT NULL,
    DeviceId          NVARCHAR(100)    NOT NULL,
    DeviceInfo        NVARCHAR(500)    NULL,
    IpAddress         NVARCHAR(45)     NULL,
    RefreshTokenHash  NVARCHAR(255)    NULL,
    IsRevoked         BIT              NOT NULL CONSTRAINT DF_ActiveSessions_IsRevoked DEFAULT 0,
    CreatedAt         DATETIME2        NOT NULL CONSTRAINT DF_ActiveSessions_CreatedAt DEFAULT SYSUTCDATETIME(),
    LastSeenAt        DATETIME2        NOT NULL CONSTRAINT DF_ActiveSessions_LastSeenAt DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_ActiveSessions_Users FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId) ON DELETE CASCADE
);
CREATE INDEX IX_ActiveSessions_User_Active ON dbo.ActiveSessions (UserId, IsRevoked) INCLUDE (DeviceId, LastSeenAt);
GO

/* -------------------------------------------------------------- Courses ---- */
IF OBJECT_ID(N'dbo.Courses', N'U') IS NULL
CREATE TABLE dbo.Courses (
    CourseId      INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Courses PRIMARY KEY,
    Title         NVARCHAR(200)     NOT NULL,
    Slug          NVARCHAR(200)     NOT NULL,
    Description   NVARCHAR(MAX)     NULL,
    ThumbnailUrl  NVARCHAR(500)     NULL,
    OrderIndex    INT               NOT NULL CONSTRAINT DF_Courses_OrderIndex DEFAULT 0,
    CreatedAt     DATETIME2         NOT NULL CONSTRAINT DF_Courses_CreatedAt DEFAULT SYSUTCDATETIME(),
    CONSTRAINT UQ_Courses_Slug UNIQUE (Slug)
);
GO

/* ---------------------------------------------------------- Assessments ---- */
IF OBJECT_ID(N'dbo.Assessments', N'U') IS NULL
CREATE TABLE dbo.Assessments (
    AssessmentId            INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Assessments PRIMARY KEY,
    CourseId                INT               NOT NULL,
    Title                   NVARCHAR(200)     NOT NULL,
    Slug                    NVARCHAR(200)     NOT NULL,
    Description             NVARCHAR(MAX)     NULL,
    Topic                   NVARCHAR(100)     NULL,
    Difficulty              NVARCHAR(20)      NULL,
    DefaultDurationMinutes  INT               NOT NULL CONSTRAINT DF_Assess_DefDur DEFAULT 60,
    MinDurationMinutes      INT               NOT NULL CONSTRAINT DF_Assess_MinDur DEFAULT 20,
    TotalQuestions          INT               NOT NULL CONSTRAINT DF_Assess_TotalQ DEFAULT 30,
    PassPercentage          INT               NOT NULL CONSTRAINT DF_Assess_Pass DEFAULT 60,
    AttemptType             NVARCHAR(20)      NOT NULL CONSTRAINT DF_Assess_Type DEFAULT N'GRADED',
    SequentialUnlock        BIT               NOT NULL CONSTRAINT DF_Assess_Seq DEFAULT 1,
    LockdownEnabled         BIT               NOT NULL CONSTRAINT DF_Assess_Lock DEFAULT 1,
    ProctoringEnabled       BIT               NOT NULL CONSTRAINT DF_Assess_Proc DEFAULT 1,
    OrderIndex              INT               NOT NULL CONSTRAINT DF_Assess_Order DEFAULT 0,
    CreatedAt               DATETIME2         NOT NULL CONSTRAINT DF_Assess_CreatedAt DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_Assessments_Courses FOREIGN KEY (CourseId) REFERENCES dbo.Courses(CourseId) ON DELETE CASCADE,
    CONSTRAINT UQ_Assessments_Slug UNIQUE (Slug),
    CONSTRAINT CK_Assessments_Type       CHECK (AttemptType IN (N'PRACTICE', N'GRADED')),
    CONSTRAINT CK_Assessments_Difficulty CHECK (Difficulty IS NULL OR Difficulty IN (N'EASY', N'MEDIUM', N'HARD')),
    CONSTRAINT CK_Assessments_Duration   CHECK (MinDurationMinutes > 0 AND MinDurationMinutes <= DefaultDurationMinutes),
    CONSTRAINT CK_Assessments_Pass       CHECK (PassPercentage BETWEEN 0 AND 100)
);
CREATE INDEX IX_Assessments_Course_Order ON dbo.Assessments (CourseId, OrderIndex);
GO

/* ------------------------------------------------------------ Questions ---- */
IF OBJECT_ID(N'dbo.Questions', N'U') IS NULL
CREATE TABLE dbo.Questions (
    QuestionId    INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Questions PRIMARY KEY,
    AssessmentId  INT               NOT NULL,
    QuestionText  NVARCHAR(MAX)     NOT NULL,
    OptionsJson   NVARCHAR(MAX)     NOT NULL,          -- JSON array of 4 strings
    CorrectIndex  INT               NOT NULL,          -- 0..3
    Explanation   NVARCHAR(MAX)     NULL,
    Topic         NVARCHAR(100)     NULL,
    Difficulty    NVARCHAR(20)      NULL,
    OrderIndex    INT               NOT NULL CONSTRAINT DF_Questions_Order DEFAULT 0,
    CONSTRAINT FK_Questions_Assessments FOREIGN KEY (AssessmentId) REFERENCES dbo.Assessments(AssessmentId) ON DELETE CASCADE,
    CONSTRAINT CK_Questions_Correct CHECK (CorrectIndex BETWEEN 0 AND 3),
    CONSTRAINT CK_Questions_Options CHECK (ISJSON(OptionsJson) = 1)
);
CREATE INDEX IX_Questions_Assessment_Order ON dbo.Questions (AssessmentId, OrderIndex);
GO

/* ---------------------------------------------------------- Enrollments ---- */
IF OBJECT_ID(N'dbo.Enrollments', N'U') IS NULL
CREATE TABLE dbo.Enrollments (
    EnrollmentId  INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Enrollments PRIMARY KEY,
    UserId        INT               NOT NULL,
    CourseId      INT               NOT NULL,
    EnrolledAt    DATETIME2         NOT NULL CONSTRAINT DF_Enroll_At DEFAULT SYSUTCDATETIME(),
    CompletedAt   DATETIME2         NULL,
    CONSTRAINT FK_Enrollments_Users   FOREIGN KEY (UserId)   REFERENCES dbo.Users(UserId)     ON DELETE CASCADE,
    CONSTRAINT FK_Enrollments_Courses FOREIGN KEY (CourseId) REFERENCES dbo.Courses(CourseId) ON DELETE CASCADE,
    CONSTRAINT UQ_Enrollments_User_Course UNIQUE (UserId, CourseId)
);
GO

/* ------------------------------------------------------------- Attempts ---- */
IF OBJECT_ID(N'dbo.Attempts', N'U') IS NULL
CREATE TABLE dbo.Attempts (
    AttemptId               BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Attempts PRIMARY KEY,
    UserId                  INT           NOT NULL,
    AssessmentId            INT           NOT NULL,
    Status                  NVARCHAR(20)  NOT NULL CONSTRAINT DF_Attempts_Status DEFAULT N'IN_PROGRESS',
    ChosenDurationMinutes   INT           NOT NULL,
    DefaultDurationMinutes  INT           NOT NULL,
    StartedAt               DATETIME2     NOT NULL,
    DeadlineAt              DATETIME2     NOT NULL,
    SubmittedAt             DATETIME2     NULL,
    TimeTakenSec            INT           NULL,
    Score                   INT           NULL,
    Total                   INT           NULL,
    Percentage              DECIMAL(5,2)  NULL,
    MalpracticeCount        INT           NOT NULL CONSTRAINT DF_Attempts_Malp DEFAULT 0,
    ExtendedDuration        BIT           NOT NULL CONSTRAINT DF_Attempts_Ext  DEFAULT 0,
    RankPosition            INT           NULL,
    MotivationalMessage     NVARCHAR(500) NULL,
    IsGraded                BIT           NOT NULL CONSTRAINT DF_Attempts_Graded DEFAULT 1,
    CreatedAt               DATETIME2     NOT NULL CONSTRAINT DF_Attempts_CreatedAt DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_Attempts_Users       FOREIGN KEY (UserId)       REFERENCES dbo.Users(UserId),
    CONSTRAINT FK_Attempts_Assessments FOREIGN KEY (AssessmentId) REFERENCES dbo.Assessments(AssessmentId),
    CONSTRAINT CK_Attempts_Status CHECK (Status IN (N'IN_PROGRESS', N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED'))
);
-- "Single attempt" rule enforced by the database itself (race-condition proof).
CREATE UNIQUE INDEX UX_Attempts_User_Assessment_Graded
    ON dbo.Attempts (UserId, AssessmentId) WHERE IsGraded = 1;
-- Serves the rank / leaderboard queries.
CREATE INDEX IX_Attempts_Assessment_Rank
    ON dbo.Attempts (AssessmentId, Status, Score DESC, TimeTakenSec ASC) INCLUDE (UserId, Percentage, RankPosition);
CREATE INDEX IX_Attempts_User ON dbo.Attempts (UserId, AssessmentId) INCLUDE (Status);
-- Serves the expired-attempt sweeper.
CREATE INDEX IX_Attempts_InProgress_Started ON dbo.Attempts (StartedAt) WHERE Status = N'IN_PROGRESS';
GO

/* -------------------------------------------------------------- Answers ---- */
IF OBJECT_ID(N'dbo.Answers', N'U') IS NULL
CREATE TABLE dbo.Answers (
    AnswerId        BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_Answers PRIMARY KEY,
    AttemptId       BIGINT     NOT NULL,
    QuestionId      INT        NOT NULL,
    SelectedIndex   INT        NULL,
    MarkedForReview BIT        NOT NULL CONSTRAINT DF_Answers_Mark DEFAULT 0,
    UpdatedAt       DATETIME2  NOT NULL CONSTRAINT DF_Answers_UpdatedAt DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_Answers_Attempts  FOREIGN KEY (AttemptId)  REFERENCES dbo.Attempts(AttemptId) ON DELETE CASCADE,
    CONSTRAINT FK_Answers_Questions FOREIGN KEY (QuestionId) REFERENCES dbo.Questions(QuestionId),
    CONSTRAINT UQ_Answers_Attempt_Question UNIQUE (AttemptId, QuestionId),
    CONSTRAINT CK_Answers_Selected CHECK (SelectedIndex IS NULL OR SelectedIndex BETWEEN 0 AND 3)
);
GO

/* ------------------------------------------------------ MalpracticeLogs ---- */
IF OBJECT_ID(N'dbo.MalpracticeLogs', N'U') IS NULL
CREATE TABLE dbo.MalpracticeLogs (
    LogId         BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_MalpracticeLogs PRIMARY KEY,
    AttemptId     BIGINT        NOT NULL,
    Type          NVARCHAR(30)  NOT NULL,
    OccurredAt    DATETIME2     NOT NULL CONSTRAINT DF_Malp_At DEFAULT SYSUTCDATETIME(),
    MetadataJson  NVARCHAR(MAX) NULL,
    CONSTRAINT FK_Malp_Attempts FOREIGN KEY (AttemptId) REFERENCES dbo.Attempts(AttemptId) ON DELETE CASCADE,
    CONSTRAINT CK_Malp_Type CHECK (Type IN (N'TAB_SWITCH', N'MINIMIZE', N'FULLSCREEN_EXIT', N'DEVTOOLS', N'COPY_PASTE', N'RIGHT_CLICK'))
);
CREATE INDEX IX_Malp_Attempt    ON dbo.MalpracticeLogs (AttemptId, OccurredAt);
CREATE INDEX IX_Malp_OccurredAt ON dbo.MalpracticeLogs (OccurredAt DESC);
GO

/* --------------------------------------------------- ProctoringSnapshots ---- */
IF OBJECT_ID(N'dbo.ProctoringSnapshots', N'U') IS NULL
CREATE TABLE dbo.ProctoringSnapshots (
    SnapshotId      BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_ProctoringSnapshots PRIMARY KEY,
    AttemptId       BIGINT        NOT NULL,
    ImagePath       NVARCHAR(500) NOT NULL,
    CapturedAt      DATETIME2     NOT NULL CONSTRAINT DF_Snap_At DEFAULT SYSUTCDATETIME(),
    TriggerType     NVARCHAR(20)  NOT NULL,
    FaceDetected    BIT           NULL,
    FaceMatchScore  DECIMAL(5,2)  NULL,
    CONSTRAINT FK_Snap_Attempts FOREIGN KEY (AttemptId) REFERENCES dbo.Attempts(AttemptId) ON DELETE CASCADE,
    CONSTRAINT CK_Snap_Trigger CHECK (TriggerType IN (N'START', N'INTERVAL', N'MALPRACTICE', N'END'))
);
CREATE INDEX IX_Snap_Attempt ON dbo.ProctoringSnapshots (AttemptId, CapturedAt);
GO

/* ------------------------------------------------------------ AuditLogs ---- */
IF OBJECT_ID(N'dbo.AuditLogs', N'U') IS NULL
CREATE TABLE dbo.AuditLogs (
    AuditId       BIGINT IDENTITY(1,1) NOT NULL CONSTRAINT PK_AuditLogs PRIMARY KEY,
    AdminUserId   INT           NOT NULL,
    Action        NVARCHAR(100) NOT NULL,
    TargetType    NVARCHAR(50)  NULL,
    TargetId      NVARCHAR(50)  NULL,
    MetadataJson  NVARCHAR(MAX) NULL,
    CreatedAt     DATETIME2     NOT NULL CONSTRAINT DF_Audit_At DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_Audit_Users FOREIGN KEY (AdminUserId) REFERENCES dbo.Users(UserId)
);
CREATE INDEX IX_Audit_Created ON dbo.AuditLogs (CreatedAt DESC);
GO

/* -------------------------------------------------------- CourseReflections ---- */
IF OBJECT_ID(N'dbo.CourseReflections', N'U') IS NULL
CREATE TABLE dbo.CourseReflections (
    ReflectionId     INT IDENTITY(1,1) NOT NULL CONSTRAINT PK_CourseReflections PRIMARY KEY,
    UserId           INT               NOT NULL,
    CourseId         INT               NOT NULL,
    AnswersJson      NVARCHAR(MAX)     NOT NULL,
    CreatedAt        DATETIME2         NOT NULL CONSTRAINT DF_CourseReflections_CreatedAt DEFAULT SYSUTCDATETIME(),
    UpdatedAt        DATETIME2         NOT NULL CONSTRAINT DF_CourseReflections_UpdatedAt DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_CourseReflections_Users FOREIGN KEY (UserId) REFERENCES dbo.Users(UserId) ON DELETE CASCADE,
    CONSTRAINT FK_CourseReflections_Courses FOREIGN KEY (CourseId) REFERENCES dbo.Courses(CourseId) ON DELETE CASCADE,
    CONSTRAINT UQ_CourseReflections_User_Course UNIQUE (UserId, CourseId)
);
CREATE INDEX IX_CourseReflections_User ON dbo.CourseReflections (UserId);
CREATE INDEX IX_CourseReflections_Course ON dbo.CourseReflections (CourseId);
GO

/* -------------------------------------------------------------- Views ------ */
-- Live ranking view. RANK() gives exactly the same result as the API's
-- "COUNT(*) + 1 of better attempts" formula (ties share a rank).
CREATE OR ALTER VIEW dbo.vw_AssessmentRanking AS
SELECT  a.AttemptId, a.AssessmentId, a.UserId, u.Name, a.Score, a.Total, a.Percentage, a.TimeTakenSec, a.Status,
        RANK()   OVER (PARTITION BY a.AssessmentId ORDER BY a.Score DESC, a.TimeTakenSec ASC) AS LiveRank,
        COUNT(*) OVER (PARTITION BY a.AssessmentId) AS TotalParticipants
FROM    dbo.Attempts a
JOIN    dbo.Users u ON u.UserId = a.UserId
WHERE   a.Status IN (N'SUBMITTED', N'AUTO_SUBMITTED', N'FLAGGED');
GO

-- Detailed tabular reflection activity answers view (using OPENJSON)
CREATE OR ALTER VIEW dbo.vw_CourseReflections AS
SELECT  
    r.ReflectionId,
    r.UserId,
    u.Name AS StudentName,
    u.Email AS StudentEmail,
    r.CourseId,
    c.Title AS CourseTitle,
    c.Slug AS CourseSlug,
    q.question_number AS QuestionNumber,
    q.question_text AS QuestionText,
    q.selected_option AS SelectedOption,
    r.CreatedAt AS SubmittedAt,
    r.UpdatedAt
FROM dbo.CourseReflections r
JOIN dbo.Users u ON u.UserId = r.UserId
JOIN dbo.Courses c ON c.CourseId = r.CourseId
CROSS APPLY OPENJSON(r.AnswersJson)
WITH (
    question_number INT           '$.question_number',
    question_text   NVARCHAR(500) '$.question_text',
    selected_option NVARCHAR(500) '$.selected_option'
) q;
GO

PRINT 'ExamProLMS schema ready.';
