-- Create a dedicated database for your project
# CREATE DATABASE IF NOT EXISTS analytics;
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
# *******************************************************************************************************
SELECT * FROM anaphyl_pipeline.titanic_data;

SELECT 
    PassengerId,
    Gender, 
    Fare,
    -- This calculates the average completion time FOR THAT SPECIFIC TASK
    AVG(Fare) OVER(PARTITION BY Gender) AS average_fare
FROM anaphyl_pipeline.titanic_data;

#******************************************************************************************************
# The use of OVER(PARTITION BY) with Titanic Data:

SELECT 
    PassengerId, 
    Gender, 
    Pclass,
    Fare,
    -- Your original finding
    AVG(Fare)  AS avg_fare_by_gender,
    -- The deeper insight: Avg fare for that Gender in that specific Class
    AVG(Fare) OVER(PARTITION BY Gender, Pclass) AS avg_fare_gender_class
FROM anaphyl_pipeline.titanic_data;

#********************************************************************************************************
# The Use of Subqueries (mydb.film):

USE sakila;

# 1. Find the name of a movie with longest run time:
SELECT title, rating, length
FROM film
WHERE length IN (SELECT MAX(length) FROM film);

# 2. Find the proportion of movies with a specific rating:
SELECT (SELECT COUNT(*) FROM film WHERE rating = 'NC-17') / COUNT(*) as proportion
FROM film;


# 3. Find custmers who have rented a specific movie rating:
SELECT CONCAT(first_name, " ", last_name) as full_name, email
FROM customer
WHERE customer_id IN
	(SELECT customer_id FROM rental WHERE inventory_id IN
		(SELECT inventory_id FROM inventory WHERE film_id IN 
			(SELECT film_id FROM film WHERE rating = 'NC-17')));
            
# From Gemini AI (same as at # 3.):
SELECT CONCAT(first_name, ' ', last_name) AS full_name, email
FROM customer
WHERE customer_id IN (
    SELECT customer_id 
    FROM rental 
    WHERE inventory_id IN (
        SELECT inventory_id 
        FROM inventory 
        WHERE film_id IN (
            SELECT film_id 
            FROM film 
            WHERE rating = 'NC-17'
        )
    )
);

# As CTE/Common Table Expression, the logic becomes:
USE sakila;

WITH target_films AS (
    SELECT film_id 
    FROM film 
    WHERE rating = 'NC-17'
),
rented_inventory AS (
    SELECT inventory_id, film_id 
    FROM inventory 
    WHERE film_id IN (SELECT film_id FROM target_films)
),
customer_matches AS (
    SELECT DISTINCT customer_id 
    FROM rental 
    WHERE inventory_id IN (SELECT inventory_id FROM rented_inventory)
)
-- Final clean output for Python
SELECT 
    CONCAT(first_name, ' ', last_name) AS full_name, 
    email
FROM customer
WHERE customer_id IN (SELECT customer_id FROM customer_matches);

#********************************************************************************************************

# ... using Group By without COUNT:
SELECT 
    task_name, 
    AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time)) AS avg_duration
FROM activity
WHERE status = 'completed'
GROUP BY task_name;
-- ****************************************************************************************************
# Recomended MySQL Course: 
# https://www.youtube.com/watch?v=7NBt0V8ebGk

# To also cover:
# https://www.youtube.com/watch?v=3Pv2tCkSY4Q

# To also cover:
# https://www.youtube.com/watch?v=-u-kCJmJHCk
# https://www.youtube.com/watch?v=-u-kCJmJHCk
# https://www.youtube.com/watch?v=LJC8277LONg

# To also cover:
# https://www.youtube.com/watch?v=GHPHZ8XJxeg
-- ****************************************************************************************************
# Exploring MySQL Databases:
USE mydb;
USE anaphyl_pipeline;
SHOW TABLES;
DESCRIBE activity;

-- ****************************************************************************************************
USE analytics;

SELECT  product_category, payment_method, COUNT(*) AS sub_total
FROM ecommerce_sales
#WHERE COUNT(*) > 130
GROUP BY product_category, payment_method
HAVING COUNT(*) > 130
ORDER BY COUNT(*) ASC;
-- ****************************************************************************************************
# Window Functions:
USE analytics;

SELECT Category, Sales, Quantity, Profit, Region,
	ROW_NUMBER() OVER(ORDER BY Profit DESC) AS Popularity,
    RANK() OVER(ORDER BY Profit DESC) AS Profit_Rank 
FROM retail_sales
WHERE Sales > 0;

-- ****************************************************************************************************
# Window Functions with PARTITION BY:
USE analytics;

