/* ============================================================================
   ExamPro LMS - demo content (1 course, 4 graded assessments, 1 practice set)
   Users are NOT seeded here because passwords must be bcrypt-hashed by the app.
   Create users with:  python -m scripts.create_admin   (see backend/README.md)
   Safe to re-run: skips when the demo course already exists.
   ============================================================================ */
USE ExamProLMS;
GO
SET QUOTED_IDENTIFIER ON;
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Courses WHERE Slug = N'quantitative-aptitude')
BEGIN
    BEGIN TRAN;

    INSERT INTO dbo.Courses (Title, Slug, Description, OrderIndex)
    VALUES (N'Quantitative Aptitude',
            N'quantitative-aptitude',
            N'Arithmetic foundations for TNPSC, SSC, Banking and RRB exams. Complete the graded tests in order; use the practice set for unlimited revision.',
            1);
    DECLARE @course INT = SCOPE_IDENTITY();

    /* ---- Assessments ------------------------------------------------------ */
    INSERT INTO dbo.Assessments
        (CourseId, Title, Slug, Description, Topic, Difficulty, DefaultDurationMinutes, MinDurationMinutes,
         TotalQuestions, PassPercentage, AttemptType, SequentialUnlock, LockdownEnabled, ProctoringEnabled, OrderIndex)
    VALUES
        (@course, N'Percentage',    N'percentage',    N'Percentage basics: increase, decrease and successive change.', N'Percentage',      N'EASY',   30, 15, 5, 60, N'GRADED',   1, 1, 1, 1),
        (@course, N'Time & Work',   N'time-and-work', N'Work, wages, pipes and cisterns.',                              N'Time & Work',     N'MEDIUM', 30, 15, 4, 60, N'GRADED',   1, 1, 1, 2),
        (@course, N'Profit & Loss', N'profit-and-loss', N'Cost price, selling price, discount and markup.',             N'Profit & Loss',   N'MEDIUM', 30, 15, 4, 60, N'GRADED',   1, 1, 1, 3),
        (@course, N'Mixtures',      N'mixtures',      N'Ratios, alligation and replacement problems.',                  N'Mixtures',        N'HARD',   30, 15, 4, 60, N'GRADED',   1, 1, 1, 4),
        (@course, N'Percentage - Practice Set', N'percentage-practice', N'Unlimited practice with instant feedback. Nothing is recorded.', N'Percentage', N'EASY', 30, 15, 5, 0, N'PRACTICE', 0, 0, 0, 5);

    DECLARE @pct  INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage');
    DECLARE @tw   INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'time-and-work');
    DECLARE @pl   INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'profit-and-loss');
    DECLARE @mix  INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'mixtures');
    DECLARE @prac INT = (SELECT AssessmentId FROM dbo.Assessments WHERE Slug = N'percentage-practice');

    /* ---- Questions -------------------------------------------------------- */
    INSERT INTO dbo.Questions (AssessmentId, QuestionText, OptionsJson, CorrectIndex, Explanation, Topic, Difficulty, OrderIndex)
    VALUES
    -- Percentage (graded)
    (@pct, N'What is 25% of 240?', N'["40","50","60","80"]', 2,
        N'25% = 1/4, and 240 / 4 = 60.', N'Percentage', N'EASY', 1),
    (@pct, N'A number increases from 80 to 100. What is the percentage increase?', N'["20%","30%","25%","15%"]', 2,
        N'Increase = 20. Percentage increase = 20 / 80 x 100 = 25%.', N'Percentage', N'EASY', 2),
    (@pct, N'The price of a book falls from Rs. 250 to Rs. 200. What is the percentage decrease?', N'["15%","25%","10%","20%"]', 3,
        N'Decrease = 50. Percentage decrease = 50 / 250 x 100 = 20%.', N'Percentage', N'EASY', 3),
    (@pct, N'A student needs 40% to pass. He scores 120 marks and fails by 30 marks. What are the maximum marks?', N'["350","400","375","450"]', 2,
        N'Pass mark = 120 + 30 = 150. 40% of M = 150, so M = 150 / 0.4 = 375.', N'Percentage', N'MEDIUM', 4),
    (@pct, N'20% of a number is 45. What is the number?', N'["180","225","250","200"]', 1,
        N'Number = 45 x 100 / 20 = 225.', N'Percentage', N'EASY', 5),

    -- Time & Work (graded)
    (@tw, N'A can finish a job in 10 days and B in 15 days. Working together, how many days will they take?', N'["5","6","7.5","8"]', 1,
        N'Combined rate = 1/10 + 1/15 = 1/6 per day, so 6 days.', N'Time & Work', N'EASY', 1),
    (@tw, N'A can finish a job in 12 days. He works for 4 days and then leaves. What fraction of the job remains?', N'["1/3","1/2","2/3","3/4"]', 2,
        N'Work done = 4/12 = 1/3, so remaining = 2/3.', N'Time & Work', N'EASY', 2),
    (@tw, N'8 men can complete a job in 12 days. How many days will 6 men take?', N'["14","15","16","18"]', 2,
        N'Man-days = 8 x 12 = 96. 96 / 6 = 16 days.', N'Time & Work', N'MEDIUM', 3),
    (@tw, N'Pipe A fills a tank in 20 minutes and pipe B empties it in 30 minutes. With both open, how long to fill the tank?', N'["50","60","40","45"]', 1,
        N'Net rate = 1/20 - 1/30 = 1/60 per minute, so 60 minutes.', N'Time & Work', N'MEDIUM', 4),

    -- Profit & Loss (graded)
    (@pl, N'An article bought for Rs. 800 is sold for Rs. 920. What is the profit percentage?', N'["12%","15%","18%","20%"]', 1,
        N'Profit = 120. 120 / 800 x 100 = 15%.', N'Profit & Loss', N'EASY', 1),
    (@pl, N'An article is sold at a 10% loss for Rs. 720. What was the cost price?', N'["780","750","800","820"]', 2,
        N'SP = 0.9 x CP, so CP = 720 / 0.9 = 800.', N'Profit & Loss', N'MEDIUM', 2),
    (@pl, N'The cost price of 12 articles equals the selling price of 10 articles. What is the profit percentage?', N'["10%","15%","20%","25%"]', 2,
        N'Let CP of one article = 1. SP of one = 12/10 = 1.2, so profit = 20%.', N'Profit & Loss', N'MEDIUM', 3),
    (@pl, N'The marked price is Rs. 500 and a discount of 20% is given. What is the selling price?', N'["380","420","400","450"]', 2,
        N'SP = 500 x 0.8 = 400.', N'Profit & Loss', N'EASY', 4),

    -- Mixtures (graded)
    (@mix, N'A 20 L mixture has milk and water in the ratio 3:1. How much water is in it?', N'["4 L","5 L","6 L","8 L"]', 1,
        N'Water = 1/4 of 20 L = 5 L.', N'Mixtures', N'EASY', 1),
    (@mix, N'2 kg of sugar at Rs. 40/kg is mixed with 3 kg at Rs. 50/kg. What is the price per kg of the mixture?', N'["44","45","46","48"]', 2,
        N'Total cost = 80 + 150 = 230. 230 / 5 = 46.', N'Mixtures', N'MEDIUM', 2),
    (@mix, N'A 40 L mixture has milk and water in the ratio 3:2. How much water must be added to make the ratio 1:1?', N'["6 L","8 L","10 L","12 L"]', 1,
        N'Milk = 24 L, water = 16 L. To match milk, add 24 - 16 = 8 L.', N'Mixtures', N'MEDIUM', 3),
    (@mix, N'In what ratio should rice at Rs. 30/kg be mixed with rice at Rs. 40/kg to get a mixture worth Rs. 36/kg?', N'["3:2","1:1","1:2","2:3"]', 3,
        N'By alligation: (40 - 36) : (36 - 30) = 4 : 6 = 2 : 3.', N'Mixtures', N'HARD', 4),

    -- Practice set
    (@prac, N'What is 10% of 500?', N'["5","25","50","100"]', 2,
        N'10% = 1/10, and 500 / 10 = 50.', N'Percentage', N'EASY', 1),
    (@prac, N'What is 50% of 50% of 200?', N'["75","25","100","50"]', 3,
        N'50% of 200 = 100; 50% of 100 = 50.', N'Percentage', N'EASY', 2),
    (@prac, N'Express 0.5 as a percentage.', N'["5%","0.5%","50%","500%"]', 2,
        N'Multiply by 100: 0.5 x 100 = 50%.', N'Percentage', N'EASY', 3),
    (@prac, N'A population of 20,000 grows 10% each year for two years. What is it after two years?', N'["24000","24200","22000","24400"]', 1,
        N'20,000 x 1.1 x 1.1 = 24,200.', N'Percentage', N'MEDIUM', 4),
    (@prac, N'A salary of Rs. 30,000 has 40% spent on rent. How much is left?', N'["12000","18000","20000","16000"]', 1,
        N'Rent = 12,000, so remaining = 30,000 - 12,000 = 18,000.', N'Percentage', N'EASY', 5);

    COMMIT;
    PRINT 'Demo content inserted.';
END
ELSE
    PRINT 'Demo content already present - skipped.';
GO
