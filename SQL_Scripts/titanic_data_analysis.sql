SELECT * FROM anaphyl_pipeline.titanic_data;

SELECT 
    PassengerId,
    Gender, 
    Fare,
    -- This calculates the average completion time FOR THAT SPECIFIC TASK
    AVG(Fare) OVER(PARTITION BY Gender) AS average_fare
FROM anaphyl_pipeline.titanic_data;

#******************************************************************************
SELECT 
    PassengerId, 
    Gender, 
    Pclass,
    Fare,
    -- Your original finding
    AVG(Fare) OVER(PARTITION BY Gender) AS avg_fare_by_gender,
    -- The deeper insight: Avg fare for that Gender in that specific Class
    AVG(Fare) OVER(PARTITION BY Gender, Pclass) AS avg_fare_gender_class
FROM anaphyl_pipeline.titanic_data;

#******************************************************************************