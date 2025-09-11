
import numpy as np
import pandas as pd
from flask import jsonify, request
from src.app.db_queries import (
    load_main_table_cached,
    get_trip_points, get_all_trip_locations, get_trip_map, get_users_with_summary, get_engine

)
from src.app.utils.cache import cached_reverse_geocode
from src.app.utils.helpers import get_time_range

# ---------- /trips (GET) ----------
def list_trips():
    df = load_main_table_cached()
    required = {"unique_id", "device_id", "timestamp"}
    if df.empty or not required.issubset(df.columns):
        missing = required - set(df.columns)
        return jsonify({"error": f"Missing column(s): {', '.join(missing)}"}), 400

    agg = {"device_id": "first", "timestamp": ["min", "max"]}
    if "trip_distance_used" in df.columns:
        agg["trip_distance_used"] = "first"

    trips = df.groupby("unique_id").agg(agg).reset_index()

    # Flatten columns
    cols = ["unique_id", "device_id", "start_time", "end_time"]
    if "trip_distance_used" in df.columns:
        trips.columns = cols + ["trip_distance_used"]
    else:
        trips.columns = cols

    trips = trips.replace({np.nan: None})
    trips["start_time"] = trips["start_time"].astype(str)
    trips["end_time"] = trips["end_time"].astype(str)
    return jsonify(trips.to_dict(orient="records"))

# ---------- /trips/<id> (GET) ----------
def trip_details(unique_id: int):
    df = load_main_table_cached()
    trip = df[df["unique_id"] == unique_id]
    if trip.empty:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify({
        "unique_id": unique_id,
        "device_id": trip["device_id"].iloc[0],
        "start_time": str(trip["timestamp"].min()),
        "end_time": str(trip["timestamp"].max())
    })

# ---------- /trips/stats/<id> (GET) ----------
def trip_stats(unique_id: int):
    df = load_main_table_cached()
    trip = df[df["unique_id"] == unique_id]
    if trip.empty:
        return jsonify({"error": "Trip not found"}), 404

    duration = (trip["timestamp"].max() - trip["timestamp"].min()).total_seconds() / 60.0
    resp = {"unique_id": unique_id, "duration_minutes": round(duration, 2)}
    if "trip_distance_used" in trip.columns and not trip["trip_distance_used"].isna().all():
        resp["distance_km"] = round(float(trip["trip_distance_used"].iloc[0]), 2)
    if "safe_score" in trip.columns and not trip["safe_score"].isna().all():
        resp["safe_score"] = round(float(trip["safe_score"].iloc[0]), 2)
    return jsonify(resp)

# ---------- /trips/location/<id> (GET) ----------
"""def trip_location(unique_id: int):
    df = get_trip_points(unique_id)
    if df.empty:
        return jsonify({"error": "Trip not found"}), 404
    row = df.iloc[0]
    from_loc = cached_reverse_geocode(row["start_latitude"], row["start_longitude"])
    to_loc   = cached_reverse_geocode(row["end_latitude"],   row["end_longitude"])
    return jsonify({
        "unique_id": unique_id,
        "from": f"({row['start_latitude']}, {row['start_longitude']}) → {from_loc}",
        "to":   f"({row['end_latitude']}, {row['end_longitude']}) → {to_loc}"
    })"""

from datetime import datetime

def convert_unix_ms_to_str(unix_ms):
    dt = datetime.fromtimestamp(unix_ms / 1000)
    return dt.strftime("%Y-%m-%d %I:%M %p")

def trip_location(unique_id: int):
    df = get_trip_points(unique_id)
    if df.empty:
        return jsonify({"error": "Trip not found"}), 404
    
    row = df.iloc[0]
    
    from_loc = cached_reverse_geocode(row["start_latitude"], row["start_longitude"])
    to_loc   = cached_reverse_geocode(row["end_latitude"], row["end_longitude"])
    
    return jsonify({
        "unique_id": unique_id,
        "from": f"({row['start_latitude']}, {row['start_longitude']}) → {from_loc}",
        "to":   f"({row['end_latitude']}, {row['end_longitude']}) → {to_loc}",
        "start_time": convert_unix_ms_to_str(int(row["start_time"])),
        "end_time": convert_unix_ms_to_str(int(row["end_time"]))
    })


