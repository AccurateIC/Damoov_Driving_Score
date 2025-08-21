
from fastapi import FastAPI
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta

app = FastAPI()

# === Database Configuration ===
DB_PATH = "D:/Downloadss/New_db/test.db"  # ✅ Confirmed working
TABLE_NAME = "SampleTable"              # ✅ Confirmed table

# === Load Data from SQLite ===
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['tick_timestamp'], unit='s', errors='coerce')
    return df.sort_values(by='timestamp')

df = load_data()

# === Geopy Setup ===
geolocator = Nominatim(user_agent="trip-location-tester")

def reverse_geocode(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='en', timeout=10)
        return location.address if location else "Unknown location"
    except Exception as e:
        return f"Error: {e}"

# === API 1: List All Trips ===
@app.get("/trips")
def list_trips():
    trips = df.groupby('unique_id').agg({
        'device_id': 'first',
        'timestamp': ['min', 'max'],
        'trip_distance_used': 'first'
    }).reset_index()
    trips.columns = ['unique_id', 'device_id', 'start_time', 'end_time', 'trip_distance_used']
    return trips.to_dict(orient='records')

# === API 2: Trip Details by unique_id ===
@app.get("/trips/{unique_id}")
def trip_details(unique_id: int):
    trip = df[df['unique_id'] == unique_id]
    if trip.empty:
        return {"error": "Trip not found"}

    events = trip[['timestamp', 'event_type']].dropna().to_dict(orient='records')

    return {
        "unique_id": unique_id,
        "device_id": trip['device_id'].iloc[0],
        "start_time": trip['timestamp'].min(),
        "end_time": trip['timestamp'].max(),
        "events": events
    }

# === API 3: Trip Stats ===
@app.get("/trips/stats/{unique_id}")
def trip_stats(unique_id: int):
    trip = df[df['unique_id'] == unique_id]
    if trip.empty:
        return {"error": "Trip not found"}

    duration = (trip['timestamp'].max() - trip['timestamp'].min()).total_seconds() / 60

    return {
        "unique_id": unique_id,
        "distance_km": round(trip['trip_distance'].iloc[0], 2),
        "duration_minutes": round(duration, 2),
        "score": round(trip['score'].iloc[0], 2)
    }

# === API 4: Map Route ===
@app.get("/trips/map/{unique_id}")
def trip_map(unique_id: int):
    trip = df[df['unique_id'] == unique_id]
    if trip.empty:
        return {"error": "Trip not found"}

    route = trip[['latitude', 'longitude', 'timestamp']].dropna().to_dict(orient='records')
    return {
        "unique_id": unique_id,
        "route": route
    }

# === API 5: Raw GPS Locations ===
@app.get("/locations/{unique_id}")
def get_locations(unique_id: int):
    trip = df[df['unique_id'] == unique_id]
    if trip.empty:
        return {"error": "Trip not found"}

    return {
        "unique_id": unique_id,
        "locations": trip[['latitude', 'longitude', 'timestamp']].dropna().to_dict(orient='records')
    }

# === API 6: Start and End Location via Reverse Geocoding ===
@app.get("/trips/location/{unique_id}")
def trip_start_end_verbose(unique_id: int):
    trip_data = df[df['unique_id'] == unique_id]
    if trip_data.empty:
        return {"error": "Trip not found"}

    start_row = trip_data.iloc[0]
    end_row = trip_data.iloc[-1]

    start_lat, start_lon = start_row['latitude'], start_row['longitude']
    end_lat, end_lon = end_row['latitude'], end_row['longitude']

    try:
        from_location = geolocator.reverse((start_lat, start_lon), language='en', timeout=10)
        to_location = geolocator.reverse((end_lat, end_lon), language='en', timeout=10)

        return {
            "unique_id": unique_id,
            "from": f"({start_lat}, {start_lon}) → {from_location.address if from_location else 'Unknown'}",
            "to": f"({end_lat}, {end_lon}) → {to_location.address if to_location else 'Unknown'}"
        }

    except Exception as e:
        return {"error": f"Geocoding failed: {str(e)}"}

# === API 7: Performance Summary (New Drivers, Active Drivers, Trips, Mileage, Time Driven) ===
@app.get("/performance_summary")
def performance_summary(filter: str = "last_2_weeks"):
    now = datetime.now()
    if filter == "last_1_week":
        since = now - timedelta(weeks=1)
    elif filter == "last_1_month":
        since = now - timedelta(days=30)
    elif filter == "last_2_months":
        since = now - timedelta(days=60)
    else:
        since = now - timedelta(weeks=2)

    filtered_df = df[df['timestamp'] >= since]

    new_drivers = filtered_df['device_id'].nunique()
    active_drivers = filtered_df.groupby('device_id')['unique_id'].nunique().gt(0).sum()
    trips = filtered_df['unique_id'].nunique()
    mileage = filtered_df['distance_delta'].sum() if 'distance_delta' in filtered_df.columns else 0
    drive_time = filtered_df.groupby('unique_id').apply(lambda x: (x['timestamp'].max() - x['timestamp'].min()).total_seconds()).sum()

    return {
        "new_drivers": int(new_drivers),
        "active_drivers": int(active_drivers),
        "trips": int(trips),
        "mileage_km": round(mileage, 2),
        "total_drive_time_seconds": int(drive_time)
    }
