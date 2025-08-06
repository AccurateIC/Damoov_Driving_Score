
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
from geopy.geocoders import Nominatim
import numpy as np
from fastapi.responses import JSONResponse

app = Flask(__name__)
CORS(app)

DB_PATH = "D:/Downloadss/tracking_db/tracking_db.db"
TABLE_NAME = "SampleTable"
geolocator = Nominatim(user_agent="trip-location-tester")

# --- Utilities ---
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['tick_timestamp'], unit='s', errors='coerce')
    return df.dropna(subset=['timestamp'])

def get_time_range(filter_val, now):
    return {
        "last_1_week": now - timedelta(weeks=1),
        "last_2_weeks": now - timedelta(weeks=2),
        "last_1_month": now - timedelta(days=30),
        "last_2_months": now - timedelta(days=60)
    }.get(filter_val)

def reverse_geocode(lat, lon):
    try:
        loc = geolocator.reverse((lat, lon), language='en', timeout=10)
        return loc.address if loc else "Unknown location"
    except Exception:
        return "Geocoding error"

# --- Existing Summary APIs ---

@app.route("/performance_summary")
def performance_summary():
    filter_val = request.args.get("filter")
    df = load_data()
    now = df['timestamp'].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400
    df2 = df[df['timestamp'] >= start]
    if df2.empty:
        return jsonify({"error": "No data"}), 404
    trip_df = df2.drop_duplicates("unique_id")
    trip_df = trip_df[trip_df['trip_distance_used'] <= 500]
    df2 = df2[df2['unique_id'].isin(trip_df['unique_id'])]
    summary = {
        "new_drivers": trip_df['device_id'].nunique(),
        "active_drivers": trip_df['device_id'].nunique(),
        "trips_number": trip_df['unique_id'].nunique(),
        "mileage": round(trip_df['trip_distance_used'].sum(), 2),
        "time_of_driving": round(
            (df2.groupby('unique_id')['timestamp'].max() -
             df2.groupby('unique_id')['timestamp'].min()).dt.total_seconds().sum() / 60, 2
        )
    }
    return jsonify(summary)
    

