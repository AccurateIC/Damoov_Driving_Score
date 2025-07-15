
from fastapi import FastAPI, Query
from datetime import timedelta
import pandas as pd
import sqlite3

app = FastAPI()

DB_PATH = "D:/Downloadss/tracking_db/tracking_db.db"
TABLE_NAME = "SampleTable"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT timestamp, device_id, unique_id, trip_distance_used
        FROM SampleTable
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    return df.dropna(subset=['timestamp'])

@app.get("/performance_summary")
def get_performance_summary(filter: str = Query(..., description="Use: last_1_week, last_2_weeks, last_1_month, last_2_months")):
    df = load_data()

    now = df['timestamp'].max()
    if pd.isna(now):
        return {"error": "No valid timestamps in database."}

    time_ranges = {
        "last_1_week": now - timedelta(weeks=1),
        "last_2_weeks": now - timedelta(weeks=2),
        "last_1_month": now - timedelta(days=30),
        "last_2_months": now - timedelta(days=60)
    }

    if filter not in time_ranges:
        return {"error": "Invalid filter value."}

    start_date = time_ranges[filter]
    filtered_df = df[df['timestamp'] >= start_date]

    if filtered_df.empty:
        return {"error": "No data found for the selected time filter."}

    # Deduplicate trips
    trip_df = filtered_df.drop_duplicates(subset="unique_id")
    trip_df = trip_df[trip_df['trip_distance_used'] <= 500]  # Remove outliers

    # Match filtered_df with valid trips only
    filtered_df = filtered_df[filtered_df['unique_id'].isin(trip_df['unique_id'])]

    summary = {
        "new_drivers": trip_df['device_id'].nunique(),
        "active_drivers": trip_df['device_id'].nunique(),
        "trips_number": trip_df['unique_id'].nunique(),
        "mileage": round(trip_df['trip_distance_used'].sum(), 2),
        "time_of_driving": round(
            (filtered_df.groupby('unique_id')['timestamp'].max() -
             filtered_df.groupby('unique_id')['timestamp'].min()).dt.total_seconds().sum() / 60, 2
        )
    }
    return summary

@app.get("/safe_driving_summary")
def get_safe_driving_summary(filter: str = Query(..., description="Use: last_1_week, last_2_weeks, last_1_month, last_2_months")):
    df = load_data()

    conn = sqlite3.connect(DB_PATH)
    score_df = pd.read_sql_query("""
        SELECT unique_id, acc_score, dec_score, cor_score, spd_score, phone_score, safe_score, timestamp
        FROM SampleTable
        WHERE safe_score IS NOT NULL
    """, conn)
    conn.close()

    score_df['timestamp'] = pd.to_datetime(score_df['timestamp'], errors='coerce')

    now = score_df['timestamp'].max()
    if pd.isna(now):
        return {"error": "No valid timestamps in database."}

    time_ranges = {
        "last_1_week": now - timedelta(weeks=1),
        "last_2_weeks": now - timedelta(weeks=2),
        "last_1_month": now - timedelta(days=30),
        "last_2_months": now - timedelta(days=60)
    }

    if filter not in time_ranges:
        return {"error": "Invalid filter value."}

    start_date = time_ranges[filter]
    filtered_df = score_df[score_df['timestamp'] >= start_date]

    if filtered_df.empty:
        return {"error": "No data found for the selected time filter."}

    # Final summary dictionary
    summary = {
        "trip_count": filtered_df['unique_id'].nunique(),
        "safety_score": round(filtered_df['safe_score'].mean(), 2),
        "acceleration_score": round(filtered_df['acc_score'].mean(), 2),
        "braking_score": round(filtered_df['dec_score'].mean(), 2),
        "cornering_score": round(filtered_df['cor_score'].mean(), 2),
        "speeding_score": round(filtered_df['spd_score'].mean(), 2),
        "phone_usage_score": round(filtered_df['phone_score'].mean(), 2),
    }

    return summary

