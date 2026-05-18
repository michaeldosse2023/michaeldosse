import streamlit as st
import pandas as pd
import joblib  # Switched from pickle to joblib
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Moodle Intervention Portal", layout="wide", page_icon="🎓")
st.title("🎓 Moodle Student Intervention Portal")
st.markdown("### Michael Dosse AI Intelligence Unit")
st.markdown("""
    This tool uses **Machine Learning** to predict student completion risks 
    across 5 different courses. Adjust the profile on the left to see the 
    real-time Risk Priority Score.
""")

# --- 2. LOAD THE MOODLE BRAIN ---
model_path = 'models/moodle_intervention_model.joblib'

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error(f"🚨 Model file not found at {model_path}! Please run the trainer script first.")
    st.stop()

# --- 3. SIDEBAR INPUTS --- Added on 16 April
# Load the maps we created during training
staff_map = joblib.load('models/staff_map.joblib')
role_map = joblib.load('models/role_map.joblib')

# In your sidebar, use the keys from the maps as the options!
staff_group = st.sidebar.selectbox("Staff Group", options=list(staff_map.keys()))
role = st.sidebar.selectbox("Role", options=list(role_map.keys()))

# Get the codes to send to the model
staff_code = staff_map[staff_group]
role_code = role_map[role]

# New Course Selector
course = st.sidebar.selectbox("Select Course", options=["BadgerNet", "Dementia", "Renal", "Anaphylaxis", "Diabetes"])
# Update the ID logic
if course == "BadgerNet":
    course_id = 0
elif course == "Dementia":
    course_id = 1
elif course == "Renal":
    course_id = 2
elif course == "Anaphylaxis":
    course_id = 3
else:
    course_id = 4

# Updated Selectboxes for Staff and Role
# Note: In a later step, we can pull these names directly from your CSV!
staff_group_code = st.sidebar.selectbox("Staff Group Code", options=[0, 1, 2, 3, 4, 5],
                                        help="Numeric code from your dataset")
role_code = st.sidebar.selectbox("Role Code", options=[0, 1, 2, 3, 4, 5], help="Numeric code from your dataset")

days_enrolled = st.sidebar.slider("Days Since Enrolled", 0, 365, 30)
days_inactive = st.sidebar.slider("Days Inactive", 0, 30, 7)

# --- 4. PREDICTION LOGIC ---
# IMPORTANT: The columns must match the training script EXACTLY (Order & Name)
input_df = pd.DataFrame(
    [[staff_group_code, role_code, days_enrolled, days_inactive, course_id]],
    columns=['Staff_Group_Code', 'Role_Code', 'Days_Since_Enrolled', 'Days_Inactive', 'Course_ID']
)

# Calculate Risk Probability
# [0][0] is usually the probability of 'Risk/Incomplete' depending on your data labels
risk_score = model.predict_proba(input_df)[0][0] * 100

# --- 5. DISPLAY RESULTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Priority Analysis: {course}")

    # Visual Risk Metric
    st.metric(label="Risk Priority Score", value=f"{risk_score:.1f}%")
    st.progress(risk_score / 100)

    if risk_score > 70:
        st.error("🔴 HIGH PRIORITY: Urgent Intervention Needed")
    elif risk_score > 40:
        st.warning("🟡 MEDIUM PRIORITY: Monitor Progress")
    else:
        st.success("🟢 LOW PRIORITY: On Track")

with col2:
    st.subheader("Recommended Actions")
    if days_inactive > 14:
        st.info("⚠️ **Action:** Send 'Engagement Check-in' email via Moodle.")

    if risk_score > 60:
        st.warning("📞 **Action:** High risk detected. Refer to Clinical Lead for review.")

    if risk_score <= 60 and days_inactive <= 14:
        st.write("✅ **Action:** No immediate action required. Keep up the good work!")

# --- 6. FOOTER ---
st.markdown("---")
st.caption(f"Michael Dosse System | Course Context: {course} | Predicted using RandomForest v2.0")
