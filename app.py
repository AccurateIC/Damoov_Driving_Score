import streamlit as st
import pandas as pd
import requests
import yaml

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Driving Score & Drift Detection", layout="wide")
st.title("🚗 Driving Score & Drift Detection Dashboard")

# Sidebar navigation
page = st.sidebar.selectbox("📂 Choose Feature", [
    "Upload Trip Data",
    "Calculate Score (Single Trip)",
    "Batch Score All Trips",
    "Drift Detection",
    "Get Score by ID",
    "All Scores (Paginated)",
    "Database Stats",
    "System Metrics",
    "View & Edit Config"
])

# Upload Trip Data
if page == "Upload Trip Data":
    st.header("📤 Upload Trip Data to SQLite DB")
    file = st.file_uploader("Upload CSV File", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.write(df.head())
        if st.button("Upload to DB"):
            data = df.to_dict(orient="records")
            response = requests.post(f"{API_URL}/upload-trip-data", json=data)
            st.json(response.json())

# Single Trip Score
elif page == "Calculate Score (Single Trip)":
    st.header("📊 Calculate Score for a Single Trip")
    file = st.file_uploader("Upload CSV for Single Trip", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.write(df.head())
        if st.button("Calculate Score"):
            response = requests.post(f"{API_URL}/calculate-score", json=df.to_dict(orient="records"))
            st.json(response.json())

# Batch Score All Trips
elif page == "Batch Score All Trips":
    st.header("📦 Run Scoring on All Trips in DB")
    if st.button("Start Batch Scoring"):
        response = requests.post(f"{API_URL}/batch-calculate-scores")
        st.json(response.json())

# Drift Detection
elif page == "Drift Detection":
    st.header("🌊 Check Drift in New Trip Data")
    file = st.file_uploader("Upload Current Trip CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        st.write(df.head())
        if st.button("Run Drift Detection"):
            response = requests.post(f"{API_URL}/check-drift", json=df.to_dict(orient="records"))
            st.json(response.json())

# Get Score by Unique ID
elif page == "Get Score by ID":
    st.header("🔍 Fetch Trip Score by Unique ID")
    unique_id = st.text_input("Enter Unique Trip ID")
    if unique_id and st.button("Get Trip Score"):
        response = requests.get(f"{API_URL}/scores/{unique_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Trip not found.")

# Paginated Scores
elif page == "All Scores (Paginated)":
    st.header("📋 View All Scores with Pagination")
    limit = st.number_input("Limit", value=10, min_value=1)
    offset = st.number_input("Offset", value=0, min_value=0)
    if st.button("Fetch Scores"):
        response = requests.get(f"{API_URL}/scores", params={"limit": limit, "offset": offset})
        if response.status_code == 200:
            result = response.json()
            st.write(f"Total: {result['total']}")
            st.dataframe(pd.DataFrame(result["data"]))
        else:
            st.error("Error fetching scores.")

# Database Stats
elif page == "Database Stats":
    st.header("📊 Database Table Stats")
    if st.button("Get Stats"):
        response = requests.get(f"{API_URL}/database-stats")
        st.json(response.json())

# System Metrics
elif page == "System Metrics":
    st.header("📈 Driving Metrics Summary")
    if st.button("Fetch Metrics"):
        response = requests.get(f"{API_URL}/metrics")
        st.json(response.json())

# Config Viewer & Editor
elif page == "View & Edit Config":
    st.header("⚙️ Config Settings (Live YAML Edit)")
    config = requests.get(f"{API_URL}/config").json()
    config_yaml = st.text_area("Current Config (editable)", yaml.dump(config), height=300)

    if st.button("Update Config"):
        try:
            new_config = yaml.safe_load(config_yaml)
            response = requests.put(f"{API_URL}/config", json=new_config)
            if response.status_code == 200:
                st.success("Config updated!")
            else:
                st.error("Failed to update config.")
        except Exception as e:
            st.error(f"Invalid YAML: {e}")
