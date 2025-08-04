import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Set page
st.set_page_config(page_title="Maintenance Prediction", layout="wide")

# Validate session
if "selected_aircraft" not in st.session_state:
    st.warning("No aircraft selected. Please go back.")
    st.stop()

aircraft_id = st.session_state.selected_aircraft
st.title(f"🛠 Maintenance Prediction for Aircraft: {aircraft_id}")

# === Train Model (you can later replace with joblib.load)
data = {
    'Flight_Hours': [1000, 400, 1200, 200, 850, 1600, 300, 900, 1800, 100],
    'Landings': [500, 150, 600, 80, 400, 900, 100, 450, 950, 30],
    'Engine_Temp': [620, 540, 650, 500, 610, 680, 520, 630, 700, 490],
    'Vibration': [3.0, 1.2, 3.4, 1.0, 2.5, 3.8, 1.1, 3.1, 4.0, 0.9],
    'Last_Maintenance': [150, 60, 200, 40, 120, 250, 50, 130, 270, 30],
    'Maintenance_Needed': [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]
}
df = pd.DataFrame(data)
X = df.drop('Maintenance_Needed', axis=1)
y = df['Maintenance_Needed']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# === User Input
st.subheader("🔧 Enter Current Flight Data:")
flight_hours = st.slider("Flight Hours", 0, 2000, 500)
landings = st.slider("Landings", 0, 1000, 250)
engine_temp = st.slider("Engine Temp (°C)", 400, 800, 600)
vibration = st.slider("Vibration Level", 0.0, 5.0, 2.0)
last_maintenance = st.slider("Hours Since Last Maintenance", 0, 300, 100)

input_data = pd.DataFrame([[flight_hours, landings, engine_temp, vibration, last_maintenance]],
    columns=['Flight_Hours', 'Landings', 'Engine_Temp', 'Vibration', 'Last_Maintenance'])

# === Prediction
prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

st.subheader("📊 Maintenance Prediction Result:")
if prediction == 1:
    st.error(f"⚠️ Maintenance is likely needed. Confidence: {probability:.2%}")
else:
    st.success(f"✅ No immediate maintenance needed. Confidence: {1 - probability:.2%}")

st.markdown("### 🔍 Input Summary")
st.dataframe(input_data)

# === Component Expiry Alert
st.subheader("🚨 Expired Components Check:")
try:
    components_df = pd.read_csv("data/components.csv")
    components_df["Expiry Date"] = pd.to_datetime(components_df["Expiry Date"])
    expired = components_df[
        (components_df["Aircraft ID"] == aircraft_id) &
        (components_df["Expiry Date"] < pd.Timestamp.today())
    ]
    if not expired.empty:
        st.error("⚠️ The following components are expired:")
        st.dataframe(expired)
    else:
        st.success("✅ No components are expired.")
except Exception as e:
    st.warning("Component data not found or incorrect format.")

# === Maintenance History
st.subheader("📜 Maintenance History:")
try:
    history_df = pd.read_csv("data/maintenance_log.csv")
    history_df = history_df[history_df["Aircraft ID"] == aircraft_id]
    if not history_df.empty:
        st.dataframe(history_df)
    else:
        st.info("No history records found for this aircraft.")
except Exception as e:
    st.warning("Maintenance history file missing or invalid.")

# === Back Button
if st.button("⬅️ Back to Aircraft List"):
    st.switch_page("pages/aircraft_list.py")
