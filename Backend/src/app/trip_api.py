
from fastapi import FastAPI
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()

# === Database Configuration ===
DB_PATH = "D:/Downloadss/tracking_db/tracking_db.db" # ✅ Confirmed working
TABLE_NAME = "SampleTable"              # ✅ Confirmed table

# === Load Data from SQLite ===
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['tick_timestamp'], unit='s', errors='coerce')
    return df.sort_values(by='timestamp')

df = load_data()

#These functions are defined for reusability in the API endpoints
def get_trip_points(unique_id: int):
    """Fetch start and stop GPS points for a given unique_id"""
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        s.UNIQUE_ID,
        s.latitude AS start_latitude,
        s.longitude AS start_longitude,
        s.timeStart AS start_time,
        e.latitude AS end_latitude,
        e.longitude AS end_longitude,
        e.timeStart AS end_time
    FROM EventsStartPointTable s
    LEFT JOIN EventsStopPointTable e ON s.UNIQUE_ID = e.UNIQUE_ID
    WHERE s.UNIQUE_ID = ?
    """
    df = pd.read_sql_query(query, conn, params=(unique_id,))
    conn.close()
    return df

def get_all_trip_locations(unique_id: int):
    """Combine start and stop points into one DataFrame"""
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT UNIQUE_ID, latitude, longitude, timeStart AS timestamp
    FROM EventsStartPointTable
    WHERE UNIQUE_ID = ?
    UNION ALL
    SELECT UNIQUE_ID, latitude, longitude, timeStart AS timestamp
    FROM EventsStopPointTable
    WHERE UNIQUE_ID = ?
    """
    df = pd.read_sql_query(query, conn, params=(unique_id, unique_id))
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    df = df.sort_values(by='timestamp')
    return df


def to_safe_json(df):
    return df.where(pd.notnull(df), None).to_dict(orient='records')



# === Geopy Setup ===
geolocator = Nominatim(user_agent="trip-location-tester")

def reverse_geocode(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='en', timeout=10)
        return location.address if location else "Unknown location"
    except Exception as e:
        return f"Error: {e}"

# === API 1: List All Trips ===
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
import numpy as np

@app.get("/trips")
def list_trips():
    df = load_data()

    # Ensure required columns exist
    required_cols = ['unique_id', 'device_id', 'timestamp', 'trip_distance_used']
    for col in required_cols:
        if col not in df.columns:
            return JSONResponse(content={"error": f"Missing column: {col} in SampleTable"}, status_code=400)

    # Group and summarize
    trips = df.groupby('unique_id').agg({
        'device_id': 'first',
        'timestamp': ['min', 'max'],
        'trip_distance_used': 'first'
    }).reset_index()

    # Rename columns
    trips.columns = ['unique_id', 'device_id', 'start_time', 'end_time', 'trip_distance_used']

    # Replace NaN or out-of-range floats with None
    trips = trips.replace({np.nan: None})

    # Convert timestamps to string for JSON safety
    trips['start_time'] = trips['start_time'].astype(str)
    trips['end_time'] = trips['end_time'].astype(str)

    return JSONResponse(content=trips.to_dict(orient="records"))



# === API 2: Trip Details by unique_id ===
@app.get("/trips/{unique_id}")
def trip_details(unique_id: int):
    trip = df[df['unique_id'] == unique_id]
    if trip.empty:
        return {"error": "Trip not found"}

    return {
        "unique_id": unique_id,
        "device_id": trip['device_id'].iloc[0],
        "start_time": trip['timestamp'].min(),
        "end_time": trip['timestamp'].max()
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
        "distance_km": round(trip['trip_distance_used'].iloc[0], 2),
        "duration_minutes": round(duration, 2),
        "safe score": round(trip['safe_score'].iloc[0], 2)
    }

"""# === API 4: Map Route ===
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
"""

@app.get("/trips/location/{unique_id}")
def trip_start_end_verbose(unique_id: int):
    df = get_trip_points(unique_id)
    if df.empty:
        return {"error": "Trip not found"}

    row = df.iloc[0]
    try:
        start_lat, start_lon = row['start_latitude'], row['start_longitude']
        end_lat, end_lon = row['end_latitude'], row['end_longitude']

        from_location = reverse_geocode(start_lat, start_lon)
        to_location = reverse_geocode(end_lat, end_lon)

        return {
            "unique_id": unique_id,
            "from": f"({start_lat}, {start_lon}) → {from_location}",
            "to": f"({end_lat}, {end_lon}) → {to_location}"
        }

    except Exception as e:
        return {"error": f"Geocoding failed: {str(e)}"}

@app.get("/trips/map/{track_id}")
def trip_map_with_locations(track_id: int):
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT latitude, longitude, point_date AS timestamp
    FROM LastKnownPointTable
    WHERE track_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(track_id,))
    conn.close()

    if df.empty:
        return {"error": "No route found for this track_id"}

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude', 'timestamp'])
    df = df.sort_values(by='timestamp')

    enriched_route = []

    for _, row in df.iterrows():
        location_name = reverse_geocode(row['latitude'], row['longitude'])
        enriched_route.append({
            "latitude": row['latitude'],
            "longitude": row['longitude'],
            "timestamp": row['timestamp'],
            "location": location_name
        })

    return {
        "track_id": track_id,
        "route": enriched_route
    }

"""
@app.get("/locations/{unique_id}")
def get_locations(unique_id: int):
    df = get_all_trip_locations(unique_id)
    if df.empty:
        return {"error": "No location data found for this trip"}

    locations = df[['latitude', 'longitude', 'timestamp']].dropna().to_dict(orient='records')
    return {
        "unique_id": unique_id,
        "locations": locations
    }"""

