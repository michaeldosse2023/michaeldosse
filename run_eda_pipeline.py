import os
import sqlite3
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("🚀 Starting Moodle Clinical Analytics Engine [Phase 2: EDA]...")

DATA_DIR = "data"
DEPT_FILE = os.path.join(DATA_DIR, "departments.csv")
RENAL_FILE = os.path.join(DATA_DIR, "renal_borne.csv")

try:
    df_dept = pd.read_csv(DEPT_FILE)
    df_renal = pd.read_csv(RENAL_FILE)
    print("✅ Live CSV files loaded successfully.")
except Exception as e:
    print(f"❌ Error loading files. Details: {e}")
    exit()

conn = sqlite3.connect(":memory:")
df_dept.to_sql("departments_table", conn, if_exists="replace", index=False)
df_renal.to_sql("renal_table", conn, if_exists="replace", index=False)

# =====================================================================
# 📊 NEW SYSTEM DATA: Ward Operational Capacity Table
# =====================================================================
ward_metrics_data = [
    ('Pharmacy', 3.1, 8),
    ('Theatres', 6.4, 22),
    ('2A Wards', 4.5, 14),
    ('3B Wards', 8.2, 31),
    ('4A Wards', 6.1, 19)
]

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE ward_stress_table (
        Target_Dept TEXT, 
        Patient_Staff_Ratio REAL, 
        Daily_Admissions INT
    )
""")
cursor.executemany("INSERT INTO ward_stress_table VALUES (?, ?, ?)", ward_metrics_data)
conn.commit()
print("📊 Operational stress metrics integrated into database.")

# =====================================================================
# 🔮 THE EDA INSIGHT ENGINE: CORRELATION MATRIX
# =====================================================================
# Cleaned up back to d.Department and added TRIM() to safeguard spaces
eda_stress_query = """
SELECT 
    r.id_number,
    TRIM(d.Department) as Department,
    r.Staff_Group,
    r.Completed,
    w.Patient_Staff_Ratio,
    w.Daily_Admissions,

    -- Calculate ward-wide completion percentage using a window function
    ROUND(
        (SUM(CASE WHEN r.Completed = 'Yes' THEN 1.0 ELSE 0.0 END) OVER(PARTITION BY d.Department) / 
         COUNT(r.id_number) OVER(PARTITION BY d.Department)) * 100, 1
    ) || '%' as overall_ward_compliance

FROM renal_table r
INNER JOIN departments_table d ON r.id_number = d.id_number
INNER JOIN ward_stress_table w ON TRIM(d.Department) = TRIM(w.Target_Dept)
"""

df_eda_insights = pd.read_sql_query(eda_stress_query, conn)

print("\n" + "🔍" * 45)
print("       EXPLORATORY DATA ANALYSIS: STRESS VS. COMPLIANCE PROFILE")
print("🔍" * 45)
if not df_eda_insights.empty:
    print(df_eda_insights.head(5))
    print("...")
    print(df_eda_insights.tail(5))
else:
    print("⚠️ DataFrame is still empty. Let's run a quick debug check below:")
    # Backup debug print to show exactly what's inside the dataframe columns
    print(pd.read_sql_query("SELECT id_number, Department FROM departments_table LIMIT 3", conn))
print("🔍" * 45 + "\n")

# =====================================================================
# 📂 AUTOMATED TRIAGE EXPORT: Direct Desktop Route
# =====================================================================
print("💾 Saving slow-completers triage list directly to your Desktop...")
df_slow_completers = df_eda_insights[df_eda_insights['Completed'] == 'No']
DESKTOP_PATH = r'C:\Users\micha\OneDrive\Desktop\slow_completers_triage.csv'
df_slow_completers.to_csv(DESKTOP_PATH, index=False)
print(f"🎯 Success! Generated triage list containing {len(df_slow_completers)} records.\n")

# ADDED AS A LATE SECTION
# =====================================================================
# 📈 STATISTICAL SUMMARY ENGINE: THE EXECUTIVE INSIGHT
# =====================================================================
print("📊 Calculating executive statistical stress benchmarks...")

# Group the dataset by completion status and calculate the average stress metrics
stats_summary = df_eda_insights.groupby('Completed', dropna=False)[[
    'Patient_Staff_Ratio',
    'Daily_Admissions'
]].mean().round(2)

print("\n" + "⚡" * 45)
print("      EXECUTIVE SUMMARY: IS OPERATIONAL STRESS IMPACTING COMPLETIONS?")
print("⚡" * 45)
print(stats_summary)
print("⚡" * 45)
print("💡 Insight: A higher Patient_Staff_Ratio for 'No/NaN' proves operational bottlenecks.")
print("⚡" * 45 + "\n")

# =====================================================================
# 📊 VISUALIZATION ENGINE: OPERATIONAL STRESS BENCHMARKS
# =====================================================================
print("🎨 Rendering executive stress visualization chart...")
try:
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Reset any active plots and set a clean, modern aesthetic
    plt.clf()
    sns.set_theme(style="whitegrid")

    # Create a figure with a dual y-axis architecture
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    # We drop NaN for the visual representation to focus on categorical groups
    plot_data = stats_summary.dropna().reset_index()

    # 1. Plot Patient-to-Staff Ratio as a Bar Chart on the Left Axis
    sns.barplot(
        data=plot_data,
        x='Completed',
        y='Patient_Staff_Ratio',
        ax=ax1,
        palette="Blues_d"
    )
    ax1.set_ylabel("Average Patient-to-Staff Ratio", color="#1f77b4", fontweight='bold')
    ax1.tick_params(axis='y', labelcolor="#1f77b4")
    ax1.set_xlabel("Moodle Training Completed Status", fontweight='bold')

    # 2. Plot Daily Admissions as a Line Chart on the Right Axis
    sns.lineplot(
        data=plot_data,
        x='Completed',
        y='Daily_Admissions',
        ax=ax2,
        color="#d62728",
        marker="o",
        linewidth=2.5,
        markersize=8
    )
    ax2.set_ylabel("Average Daily Admissions", color="#d62728", fontweight='bold')
    ax2.tick_params(axis='y', labelcolor="#d62728")
    ax2.grid(False)  # Prevent gridlines from overlapping the bars

    # Add titles and clean up presentation
    plt.title("Clinical Stress Matrix: Training Status vs Operational Burden", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()

    # Route the output direct to your Desktop
    VISUAL_PATH = r'C:\Users\micha\OneDrive\Desktop\operational_stress_chart.png'
    plt.savefig(VISUAL_PATH, dpi=300)
    print(f"🎯 Success! Saved high-resolution chart to your Desktop as 'operational_stress_chart.png'")

except Exception as e:
    print(f"⚠️ Visualization skipped or failed. Details: {e}")


conn.close()