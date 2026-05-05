-- Create a dedicated database for your project
CREATE DATABASE IF NOT EXISTS anaphyl_pipeline;
USE anaphyl_pipeline;

-- Table 1: Master list of people (u)
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100),
    join_date DATE
);

-- Table 2: Every action they took (a)
CREATE TABLE activity (
    activity_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    task_name VARCHAR(100),
    start_time DATETIME,
    end_time DATETIME,
    status VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


INSERT INTO users (user_id, user_name, join_date) VALUES 
(101, 'Alice Smith', '2026-01-15'),
(102, 'Bob Jones', '2026-02-10'),
(103, 'Charlie Davis', '2026-03-05');

INSERT INTO activity (user_id, task_name, start_time, end_time, status) VALUES 
(101, 'Data Entry', '2026-05-01 09:00:00', '2026-05-01 09:45:00', 'completed'),
(102, 'SQL Cleanup', '2026-05-01 10:00:00', '2026-05-01 14:30:00', 'completed'), -- Takes a long time
(103, 'Pipeline Test', '2026-05-01 11:00:00', NULL, 'incomplete'); -- No end time

SELECT * FROM users;
SELECT * FROM activity;

USE anaphyl_pipeline;

SELECT 
    u.user_name AS Name, 
    a.task_name AS Task,
    a.status AS Status
FROM users u
JOIN activity a ON u.user_id = a.user_id
WHERE a.status = 'incomplete' OR TIMESTAMPDIFF(HOUR, a.start_time, a.end_time) > 2;

-- ****************************************************************************************************
USE mydb;

SELECT 
    u.user_name AS Name, 
    a.task_name AS Task,
    a.status AS Status
FROM users u
JOIN activity a ON u.user_id = a.user_id
WHERE a.status = 'incomplete' OR TIMESTAMPDIFF(HOUR, a.start_time, a.end_time) > 2;

-- ****************************************************************************************************
USE mydb;
SELECT 
    u.user_id, 
    u.user_name, 
    a.status
FROM users u
LEFT JOIN activity a ON u.user_id = a.user_id;

-- ****************************************************************************************************
# Using Group By:
/* 
   Advanced SQL Stage 2: Aggregations
   Objective: Count 'slow-completers' per course to reduce PANDAS overhead.
*/
USE mydb;
SELECT 
    a.task_name AS Course_Module, 
    COUNT(u.user_id) AS slow_completer_count
FROM users u
JOIN activity a ON u.user_id = a.user_id
-- Filter for those who are behind or incomplete
WHERE a.status = 'incomplete' 
   OR TIMESTAMPDIFF(HOUR, a.start_time, a.end_time) > 2
GROUP BY a.task_name
ORDER BY slow_completer_count DESC;


# ... using Group By without COUNT:
SELECT 
    task_name, 
    AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time)) AS avg_duration
FROM activity
WHERE status = 'completed'
GROUP BY task_name;
-- ****************************************************************************************************
# Course: 
# https://www.youtube.com/watch?v=7NBt0V8ebGk
-- ****************************************************************************************************