# ---------- /locations/<id> (GET) ----------
def raw_locations(unique_id: int):
    df = get_all_trip_locations(unique_id)
    if df.empty:
        return jsonify({"error": "No location data"}), 404
    df = df.dropna(subset=["latitude", "longitude", "timestamp"]).copy()
    df["timestamp"] = df["timestamp"].astype(str)
    return jsonify({
        "unique_id": unique_id,
        "locations": df[["latitude", "longitude", "timestamp"]].to_dict(orient="records")
    })

# ---------- /trips/map/<track_id> (GET) ----------
def trip_map(track_id: int):
    df = get_trip_map(track_id)
    if df.empty:
        return jsonify({"error": "Route not found"}), 404
    enriched = []
    for _, row in df.iterrows():
        enriched.append({
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "timestamp": str(row["timestamp"]),
            "location": cached_reverse_geocode(row["latitude"], row["longitude"])
        })
    return jsonify({"track_id": track_id, "route": enriched})

# ---------- /users (GET) ----------
"""def list_users():
    df = get_users_with_summary()

    if df.empty:
        return jsonify([])

    result = df.to_dict(orient="records")
    return jsonify(result)
"""

def list_users():
    filter_val = request.args.get("filter")
    df = get_users_with_summary()

    if df.empty:
        return jsonify([])

    # Ensure timestamp is datetime and UTC
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    if filter_val:
        now = pd.Timestamp.now() # use actual current time
        start = get_time_range(filter_val, now)
        if not start:
            return jsonify({"error": "Invalid filter"}), 400

        df = df[df["timestamp"] >= start]
        if df.empty:
            return jsonify({"error": "No data"}), 404
   # clean timestamps before jsonify
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["timestamp"] = df["timestamp"].dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
        df["timestamp"] = df["timestamp"].replace({pd.NaT: None})

    return jsonify(df.to_dict(orient="records"))


def list_trips_with_user():
    df = load_main_table_cached()
    filter_val = request.args.get("filter")
    cols = {"unique_id", "device_id", "timestamp", "trip_distance_used", "user_id"}
    if df.empty or not cols.issubset(df.columns):
        missing = cols - set(df.columns)
        return jsonify({"error": f"Missing column(s): {', '.join(missing)}"}), 400
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    if filter_val:
        now = pd.Timestamp.now() # use actual current time
        start = get_time_range(filter_val, now)
        if not start:
            return jsonify({"error": "Invalid filter"}), 400

        df = df[df["timestamp"] >= start]
        if df.empty:
            return jsonify({"error": "No data"}), 404

    # Drop null distances and filter for > 1 km
    df = df.dropna(subset=["trip_distance_used"])
    df = df[df["trip_distance_used"] > 1]

    # Load users table to get names
    engine = get_engine()
    users_df = pd.read_sql("SELECT id, name FROM users", con=engine)
    df = df.merge(users_df, how="left", left_on="user_id", right_on="id")

    # Aggregate like original list_trips()
    agg = {"device_id": "first", "timestamp": ["min", "max"], "name": "first"}
    agg["trip_distance_used"] = "first"

    trips = df.groupby("unique_id").agg(agg).reset_index()

    # Flatten columns
    trips.columns = ["unique_id", "device_id", "start_time", "end_time", "name", "trip_distance_used"]

    trips = trips.replace({np.nan: None})
    trips["start_time"] = trips["start_time"].astype(str)
    trips["end_time"] = trips["end_time"].astype(str)

    return jsonify(trips.to_dict(orient="records"))
