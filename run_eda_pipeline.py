import sqlite3
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# 1. Spin up our relational repository
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE users (user_id INT, user_name TEXT, course_group TEXT)")
cursor.execute("CREATE TABLE user_activity (user_id INT, days_inactive INT, completed_modules INT)")

# Expanded dataset to build proper statistical variance distributions
users_data = [
    (101, 'Alice Smith', 'Clinical Tech'), (102, 'Bob Jones', 'Obstetrics'),
    (103, 'Charlie Green', 'Clinical Tech'), (104, 'Diana Prince', 'Obstetrics'),
    (105, 'Evan Wright', 'Clinical Tech'), (106, 'Fiona Gallagher', 'Obstetrics'),
    (107, 'George Brooks', 'Clinical Tech'), (108, 'Hannah Abbott', 'Obstetrics'),
    (109, 'Ian Malcolm', 'Clinical Tech'), (110, 'Julia Roberts', 'Obstetrics')
]

activity_data = [
    (101, 2, 12), (102, 14, 4), (103, 4, 15), (104, 25, 1), (105, 1, 14),
    (106, 11, 6), (107, 2, 13), (108, 29, 0), (109, 5, 16), (110, 12, 5)
]

cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", users_data)
cursor.executemany("INSERT INTO user_activity VALUES (?, ?, ?)", activity_data)
conn.commit()

# 2. Pull data using our Window Function partition foundation
query = """
SELECT 
    u.user_id,
    u.user_name,
    u.course_group,
    a.days_inactive,
    a.completed_modules,
    ROUND(AVG(a.days_inactive) OVER(PARTITION BY u.course_group), 1) as group_mean_inactivity
FROM users u
INNER JOIN user_activity a ON u.user_id = a.user_id
"""
df = pd.read_sql_query(query, conn)

# 3. STATISTICAL EDA LAYER: Calculate Team Standard Deviation & Z-Score
# Standard deviation measures the spread of the data.
# Z-Score tells us exactly how many standard deviations a user is from their team's average.
df['group_std_dev'] = df.groupby('course_group')['days_inactive'].transform('std').round(1)
df['z_score'] = ((df['days_inactive'] - df['group_mean_inactivity']) / df['group_std_dev']).round(2)

# Architect Rule: Mathematically classify performance risks
def statistical_triage(z):
    if z > 1.0:
        return 'slow-completers (Critical Divergence)'
    elif z > 0.0:
        return 'active (Monitor Trend)'
    return 'active (Optimal Efficiency)'

df['performance_status'] = df['z_score'].apply(statistical_triage)

# 4. PRINT ADVANCED STATISTICAL INSIGHT REPORT
print("\n" + "📊" * 40)
print("       INSIGHT SPECIALIST: ADVANCED DEVIATION REPORT")
print("📊" * 40)
print(df[['user_name', 'course_group', 'days_inactive', 'group_mean_inactivity', 'group_std_dev', 'z_score', 'performance_status']])
print("📊" * 40 + "\n")

conn.close()
