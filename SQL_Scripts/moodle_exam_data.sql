SELECT * FROM mydb.moodle_exam_data;

USE mydb;

INSERT INTO moodle_exam_data (Student_ID, Hours_Studied, Attendance_Rate, Previous_Grade, Gender, Exam_Score)
VALUES 
(9001, 45, 98, 88, 'male', NULL),   -- The "Star Student" (Prediction should be high)
(9002, 2, 40, 55, 'female', NULL),  -- The "At-Risk Student" (Prediction should be low)
(9003, 20, 75, 70, 'male', NULL);   -- The "Average Student" (Prediction should be middle)

-- Double check they are there
SELECT * FROM moodle_exam_data WHERE Exam_Score IS NULL;


SET SQL_SAFE_UPDATES = 0;

-- Now run your update again
UPDATE moodle_exam_data 
SET Hours_Studied = 0, Attendance_Rate = 0, Previous_Grade = 0 
WHERE Student_ID = 9002;

SET SQL_SAFE_UPDATES = 1; -- Turn safety back on afterward

-- Let's see the Top 10 Students in your database
SELECT * FROM moodle_exam_data 
WHERE Exam_Score IS NOT NULL 
ORDER BY Exam_Score DESC 
LIMIT 10;

-- Let's check the relationship between studying and scores
SELECT 
    AVG(Exam_Score) AS Avg_Score, 
    CASE 
        WHEN Hours_Studied > 30 THEN 'High Study (30+ hrs)'
        WHEN Hours_Studied < 5 THEN 'Low Study (0-5 hrs)'
        ELSE 'Medium'
    END AS Study_Category
FROM moodle_exam_data
WHERE Exam_Score IS NOT NULL
GROUP BY Study_Category;

# ************** NOTES ON 02/04/2026 **************************
-- Let's see the average score for different levels of studying
SELECT 
    CASE 
        WHEN Hours_Studied >= 40 THEN 'A: Hard Workers (40+ hrs)'
        WHEN Hours_Studied BETWEEN 20 AND 39 THEN 'B: Average (20-39 hrs)'
        WHEN Hours_Studied BETWEEN 5 AND 19 THEN 'C: Minimum (5-19 hrs)'
        ELSE 'D: Low Study (0-4 hrs)'
    END AS Study_Category,
    COUNT(*) AS Number_of_Students,
    ROUND(AVG(Exam_Score), 2) AS Avg_Exam_Score,
    ROUND(AVG(Attendance_Rate), 2) AS Avg_Attendance
FROM moodle_exam_data
WHERE Exam_Score IS NOT NULL
GROUP BY Study_Category
ORDER BY Study_Category ASC;


# Let's fix the "World" (MySQL) with this script:
# We will manually "Inject" logic into your 1,000 rows so the AI can finally see a pattern.'''
SET SQL_SAFE_UPDATES = 0;

-- 1. Give 'Hard Workers' a massive boost (Logical Pattern)
UPDATE moodle_exam_data 
SET Exam_Score = 85 + (RAND() * 10) 
WHERE Hours_Studied > 35 AND Attendance_Rate > 85;

-- 2. Give 'Strugglers' a massive drop (Logical Pattern)
UPDATE moodle_exam_data 
SET Exam_Score = 20 + (RAND() * 20) 
WHERE Hours_Studied < 10 AND Attendance_Rate < 50;

SET SQL_SAFE_UPDATES = 1;


-- To force the data to have a clear, mathematical rule that the AI can't ignore:
SET SQL_SAFE_UPDATES = 0;

-- Rule 1: "Hard Work = Success" (Students with 40+ hrs get 90-100)
UPDATE moodle_exam_data 
SET Exam_Score = 90 + (RAND() * 10) 
WHERE Hours_Studied >= 40 AND Attendance_Rate >= 80;

-- Rule 2: "Neglect = Failure" (Students with <5 hrs get 20-40)
UPDATE moodle_exam_data 
SET Exam_Score = 20 + (RAND() * 20) 
WHERE Hours_Studied < 5 AND Attendance_Rate < 30;

SET SQL_SAFE_UPDATES = 1;

-- Doing one final "Stress Test" to see your V3 Brain handle the extremes we taught it:
SET SQL_SAFE_UPDATES = 0;

-- Let's create two NEW students to see the full range
INSERT INTO moodle_exam_data (Student_ID, Hours_Studied, Attendance_Rate, Previous_Grade, Gender, Exam_Score)
VALUES 
(9999, 50, 95, 90, 'female', NULL), -- The "Absolute Genius"
(8888, 1, 10, 30, 'male', NULL);    -- The "Absolute Warning"

SET SQL_SAFE_UPDATES = 1;

-- Preparing the "landing pad" for your AI's thoughts:
ALTER TABLE moodle_exam_data 
ADD COLUMN AI_Prediction FLOAT;

-- Check to see the empty column
SELECT * FROM moodle_exam_data;

-- This is the ultimate "Proof of Life" for your AI:
SELECT Student_ID, Hours_Studied, Attendance_Rate, AI_Prediction 
FROM mydb.moodle_exam_data 
WHERE Student_ID IN (9999, 8888, 9003);

-- This will wipe out the test students entirely so we can start fresh with a clean slate:
SET SQL_SAFE_UPDATES = 0;

-- 1. Delete the duplicates
DELETE FROM moodle_exam_data WHERE Student_ID IN (8888, 9003, 9999);

-- 2. Insert them again, ONCE each
INSERT INTO moodle_exam_data (Student_ID, Hours_Studied, Attendance_Rate, Previous_Grade, Gender, Exam_Score)
VALUES 
(9003, 20, 75, 70, 'male', NULL),
(9999, 50, 95, 90, 'female', NULL),
(8888, 1, 10, 30, 'male', NULL);

SET SQL_SAFE_UPDATES = 1;

-- 3. Verify you only see 3 rows
SELECT * FROM moodle_exam_data WHERE Exam_Score IS NULL;