SELECT Category, Sales, Quantity, Profit,
	ROW_NUMBER() OVER(PARTITION BY Category ORDER BY Profit DESC) AS Popularity
FROM retail_sales
WHERE Sales > 0;

-- ****************************************************************************************************
# Window Functions Using Subquesries:
USE analytics;
SELECT * FROM 
(SELECT Category, Sales, Quantity, Profit,
	ROW_NUMBER() OVER(PARTITION BY Category ORDER BY Profit DESC) AS Popularity
FROM retail_sales
WHERE Sales > 0) AS Pop
WHERE Popularity <= 100;

-- ****************************************************************************************************
# CTE/Common Table Expression vs Subqueries (aslo see "# As CTE, the logic becomes" section above):
USE analytics;

SELECT *
FROM 
(SELECT Category, MAX(Sales) AS Max_Sales
FROM retail_sales
GROUP BY Category) AS mp
WHERE Max_Sales >= 1763; 


# CTE/Common Table Expression Demo (to run the next two blocks together):
WITH mp AS (SELECT Category, MAX(Sales) AS Max_Sales
FROM retail_sales
GROUP BY Category) 

SELECT * FROM mp
WHERE Max_Sales >= 1763; 

# CTE: Multiple References
USE analytics;
WITH mp AS (SELECT Category, MAX(Sales) AS Max_Sales
FROM retail_sales
GROUP BY Category)

SELECT COUNT(*)
FROM mp
WHERE Max_Sales < (SELECT AVG(Max_Sales) FROM mp);


-- ****************************************************************************************************
# Recursive CTE Structure (NOT EXECUTABLE HERE):
WITH RECURSIVE my_dates(dt) AS (SELECT '2014-12-25'
								UNION ALL
                                SELECT dt + INTERVAL 1 day
                                FROM my_dates 
                                WHERE dt < '2014-12-31')
SELECT * FROM my_dates;

-- ****************************************************************************************************
# The Moodle "Categorization" Query with CASE WHEN:

# CASE WHEN Example ONE:
USE mydb;
SELECT 
    u.user_name,
    a.task_name,
    TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time) AS duration,
    -- Creating a custom 'Status' flag in SQL
    CASE 
        WHEN a.status = 'incomplete' THEN 'Priority: Slow-Completer'
        WHEN TIMESTAMPDIFF(MINUTE, a.start_time, a.end_time) > 120 THEN 'Warning: High Duration'
        ELSE 'On-Track'
    END AS performance_category
FROM users u
JOIN activity a ON u.user_id = a.user_id;


# CASE WHEN Example TWO:
SELECT  product_category, quantity,
	CASE 
		WHEN quantity > 5 THEN 'high_stock'
        WHEN quantity > 3 THEN 'medium_stock'
        ELSE 'low'
	END Stock_Category
FROM analytics.ecommerce_sales;

-- ****************************************************************************************************
# ******************************************************************************************************
# How to use OVER (PARTITION BY):

USE mydb;

SELECT 
    user_id, 
    task_name, 
    TIMESTAMPDIFF(MINUTE, start_time, end_time) AS duration_minutes,
    -- This looks at the average for JUST that specific task
    AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time)) OVER(PARTITION BY task_name) AS task_avg_duration,
    status
FROM activity
WHERE status = 'completed';

# ******************************************************************************************************
# Subqueries FINAL Practice:

# Example ONE:
USE analytics;
SELECT Category,	Sales,	QuantitY,	Region
FROM retail_sales
WHERE Region IN
		(SELECT Category
		FROM retail_sales
		WHERE Quantity > 2 AND Region = 'South');

# Example TWO:
SELECT * FROM Products
WHERE price > (SELECT AVG(price) FROM Products);

# ******************************************************************************************************
# The most commonly used SQL AGGREGATE FUNCTIONS are:

MIN() # returns the smallest value of a column
MAX() # returns the largest value of a column
COUNT() # returns the number of rows in a set
SUM() # returns the sum of a numerical column
AVG() # returns the average value of a numerical column
# Aggregate functions ignore null values (except for COUNT(*))

# ******************************************************************************************************
SELECT 
FROM 
	JOIN # Optional
WHERE
GROUP BY 
ORDER BY
HAVING # if WHERE clause is not suitable

# ******************************************************************************************************

SELECT date, 
	payment_method, 
    SUM(paymewnts) AS total_payments
FROM invoices
GROUP BY date, payment_method
ORDER BY total_payments;
# ******************************************************************************************************

# ******************************************************************************************************

# ******************************************************************************************************

# ******************************************************************************************************

# ******************************************************************************************************

# ******************************************************************************************************

# ******************************************************************************************************

# ******************************************************************************************************

# ******************************************************************************************************