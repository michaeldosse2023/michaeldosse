# *****************************************************************************
# BSOT_DATA
SELECT * FROM mydb.bsot_data;
# *****************************************************************************

# (A) CONVERTING Date format:
-- 1. Unlock the safety gate
SET SQL_SAFE_UPDATES = 0;

-- 2. Update all three columns at once
UPDATE mydb.bsot_data 
SET 
    Enrolment_Date = STR_TO_DATE(NULLIF(Enrolment_Date, ''), '%d/%m/%Y'),
    Last_access = STR_TO_DATE(NULLIF(Last_access, ''), '%d/%m/%Y'),
    Completion_Date = STR_TO_DATE(NULLIF(Completion_Date, ''), '%d/%m/%Y')
WHERE 1=1; -- This '1=1' is a little trick to tell MySQL "Yes, update everything."

-- 3. Lock the gate back up
SET SQL_SAFE_UPDATES = 1;

# ****************************************************************************
# (B) bsot_data "Audit" query: 
SELECT 
    Staff_Group, 
    Role, 
    COUNT(*) as Total_Enrolled,
    COUNT(Completion_Date) as Total_Completed,
    ROUND(AVG(DATEDIFF(Completion_Date, Enrolment_Date)), 1) as Avg_Days_to_Finish
FROM mydb.bsot_data
GROUP BY Staff_Group, Role
ORDER BY Avg_Days_to_Finish DESC;

# *****************************************************************************
# OPTIONAL
# Checking who is currently a "Risk" directly in SQL to compare against the AI list later:
SELECT 
    ID_Number, 
    Staff_Group, 
    DATEDIFF(CURDATE(), Last_access) as Days_Since_Last_Login
FROM mydb.bsot_data
WHERE Completion_Date IS NULL
ORDER BY Days_Since_Last_Login DESC;

