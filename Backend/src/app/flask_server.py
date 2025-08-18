

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

DB_PATH = "/home/ankita/Desktop/Damoov/Damoov_Driving_Score/Backend/src/app/tracking_db.db"
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

"""@app.route("/performance_summary")
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
        "mileage": round(trip_df[trip_df['trip_distance_used'] <= 1000]['trip_distance_used'].sum(), 2),
        "time_of_driving": round(
            (df2.groupby('unique_id')['timestamp'].max() -
             df2.groupby('unique_id')['timestamp'].min()).dt.total_seconds().sum() / 60, 2
        )
    }
    return jsonify(summary)"""

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

@app.route("/performance_summary")
def performance_summary():
    filter_val = request.args.get("filter")
    df = load_data()

    # Time range filter
    now = df['timestamp'].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df['timestamp'] >= start]
    if df.empty:
        return jsonify({"error": "No data in selected range"}), 404

    # One row per trip
    trip_df = df.drop_duplicates("unique_id")

    # Filter trips with valid distance
    trip_df = trip_df[trip_df['trip_distance_used'] <= 500]

    # Filter based on valid GPS/timeStart using get_trip_points()
    valid_trip_ids = []
    for uid in trip_df['unique_id']:
        points = get_trip_points(uid)
        if points.empty:
            continue
        row = points.iloc[0]
        if (
            row['start_latitude'] != 0 and row['end_latitude'] != 0 and
            row['start_longitude'] != 0 and row['end_longitude'] != 0 and
            row['start_time'] and row['end_time']
        ):
            valid_trip_ids.append(uid)

    trip_df = trip_df[trip_df['unique_id'].isin(valid_trip_ids)]
    df = df[df['unique_id'].isin(valid_trip_ids)]

    # Time of driving calculation
    trip_times = df.groupby('unique_id')['timestamp'].agg(['min', 'max'])
    total_drive_time_min = ((trip_times['max'] - trip_times['min']).dt.total_seconds().sum()) / 60

    summary = {
        "new_drivers": trip_df['device_id'].nunique(),
        "active_drivers": trip_df['device_id'].nunique(),
        "trips_number": trip_df['unique_id'].nunique(),
        "mileage": round(trip_df['trip_distance_used'].sum(), 2),
        "time_of_driving": round(total_drive_time_min, 2)
    }

    return jsonify(summary)


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

"""@app.route('/summary_graph/<unique_id>/<metric>/<filter_val>', methods=['GET'])
def summary_graph(unique_id, metric, filter_val):
    now = datetime.now()
    start_date, _ = get_time_range(filter_val, now)
    
    df = load_data()
    df = df[df['timestamp'] >= start_date]

    if df.empty:
        return {"metric": metric, "labels": [], "values": []}

    # Map metric names to DB columns
    metric_map = {
        "Safety score": "safe_score",
        "Acceleration": "acc_score",
        "Braking": "dec_score",
        "Cornering": "cor_score",
        "Speeding": "spd_score",
        "Phone usage": "phone_score",
        "Registered assets": lambda d: d['device_id'].nunique(),
        "Active assets": lambda d: d['device_id'].nunique(),
        "Trips": lambda d: d['unique_id'].nunique(),
        "Driving time": lambda d: (d['timestamp'].max() - d['timestamp'].min()).total_seconds() / 60
    }

    if metric not in metric_map:
        return {"error": f"Unsupported metric: {metric}"}

    if callable(metric_map[metric]):
        values = [metric_map[metric](df)]
        labels = [metric]
    else:
        values = df.groupby(df['timestamp'].dt.date)[metric_map[metric]].mean().round(2).tolist()
        labels = sorted(df['timestamp'].dt.date.unique().astype(str))

    return {"metric": metric, "labels": labels, "values": values}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
"""


    # Map metric names to DB columns
metric_map = {
        "Safety score": "safe_score",
        "Acceleration": "acc_score",
        "Braking": "dec_score",
        "Cornering": "cor_score",
        "Speeding": "spd_score",
        "Phone usage": "phone_score",
        "Registered assets": lambda d: d['device_id'].nunique(),
        "Active assets": lambda d: d['device_id'].nunique(),
        "Trips": lambda d: d['unique_id'].nunique(),
        "Driving time": lambda d: (d['timestamp'].max() - d['timestamp'].min()).total_seconds() / 60
}

"""@app.route('/summary_graph', methods=['POST'])
def summary_graph():
    params = request.json
    metric = params.get("metric")
    filter_val = params.get("filter_val")

    now = datetime.now()
    start_date = get_time_range(filter_val, now)

    if start_date is None:
        return {"error": f"Unsupported filter: {filter_val}"}

    df = load_data()

    # Try filtering
    filtered_df = df[df['timestamp'] >= start_date]

    # Fallback if no rows found
    if filtered_df.empty:
        print(f"No rows found for filter {filter_val}, returning full dataset for testing.")
        filtered_df = df.copy()

    # Metric mapping
    metric_map = {
        "Safety score": "safe_score",
        "Acceleration": "acc_score",
        "Braking": "dec_score",
        "Cornering": "cor_score",
        "Speeding": "spd_score",
        "Phone usage": "phone_score",
        "Registered assets": lambda d: d['device_id'].nunique(),
        "Active assets": lambda d: d['device_id'].nunique(),
        "Trips": lambda d: d['unique_id'].nunique(),
        "Driving time": lambda d: (d['timestamp'].max() - d['timestamp'].min()).total_seconds() / 60
    }

    if metric not in metric_map:
        return {"error": f"Unsupported metric: {metric}"}

    # Generate labels and values
    if callable(metric_map[metric]):
        values = [metric_map[metric](filtered_df)]
        labels = [metric]
    else:
        values = (
            filtered_df.groupby(filtered_df['timestamp'].dt.date)[metric_map[metric]]
            .mean()
            .round(2)
            .tolist()
        )
        labels = sorted(filtered_df['timestamp'].dt.date.unique().astype(str))

    return {"metric": metric, "labels": labels, "data": values}
"""

