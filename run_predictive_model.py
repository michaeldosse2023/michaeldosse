import os
import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import xgboost as xgb

print("🤖 Initializing Moodle Predictive Analytics Engine [Phase 3: ML]...")

# 1. Load Data
DATA_DIR = "data"
DEPT_FILE = os.path.join(DATA_DIR, "departments.csv")
RENAL_FILE = os.path.join(DATA_DIR, "renal_borne.csv")

df_dept = pd.read_csv(DEPT_FILE)
df_renal = pd.read_csv(RENAL_FILE)

# 2. Rebuild our SQL Sandbox to create the training dataset
conn = sqlite3.connect(":memory:")
df_dept.to_sql("departments_table", conn, if_exists="replace", index=False)
df_renal.to_sql("renal_table", conn, if_exists="replace", index=False)

ward_metrics_data = [
    ('Pharmacy', 3.1, 8),
    ('Theatres', 6.4, 22),
    ('2A Wards', 4.5, 14),
    ('3B Wards', 8.2, 31),
    ('4A Wards', 6.1, 19),
    ('Emergency Medicine', 9.1, 45),
    ('Therapy Services', 2.8, 5)
]

cursor = conn.cursor()
cursor.execute("CREATE TABLE ward_stress_table (Target_Dept TEXT, Patient_Staff_Ratio REAL, Daily_Admissions INT)")
cursor.executemany("INSERT INTO ward_stress_table VALUES (?, ?, ?)", ward_metrics_data)
conn.commit()

# Pull integrated features for the machine learning model
ml_query = """
SELECT 
    CASE WHEN r.Completed = 'Yes' THEN 1 ELSE 0 END as Label,
    w.Patient_Staff_Ratio,
    r.Staff_Group
FROM renal_table r
INNER JOIN departments_table d ON r.id_number = d.id_number
INNER JOIN ward_stress_table w ON TRIM(d.Department) = TRIM(w.Target_Dept)
"""

# w.Daily_Admissions,

df_ml = pd.read_sql_query(ml_query, conn)
conn.close()

# 3. Feature Engineering: Convert categorical Staff_Group to numbers (One-Hot Encoding)
df_ml = pd.get_dummies(df_ml, columns=['Staff_Group'], drop_first=True)

# Separate features (X) and target label (y)
X = df_ml.drop('Label', axis=1)
y = df_ml['Label']

# Create a duplicated pool of our records to simulate a larger staff workforce
df_expanded_pool = pd.concat([df_ml] * 5, ignore_index=True)

# Add a tiny bit of random variation to the staff ratios so they aren't identical copies
noise = np.random.normal(0, 0.1, size=len(df_expanded_pool))
df_expanded_pool['Patient_Staff_Ratio'] = df_expanded_pool['Patient_Staff_Ratio'] + noise

# Separate features (X) and target label (y) using your new expanded pool
X = df_expanded_pool.drop('Label', axis=1)
y = df_expanded_pool['Label']

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)

print(f"📊 Training Pool: {len(X_train)} records | Testing Pool: {len(X_test)} records")

# 5. Train the XGBoost Classifier
# scale_pos_weight helps balance out data if there are more completers than slow-completers
model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=2,
    learning_rate=0.3,
    random_state=42,
    scale_pos_weight=0.5,
    eval_metric='logloss'
)

print("🏋️‍♂️ Training the XGBoost Tree Ensemble...")
model.fit(X_train, y_train)

#*************************************
# ***** CODES BUILDING EXERCISE *****
#*************************************
# Assuming 'model' is our trained XGBoost classifier
scores = model.feature_importances_
features = X.columns

# This creates a dictionary pairing each feature name with its score
importance_dict = dict(zip(features, scores))
print(importance_dict)

df_importance = pd.DataFrame(list(importance_dict.items()), columns=['Feature', 'Score'])
df_sorted = df_importance.sort_values(by='Score', ascending=False)
print(df_sorted)

#*************************************
# ***** CODES BUILDING EXERCISE/ Stop
#*************************************

# 6. Evaluate Model Performance
y_pred = model.predict(X_test)

print("\n" + "🎯" * 45)
# RENDER ALL_CAPS TEXT FOR CONTEXTUAL CLARITY
print("          XGBOOS COMPLIANCE PREDICTION REPORT")
print("🎯" * 45)
print(f"Overall Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.1f}%")
print("\nDetailed Performance Metrics:")
print(classification_report(y_test, y_pred, target_names=['Slow-Completer (0)', 'Compliant (1)']))
print("🎯" * 45 + "\n")