# *****************************************************************************
# (C) The "ML-Ready" Export: Creating a format matching your original model.
SELECT 
    Staff_Group, 
    Role, 
    -- Calculate Days Since Enrolled (using today's date)
    DATEDIFF(CURDATE(), Enrolment_Date) AS Days_Since_Enrolled,
    -- Calculate Days Inactive (difference between today and last access)
    DATEDIFF(CURDATE(), Last_access) AS Days_Inactive,
    -- Create the Status (1 if they finished, 0 if they haven't)
    CASE WHEN Completion_Date IS NOT NULL THEN 1 ELSE 0 END AS Status
FROM mydb.bsot_data;

# *****************************************************************************
# BADGERNET
SELECT * FROM mydb.badgernet;
# ****************************************************************************
# (A) CONVERTING Date format:
-- 1. Unlock the safety gate
SET SQL_SAFE_UPDATES = 0;

-- 2. Update all three columns at once
UPDATE mydb.badgernet 
SET 
    Enrolment_Date = STR_TO_DATE(NULLIF(Enrolment_Date, ''), '%d/%m/%Y'),
    Last_access = STR_TO_DATE(NULLIF(Last_access, ''), '%d/%m/%Y'),
    Completion_Date = STR_TO_DATE(NULLIF(Completion_Date, ''), '%d/%m/%Y')
WHERE 1=1; -- This '1=1' is a little trick to tell MySQL "Yes, update everything."

-- 3. Lock the gate back up
SET SQL_SAFE_UPDATES = 1;

# ****************************************************************************
# (B) BadgerNet "Audit" query: 
SELECT 
    Staff_Group, 
    Role, 
    COUNT(*) as Total_Enrolled,
    COUNT(Completion_Date) as Total_Completed,
    ROUND(AVG(DATEDIFF(Completion_Date, Enrolment_Date)), 1) as Avg_Days_to_Finish
FROM mydb.badgernet
GROUP BY Staff_Group, Role
ORDER BY Avg_Days_to_Finish DESC;

# *****************************************************************************
# (C) The "ML-Ready" Export: Creating a format matching your original model.
SELECT 
    Staff_Group, 
    Role, 
    DATEDIFF(CURDATE(), Enrolment_Date) as Days_Since_Enrolled,
    DATEDIFF(CURDATE(), Last_access) as Days_Inactive,
    CASE WHEN Completion_Date IS NOT NULL THEN 1 ELSE 0 END as Status
FROM mydb.badgernet;

# *****************************************************************************
# DEMENTIA
SELECT * FROM mydb.dementia;
# ****************************************************************************
# (A) CONVERTING Date format:
-- 1. Unlock the safety gate
SET SQL_SAFE_UPDATES = 0;

-- 2. Update all three columns at once
UPDATE mydb.dementia 
SET 
    Enrolment_Date = STR_TO_DATE(NULLIF(Enrolment_Date, ''), '%d/%m/%Y'),
    Last_access = STR_TO_DATE(NULLIF(Last_access, ''), '%d/%m/%Y'),
    Completion_Date = STR_TO_DATE(NULLIF(Completion_Date, ''), '%d/%m/%Y')
WHERE 1=1; -- This '1=1' is a little trick to tell MySQL "Yes, update everything."

-- 3. Lock the gate back up
SET SQL_SAFE_UPDATES = 1;

# ****************************************************************************
# (B) Dementia "Audit" query: 
SELECT 
    Staff_Group, 
    Role, 
    COUNT(*) as Total_Enrolled,
    COUNT(Completion_Date) as Total_Completed,
    ROUND(AVG(DATEDIFF(Completion_Date, Enrolment_Date)), 1) as Avg_Days_to_Finish
FROM mydb.dementia
GROUP BY Staff_Group, Role
ORDER BY Avg_Days_to_Finish DESC;

# *****************************************************************************
# (C) The "ML-Ready" Export: Creating a format matching your original model.
SELECT 
    Staff_Group, 
    Role, 
    DATEDIFF(CURDATE(), Enrolment_Date) as Days_Since_Enrolled,
    DATEDIFF(CURDATE(), Last_access) as Days_Inactive,
    CASE WHEN Completion_Date IS NOT NULL THEN 1 ELSE 0 END as Status
FROM mydb.dementia;

# *****************************************************************************
# ANAPHYLAXIS
SELECT * FROM mydb.anaphylaxis;
# ****************************************************************************
# (A) CONVERTING Date format:
-- 1. Unlock the safety gate
SET SQL_SAFE_UPDATES = 0;

-- 2. Update all three columns at once
UPDATE mydb.anaphylaxis
SET 
    Enrolment_Date = STR_TO_DATE(NULLIF(Enrolment_Date, ''), '%d/%m/%Y'),
    Last_access = STR_TO_DATE(NULLIF(Last_access, ''), '%d/%m/%Y'),
    Completion_Date = STR_TO_DATE(NULLIF(Completion_Date, ''), '%d/%m/%Y')
WHERE 1=1; -- This '1=1' is a little trick to tell MySQL "Yes, update everything."

-- 3. Lock the gate back up
SET SQL_SAFE_UPDATES = 1;

# ****************************************************************************
# (B) anaphylaxis "Audit" query: 
SELECT 
    Staff_Group, 
    Role, 
    COUNT(*) as Total_Enrolled,
    COUNT(Completion_Date) as Total_Completed,
    ROUND(AVG(DATEDIFF(Completion_Date, Enrolment_Date)), 1) as Avg_Days_to_Finish
FROM mydb.anaphylaxis
GROUP BY Staff_Group, Role
ORDER BY Avg_Days_to_Finish DESC;

# *****************************************************************************
# (C) The "ML-Ready" Export: Creating a format matching your original model.
SELECT 
    Staff_Group, 
    Role, 
    DATEDIFF(CURDATE(), Enrolment_Date) as Days_Since_Enrolled,
    DATEDIFF(CURDATE(), Last_access) as Days_Inactive,
    CASE WHEN Completion_Date IS NOT NULL THEN 1 ELSE 0 END as Status
FROM mydb.anaphylaxis;

# *****************************************************************************
# DIABETES
SELECT * FROM mydb.diabetes;
# ****************************************************************************
# (A) CONVERTING Date format:
-- 1. Unlock the safety gate
SET SQL_SAFE_UPDATES = 0;

-- 2. Update all three columns at once
UPDATE mydb.diabetes 
SET 
    Enrolment_Date = STR_TO_DATE(NULLIF(Enrolment_Date, ''), '%d/%m/%Y'),
    Last_access = STR_TO_DATE(NULLIF(Last_access, ''), '%d/%m/%Y'),
    Completion_Date = STR_TO_DATE(NULLIF(Completion_Date, ''), '%d/%m/%Y')
WHERE 1=1; -- This '1=1' is a little trick to tell MySQL "Yes, update everything."

-- 3. Lock the gate back up
SET SQL_SAFE_UPDATES = 1;

# ****************************************************************************
# (B) Diabetes "Audit" query: 
SELECT 
    Staff_Group, 
    Role, 
    COUNT(*) as Total_Enrolled,
    COUNT(Completion_Date) as Total_Completed,
    ROUND(AVG(DATEDIFF(Completion_Date, Enrolment_Date)), 1) as Avg_Days_to_Finish
FROM mydb.diabetes
GROUP BY Staff_Group, Role
ORDER BY Avg_Days_to_Finish DESC;

# *****************************************************************************
# (C) The "ML-Ready" Export: Creating a format matching your original model.
SELECT 
    Staff_Group, 
    Role, 
    DATEDIFF(CURDATE(), Enrolment_Date) as Days_Since_Enrolled,
    DATEDIFF(CURDATE(), Last_access) as Days_Inactive,
    CASE WHEN Completion_Date IS NOT NULL THEN 1 ELSE 0 END as Status
FROM mydb.diabetes;

# *****************************************************************************
# RENAL
SELECT * FROM mydb.renal;
# ****************************************************************************
# (A) CONVERTING Date format:
-- 1. Unlock the safety gate
SET SQL_SAFE_UPDATES = 0;

-- 2. Update all three columns at once
UPDATE mydb.renal 
SET 
    Enrolment_Date = STR_TO_DATE(NULLIF(Enrolment_Date, ''), '%d/%m/%Y'),moodle_exam_data
    Last_access = STR_TO_DATE(NULLIF(Last_access, ''), '%d/%m/%Y'),
    Completion_Date = STR_TO_DATE(NULLIF(Completion_Date, ''), '%d/%m/%Y')
WHERE 1=1; -- This '1=1' is a little trick to tell MySQL "Yes, update everything."

-- 3. Lock the gate back up
SET SQL_SAFE_UPDATES = 1;

# ****************************************************************************
# (B) Renal "Audit" query: 
SELECT 
    Staff_Group, 
    Role, 
    COUNT(*) as Total_Enrolled,
    COUNT(Completion_Date) as Total_Completed,
    ROUND(AVG(DATEDIFF(Completion_Date, Enrolment_Date)), 1) as Avg_Days_to_Finish
FROM mydb.renal
GROUP BY Staff_Group, Role
ORDER BY Avg_Days_to_Finish DESC;

# *****************************************************************************
# (C) Turning Yes & No into the 1 and 0 "language" the AI understands:
# Added on 21/04/2026
SELECT 
    Staff_Group, 
    Role, 
    DATEDIFF(CURDATE(), Enrolment_Date) as Days_Since_Enrolled, 
    DATEDIFF(CURDATE(), Last_access) as Days_Inactive,
    -- This part turns words into the 1s and 0s the model needs
    CASE 
        WHEN Completed = 'Yes' THEN 1 
        ELSE 0 
    END AS Status
FROM mydb.renal;

# *****************************************************************************