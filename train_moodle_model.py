import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import mlflow
import mlflow.sklearn

# Ensure the local models directory exists
os.makedirs('models', exist_ok=True)

# Set the name of our MLflow Experiment track
mlflow.set_experiment("Workforce_Compliance_Risk_Modeling")

print("🚀 Loading historical training datasets (Semicolon Separated)...")


def load_clean_csv(filepath):
    df = pd.read_csv(filepath, sep=';')
    df.columns = [col.replace('"', '').strip() for col in df.columns]
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.replace('"', '').str.strip()
    return df


# --- PROTECT THE EXECUTION CODE added on 15 Jul 2026 ---
if __name__ == "__main__":
    # Move ALL of your actual execution code here (indented by 4 spaces):
    # This includes loading raw files, setting up MySQL, and training.

    master_df = ...
    unique_staff = sorted([str(g) for g in master_df['Staff_Group'].unique() if pd.notna(g)])
    # ... (rest of your model training code goes here, indented & 15 Jul 2026 addition stops here)


badgernet = load_clean_csv('data/badgernet.csv')
dementia = load_clean_csv('data/dementia.csv')
renal = load_clean_csv('data/renal.csv')
anaphylaxis = load_clean_csv('data/anaphylaxis.csv')
diabetes = load_clean_csv('data/diabetes.csv')

badgernet['Course_ID'] = 0
dementia['Course_ID'] = 1
renal['Course_ID'] = 2
anaphylaxis['Course_ID'] = 3
diabetes['Course_ID'] = 4

master_df = pd.concat([badgernet, dementia, renal, anaphylaxis, diabetes], ignore_index=True)

print("⚙️ Engineering analytical modeling features...")
snapshot_date = pd.to_datetime('2026-07-09')
master_df['Parsed_Enrolment'] = pd.to_datetime(master_df['Enrolment_Date'], errors='coerce', dayfirst=True)
master_df['Parsed_Access'] = pd.to_datetime(master_df['Last_access'], errors='coerce', dayfirst=True)

master_df['Days_Since_Enrolled'] = (snapshot_date - master_df['Parsed_Enrolment']).dt.days.fillna(0)
master_df['Days_Inactive'] = (snapshot_date - master_df['Parsed_Access']).dt.days.fillna(
    master_df['Days_Since_Enrolled'])

master_df['Completed_Clean'] = master_df['Completed'].astype(str).str.lower()
master_df['Status'] = master_df['Completed_Clean'].apply(
    lambda x: 'active' if x in ['yes', 'true', '1', 'completed'] else 'slow-completers'
)

unique_staff = sorted([str(g) for g in master_df['Staff_Group'].unique() if pd.notna(g)])
unique_roles = sorted([str(r) for r in master_df['Role'].unique() if pd.notna(r)])

staff_map = {name: i for i, name in enumerate(unique_staff)}
role_map = {name: i for i, name in enumerate(unique_roles)}

master_df['Staff_Group_Code'] = master_df['Staff_Group'].map(staff_map).fillna(-1)
master_df['Role_Code'] = master_df['Role'].map(role_map).fillna(-1)

joblib.dump(staff_map, 'models/staff_map.joblib')
joblib.dump(role_map, 'models/role_map.joblib')

X = master_df[['Staff_Group_Code', 'Role_Code', 'Days_Since_Enrolled', 'Days_Inactive', 'Course_ID']]
y = master_df['Status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# --- WEEK 42 ACTION TASK: RUN MULTIPLE VARIATIONS ---
hyperparameter_options = [50, 100, 150]
best_accuracy = 0.0
best_model = None

print("\n🧪 Beginning MLflow Experiment Tracking Runs...")

for estimators in hyperparameter_options:
    # Open an explicit, isolated experiment run context in MLflow
    with mlflow.start_run(run_name=f"rf_estimators_{estimators}"):

        print(f"  ↳ Training Random Forest with n_estimators={estimators}...")
        model = RandomForestClassifier(n_estimators=estimators, random_state=42)
        model.fit(X_train, y_train)

        # Calculate validation metric
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)

        # LOG PARAMS & METRICS TO MLFLOW REGISTRY
        mlflow.log_param("n_estimators", estimators)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("accuracy", accuracy)

        # Log the actual model object artifact to MLflow storage
        mlflow.sklearn.log_model(model, "model")

        print(f"    Logged to MLflow successfully. Accuracy: {accuracy * 100:.1f}%")

        # Track our champion model iteration
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model

# Save our absolute champion model directly to production path for app.py
if best_model is not None:
    joblib.dump(best_model, 'models/moodle_intervention_model.joblib')
    print(f"\n🏆 Champion Model Version Saved successfully! Top Accuracy: {best_accuracy * 100:.1f}%")

