import os
import sqlite3
import pandas as pd

# 1. Expand Pandas display constraints for your monitor
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("🚀 Starting Moodle Clinical Analytics Engine...")

# 2. Define data folder directory paths
DATA_DIR = "data"
DEPT_FILE = os.path.join(DATA_DIR, "departments.csv")
RENAL_FILE = os.path.join(DATA_DIR, "renal_borne.csv")

# 3. Stream live data from disk files into Pandas
try:
    df_dept = pd.read_csv(DEPT_FILE)
    df_renal = pd.read_csv(RENAL_FILE)
    print("✅ Live CSV files loaded successfully from disk.")
except Exception as e:
    print(f"❌ Error loading files. Details: {e}")
    exit()

# 4. Spin up high-speed in-memory SQLite sandbox
conn = sqlite3.connect(":memory:")

# 5. Mirror DataFrames directly into relational database tables
df_dept.to_sql("departments_table", conn, if_exists="replace", index=False)
df_renal.to_sql("renal_table", conn, if_exists="replace", index=False)

# =====================================================================
# 🔮 THE MASTERWORK: TWO-COLUMN NESTED WINDOW PARTITION
# =====================================================================
nested_partition_query = """
SELECT 
    r.id_number,
    d.Department,
    r.Staff_Group,
    r.Completed,
    -- Get headcount baseline for this specific profession ON THIS SPECIFIC WARD
    COUNT(r.id_number) OVER(PARTITION BY d.Department, r.Staff_Group) as ward_stgroup_total,

    -- Sum up completions for this specific profession ON THIS SPECIFIC WARD
    SUM(CASE WHEN r.Completed = 'Yes' THEN 1 ELSE 0 END) OVER(PARTITION BY d.Department, r.Staff_Group) as ward_stgroup_completions,

    -- Calculate compliance rate localized to this specific ward-level profession
    ROUND(
        (SUM(CASE WHEN r.Completed = 'Yes' THEN 1.0 ELSE 0.0 END) OVER(PARTITION BY d.Department, r.Staff_Group) / 
         COUNT(r.id_number) OVER(PARTITION BY d.Department, r.Staff_Group)) * 100, 1
    ) || '%' as ward_stgroup_completion_rate
FROM renal_table r
INNER JOIN departments_table d ON r.id_number = d.id_number
"""

# Execute query and pull results
df_final_triage = pd.read_sql_query(nested_partition_query, conn)

# 6. PRINT CLEAN INSIGHT REPORT
print("\n" + "🔮" * 45)
print("       PRODUCTION REPORT: NESTED CLINICAL COMPLIANCE MATRIX")
print("🔮" * 45)
# Print a diverse slice showing rows from 2A Wards, 3B Wards, and 4A Wards
print(df_final_triage.iloc[[0, 1, 35, 36, 130, 131]])
print("🔮" * 45 + "\n")

conn.close()
