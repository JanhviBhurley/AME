import streamlit as st
import pandas as pd

# Set up the page
st.set_page_config(page_title="Registered Aircraft", layout="wide")

# Make sure brand is selected
if "selected_brand" not in st.session_state:
    st.warning("Please go back and select an aircraft brand.")
    st.stop()

# Get selected brand from session
selected_brand = st.session_state.selected_brand

# Load aircraft data from CSV
df = pd.read_csv("data/aircraft_data.csv")

# Filter aircraft for the selected brand
filtered_df = df[df["Manufacturer"] == selected_brand]

# Show brand title and table
st.title(f"✈️ {selected_brand} Aircraft")
st.dataframe(filtered_df, use_container_width=True)

# Optional: Select aircraft to view maintenance history
selected_id = st.selectbox("✈️ Select Aircraft to Predict Maintenance", filtered_df["Aircraft ID"])

if st.button("🔍 Predict Maintenance for Selected Aircraft"):
    st.session_state.selected_aircraft = selected_id
    st.switch_page("pages/maintenance_predict.py")

# Load maintenance log
try:
    log_df = pd.read_csv("data/maintenance_log.csv")
    aircraft_log = log_df[log_df["Aircraft ID"] == selected_id]

    st.subheader(f"🛠 Maintenance History for {selected_id}")
    st.dataframe(aircraft_log, use_container_width=True)

except FileNotFoundError:
    st.error("❌ File 'maintenance_log.csv' not found in 'data' folder. Please check the file name and location.")
except Exception as e:
    st.error(f"⚠️ An unexpected error occurred: {e}")




# Optional: Go back button
if st.button("⬅️ Back to Home"):
    st.switch_page("app.py")