import requests
import sqlite3
import pandas as pd
import json

def run_batch_drift_check():
    conn = sqlite3.connect("sqlite/sensor_data.db")
    df = pd.read_sql("SELECT * FROM TrackTable LIMIT 100", conn)
    payload = json.loads(df.to_json(orient="records"))
    response = requests.post("http://localhost:8000/check-drift", json=payload)
    print("Drift Check Response:", response.json())

if __name__ == "__main__":
    run_batch_drift_check()