@app.route("/safe_driving_summary")
def safe_driving_summary():
    filter_val = request.args.get("filter")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT unique_id, acc_score, dec_score, cor_score, spd_score, phone_score, safe_score, timestamp
        FROM SampleTable WHERE safe_score IS NOT NULL
    """, conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    now = df['timestamp'].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400
    filtered = df[df['timestamp'] >= start]
    if filtered.empty:
        return jsonify({"error": "No data"}), 404
    summary = {
        "trip_count": filtered['unique_id'].nunique(),
        "safety_score": round(filtered['safe_score'].mean(), 2),
        "acceleration_score": round(filtered['acc_score'].mean(), 2),
        "braking_score": round(filtered['dec_score'].mean(), 2),
        "cornering_score": round(filtered['cor_score'].mean(), 2),
        "speeding_score": round(filtered['spd_score'].mean(), 2),
        "phone_usage_score": round(filtered['phone_score'].mean(), 2)
    }
    return jsonify(summary)

@app.route("/eco_driving_summary")
def eco_driving_summary():
    filter_val = request.args.get("filter")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT unique_id, eco_score, brake_score, tire_score, fuel_score, timestamp
        FROM SampleTable WHERE eco_score IS NOT NULL
    """, conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    now = df['timestamp'].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400
    filt = df[df['timestamp'] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404
    latest = filt.sort_values(by=['unique_id', 'timestamp']).drop_duplicates('unique_id', keep='last')
    valid = latest[(latest['eco_score'] > 0) | (latest['brake_score'] > 0) |
                   (latest['tire_score'] > 0) | (latest['fuel_score'] > 0)]
    if valid.empty:
        return jsonify({"error": "No valid scores"}), 404
    summary = {
        "trip_count": valid['unique_id'].nunique(),
        "eco_score": round(valid['eco_score'].mean(), 2),
        "brakes_score": round(valid['brake_score'].mean(), 2),
        "tires_score": round(valid['tire_score'].mean(), 2),
        "fuel_score": round(valid['fuel_score'].mean(), 2)
    }
    return jsonify(summary)

@app.route("/safety_dashboard_summary")
def safety_dashboard_summary():
    filter_val = request.args.get("filter")
    conn = sqlite3.connect(DB_PATH)
    base_df = pd.read_sql_query("SELECT timestamp, device_id, unique_id, trip_distance_used FROM SampleTable", conn)
    df = pd.read_sql_query("""
        SELECT unique_id, device_id, trip_distance_used, speed_kmh, acc_score,
               dec_score, cor_score, spd_score, phone_score, safe_score, timestamp
        FROM SampleTable WHERE safe_score IS NOT NULL
    """, conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    base_df['timestamp'] = pd.to_datetime(base_df['timestamp'], errors='coerce')
    now = df['timestamp'].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400
    filt = df[df['timestamp'] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404
    latest = filt.sort_values(by=['unique_id', 'timestamp']).drop_duplicates('unique_id', keep='last')
    speed = filt.groupby('unique_id')['speed_kmh'].agg(['max', 'mean']).reset_index()
    speed = speed[speed['max'] < 300]
    max_spd = round(speed['max'].max(), 2) if not speed.empty else 0
    avg_spd = round(speed['mean'].mean(), 2) if not speed.empty else 0
    time_df = base_df[base_df['timestamp'] >= start]
    time_min = round((time_df.groupby('unique_id')['timestamp'].max() -
                      time_df.groupby('unique_id')['timestamp'].min()).dt.total_seconds().sum() / 60, 2)
    summary = {
        "safety_score": round(latest['safe_score'].mean(), 2),
        "trips": latest['unique_id'].nunique(),
        "driver_trips": latest['device_id'].nunique(),
        "mileage_km": round(latest['trip_distance_used'].sum(), 2),
        "time_driven_minutes": time_min,
        "average_speed_kmh": avg_spd,
        "max_speed_kmh": max_spd,
        "phone_usage_percentage": round(latest['phone_score'].mean(), 2),
        "speeding_percentage": round(latest['spd_score'].mean(), 2),
        "phone_usage_speeding_percentage": round(((latest['phone_score'].mean() + latest['spd_score'].mean()) / 2), 2),
        "unique_tags_count": latest['device_id'].nunique()
    }
    return jsonify(summary)

# --- Trip-related APIs below ---

def get_trip_points(unique_id: int):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT s.UNIQUE_ID,
               s.latitude AS start_latitude,
               s.longitude AS start_longitude,
               s.timeStart AS start_time,
               e.latitude AS end_latitude,
               e.longitude AS end_longitude,
               e.timeStart AS end_time
        FROM EventsStartPointTable s
        LEFT JOIN EventsStopPointTable e ON s.UNIQUE_ID = e.UNIQUE_ID
        WHERE s.UNIQUE_ID = ?
    """, conn, params=(unique_id,))
    conn.close()
    return df

def get_all_trip_locations(unique_id: int):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT latitude, longitude, timeStart AS timestamp
        FROM EventsStartPointTable WHERE UNIQUE_ID = ?
        UNION ALL
        SELECT latitude, longitude, timeStart AS timestamp
        FROM EventsStopPointTable WHERE UNIQUE_ID = ?
    """, conn, params=(unique_id, unique_id))
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    return df.sort_values(by='timestamp')

@app.route("/trips", methods=["GET"])
def list_trips_tripapi():
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

    #return JSONResponse(content=trips.to_dict(orient="records"))
    return jsonify(trips.to_dict(orient="records"))


 return list_trips()  # reuse existing list_trips logic above

@app.route("/trips/<int:unique_id>", methods=["GET"])
def trip_details_api(unique_id):
 def trip_details(unique_id: int):
    df = load_data()
    trip = df[df['unique_id'] == unique_id]
    if trip.empty:
        return {"error": "Trip not found"}

    return {
        "unique_id": unique_id,
        "device_id": trip['device_id'].iloc[0],
        "start_time": trip['timestamp'].min(),
        "end_time": trip['timestamp'].max()
    }
 return trip_details(unique_id)

@app.route("/trips/stats/<int:unique_id>", methods=["GET"])
def trip_stats_api(unique_id):
 def trip_stats(unique_id: int):
    df = load_data()
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
 return trip_stats(unique_id)

@app.route("/trips/location/<int:unique_id>", methods=["GET"])
def trip_location_api(unique_id):
    df = get_trip_points(unique_id)
    if df.empty:
        return jsonify({"error": "Trip not found"}), 404
    row = df.iloc[0]
    from_loc = reverse_geocode(row['start_latitude'], row['start_longitude'])
    to_loc = reverse_geocode(row['end_latitude'], row['end_longitude'])
    return jsonify({
        "unique_id": unique_id,
        "from": f"({row['start_latitude']}, {row['start_longitude']}) → {from_loc}",
        "to": f"({row['end_latitude']}, {row['end_longitude']}) → {to_loc}"
    })

@app.route("/locations/<int:unique_id>", methods=["GET"])
def raw_locations_api(unique_id):
    df = get_all_trip_locations(unique_id)
    if df.empty:
        return jsonify({"error": "No location data"}), 404
    df = df.dropna(subset=['latitude','longitude','timestamp'])
    df['timestamp'] = df['timestamp'].astype(str)
    return jsonify({
        "unique_id": unique_id,
        "locations": df[['latitude','longitude','timestamp']].to_dict(orient="records")
    })

@app.route("/trips/map/<int:track_id>", methods=["GET"])
def trip_map_api(track_id):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT latitude, longitude, point_date AS timestamp
        FROM LastKnownPointTable WHERE track_id = ?
    """, conn, params=(track_id,))
    conn.close()
    if df.empty:
        return jsonify({"error": "Route not found"}), 404
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['latitude','longitude','timestamp'])
    df = df.sort_values(by='timestamp')
    enriched = []
    for _, row in df.iterrows():
        enriched.append({
            "latitude": row['latitude'],
            "longitude": row['longitude'],
            "timestamp": str(row['timestamp']),
            "location": reverse_geocode(row['latitude'], row['longitude'])
        })
    return jsonify({"track_id": track_id, "route": enriched})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
