import os
import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DATA_DIR = "data"
DEPT_FILE = os.path.join(DATA_DIR, "departments.csv")
RENAL_FILE = os.path.join(DATA_DIR, "renal_borne.csv")

df_dept = pd.read_csv(DEPT_FILE)
df_renal = pd.read_csv(RENAL_FILE)

conn = sqlite3.connect(":memory:")
df_dept.to_sql("departments_table", conn, if_exists="replace", index=False)
df_renal.to_sql("renal_table", conn, if_exists="replace", index=False)

# =====================================================================
# 🔮 ADVANCED WINDOW FUNCTION: Multi-Metric Partitioning
# =====================================================================
percentage_partition_query = """
SELECT 
    r.id_number,
    d.Department,
    r.Staff_Group,
    r.Completed,
    -- 1. Get the headcount baseline for this specific profession ON THIS SPECIFIC WARD
    COUNT(r.id_number) OVER(PARTITION BY d.Department, r.Staff_Group) as ward_stgroup_total,

    -- 2. Sum up completions for this specific profession ON THIS SPECIFIC WARD
    SUM(CASE WHEN r.Completed = 'Yes' THEN 1 ELSE 0 END) OVER(PARTITION BY d.Department, r.Staff_Group) as ward_stgroup_completions,

    -- 3. Calculate the percentage localized to this specific ward-level profession
    ROUND(
        (SUM(CASE WHEN r.Completed = 'Yes' THEN 1.0 ELSE 0.0 END) OVER(PARTITION BY d.Department, r.Staff_Group) / 
         COUNT(r.id_number) OVER(PARTITION BY d.Department, r.Staff_Group)) * 100, 1
    ) || '%' as ward_stgroup_completion_rate
FROM renal_table r
INNER JOIN departments_table d ON r.id_number = d.id_number
"""

df_percentage = pd.read_sql_query(percentage_partition_query, conn)

# =====================================================================
# PRINT THE LIVE TRIAGE REPORT
# =====================================================================
print("\n" + "🔮" * 45)
print("     MODE 2 UPGRADE: OPERATIONAL TRIAGE VIEW WITH LIVE DEPT PERCENTAGES")
print("🔮" * 45)
# Print a sample showing rows from different departments to see the rate change
print(df_percentage.iloc[[0, 1, 35, 36, 130, 131]])
print("🔮" * 45 + "\n")

conn.close()
