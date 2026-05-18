import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. LOAD ALL THREE
badgernet = pd.read_csv('data/badgernet.csv')
dementia = pd.read_csv('data/dementia.csv')
renal = pd.read_csv('data/renal.csv') # Now this will work!
anaphylaxis = pd.read_csv('data/anaphylaxis.csv')
diabetes = pd.read_csv('data/diabetes.csv')

# 2. ASSIGN IDs
badgernet['Course_ID'] = 0
dementia['Course_ID'] = 1
renal['Course_ID'] = 2
anaphylaxis['Course_ID'] = 3
diabetes['Course_ID'] = 4

# 3. COMBINE
master_df = pd.concat([badgernet, dementia, renal, anaphylaxis, diabetes], ignore_index=True)

# The "investigation phase" - to see what was under the hood:
#print("Unique Staff Groups:", master_df['Staff_Group'].unique())
#print("Unique Roles:", master_df['Role'].unique())

# 4. MAP THE TEXT TO NUMBERS --- Added on 16 April
# 4.1 Create lists of unique categories (sorted alphabetically to keep IDs consistent)
unique_staff = sorted([str(g) for g in master_df['Staff_Group'].unique() if pd.notna(g)])
unique_roles = sorted([str(r) for r in master_df['Role'].unique() if pd.notna(r)])

# 4.2 Build the dictionaries automatically
staff_map = {name: i for i, name in enumerate(unique_staff)}
role_map = {name: i for i, name in enumerate(unique_roles)}

# 4.3 Apply the mapping
master_df['Staff_Group_Code'] = master_df['Staff_Group'].map(staff_map).fillna(-1)
master_df['Role_Code'] = master_df['Role'].map(role_map).fillna(-1)

# Save these maps so the App can use the exact same numbers!
import joblib
joblib.dump(staff_map, 'models/staff_map.joblib')
joblib.dump(role_map, 'models/role_map.joblib')

# 5. TRAIN THE MULTI-COURSE BRAIN
X = master_df[['Staff_Group_Code', 'Role_Code', 'Days_Since_Enrolled', 'Days_Inactive', 'Course_ID']]
y = master_df['Status']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 6. SAVE
joblib.dump(model, 'models/moodle_intervention_model.joblib')
print("✅ Success! The Multi-Course Engine is Live.")