@app.route('/summary_graph', methods=['POST'])
def summary_graph():
    params = request.json
    metric = params.get("metric")
    filter_val = params.get("filter_val")

    # Load data first
    df = load_data()

    # Use dataset's latest timestamp, not current date
    now = df['timestamp'].max()
    start_date = get_time_range(filter_val, now)

    if start_date is None:
        return {"error": f"Unsupported filter: {filter_val}"}

    # Filter data
    filtered_df = df[df['timestamp'] >= start_date]

    # Return empty arrays if no rows match
    if filtered_df.empty:
        return {"metric": metric, "labels": [], "data": []}

    # Metric mapping
    metric_map = {
        "Safety score": "safe_score",
        "Acceleration": "acc_score",
        "Braking": "dec_score",
        "Cornering": "cor_score",
        "Speeding": "spd_score",
        "Phone usage": "phone_score",
        "Registered assets": lambda d: d['device_id'].nunique(),
        "Active assets": lambda d: d['device_id'].nunique(),
        "Trips": lambda d: (
            d.groupby(d['timestamp'].dt.date)['unique_id']
            .nunique() ),
                     

        "Driving time": lambda d: (d['timestamp'].max() - d['timestamp'].min()).total_seconds() / 60
    }



    if metric not in metric_map:
         return {"error": f"Unsupported metric: {metric}"}
    
   # values, labels = [], []

    if callable(metric_map[metric]):
        if metric == "Trips":
            # Trips per day
            daily = filtered_df.groupby(filtered_df['timestamp'].dt.date)['unique_id'].nunique()
        elif metric == "Driving time":
            # Driving time per day in minutes
            daily = filtered_df.groupby(filtered_df['timestamp'].dt.date).apply(
                lambda g: (g['timestamp'].max() - g['timestamp'].min()).total_seconds() / 60
            )
        else:
            # Fallback to old behavior
            total_value = metric_map[metric](filtered_df)
            return {
                "metric": metric,
                "labels": [metric],
                "data": [total_value]
            }

        # Remove NaN days
        daily = daily.dropna()

        # Convert to lists
        values = daily.tolist()
        labels = daily.index.astype(str).tolist()

    else:
        daily_avg = (
            filtered_df.groupby(filtered_df['timestamp'].dt.date)[metric_map[metric]]
            .mean()
            .round(2)
            .dropna()
        )
        values = daily_avg.tolist()
        labels = daily_avg.index.astype(str).tolist()

    return {"metric": metric, "labels": labels, "data": values}

#This will be used when actual data is available
@app.route('/driver_distribution', methods=['POST'])
def driver_distribution():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    # Load & filter by time window (same pattern as /summary_graph)
    df = load_data()  # must include: device_id, safe_score, timestamp
    now = df['timestamp'].max()
    start_date = get_time_range(filter_val, now)
    if start_date is None:
        return {"error": f"Unsupported filter: {filter_val}"}, 400

    df = df[(df['timestamp'] >= start_date) & (df['safe_score'].notna())]
    if df.empty:
        return {
            "labels": ["<45.0","45-50","50-55","55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100"],
            "data": [0]*12
        }

    # --- one score per driver (latest record in the window) ---
    # if your driver id column is different, replace 'device_id' below
    df_sorted = df.sort_values(['device_id', 'timestamp'])
    idx = df_sorted.groupby('device_id')['timestamp'].idxmax()
    latest_per_driver = df_sorted.loc[idx, ['device_id', 'safe_score']]

    # --- bin drivers by their latest safe_score ---
    bins = [0, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    labels = ["<45.0","45-50","50-55","55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100"]

    latest_per_driver['score_range'] = pd.cut(
        latest_per_driver['safe_score'], bins=bins, labels=labels, right=False
    )

    distribution = (
        latest_per_driver['score_range']
        .value_counts()
        .reindex(labels, fill_value=0)
    )

    return {
        "labels": labels,
        "data": distribution.tolist()   # counts of DRIVERS per score bucket
    }


@app.route('/safety_params', methods=['POST'])
def safety_params():
    params = request.json
    filter_val = params.get("filter_val")

    # Load data
    df = load_data()

    # Use latest timestamp from dataset
    now = df['timestamp'].max()
    start_date = get_time_range(filter_val, now)

    if start_date is None:
        return {"error": f"Unsupported filter: {filter_val}"}

    # Filter dataset
    filtered_df = df[df['timestamp'] >= start_date]

    if filtered_df.empty:
        return {"labels": [], "data": []}

    avg_params = {
        "Acceleration": round(filtered_df['acc_score'].mean(), 2),
        "Braking": round(filtered_df['dec_score'].mean(), 2),
        "Cornering": round(filtered_df['cor_score'].mean(), 2),
        "Speeding": round(filtered_df['spd_score'].mean(), 2),
        "Phone usage": round(filtered_df['phone_score'].mean(), 2)
    }

    return {
        "labels": list(avg_params.keys()),
        "data": list(avg_params.values())
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)