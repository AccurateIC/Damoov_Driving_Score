
# flask_server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
import os
import yaml
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from functools import lru_cache
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ---- Load config.yaml ----
with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f) or {}

db_cfg = CONFIG.get("database", {})
main_table  = db_cfg["main_table"]
start_table = db_cfg["start_table"]
stop_table  = db_cfg["stop_table"]
old_table   = db_cfg["old_table"]
map_table   = db_cfg["map_table"]

# ---- Flask setup ----
app = Flask(__name__)
CORS(app)
geolocator = Nominatim(user_agent="trip-location-tester")

# Global engine instance
engine = None

@app.before_request
def setup_database():
    global engine
    if db_cfg.get("type", "sqlite").lower() == "mysql":
        user = db_cfg["user"]
        password = db_cfg["password"]
        host = db_cfg["host"]
        port = db_cfg["port"]
        name = db_cfg["name"]
        engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}",
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600
        )
    else:
        engine = create_engine(
            f"sqlite:///{db_cfg['sqlite_path']}",
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20
        )

# =========================
# Utilities
# =========================
@lru_cache(maxsize=1000)
def cached_reverse_geocode(lat, lon):
    """Cache geocoding results to avoid repeated requests for same coordinates"""
    try:
        loc = geolocator.reverse((lat, lon), language="en", timeout=10)
        return loc.address if loc else "Unknown location"
    except Exception:
        return "Geocoding error"

def load_data() -> pd.DataFrame:
    """Load main table and normalize to a 'timestamp' column."""
    df = pd.read_sql_query(f"SELECT * FROM {main_table}", engine)
    
    # Optimize data types
    if "unique_id" in df.columns:
        df["unique_id"] = df["unique_id"].astype("int32")
    
    if "device_id" in df.columns:
        df["device_id"] = df["device_id"].astype("category")
    
    # Convert only necessary numeric columns
    numeric_cols = ["acc_score", "dec_score", "cor_score", "spd_score", 
                   "phone_score", "safe_score", "trip_distance_used", "speed_kmh"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # normalize timestamp
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    elif "tick_timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["tick_timestamp"], unit="s", errors="coerce")
    else:
        # last resort: try common variants
        for cand in ("timeStart", "created_at", "point_date"):
            if cand in df.columns:
                df["timestamp"] = pd.to_datetime(df[cand], errors="coerce")
                break
        else:
            df["timestamp"] = pd.NaT

    df = df.dropna(subset=["timestamp"])
    return df

# Cache the data for 60 seconds to avoid repeated database queries
@lru_cache(maxsize=1)
def load_data_cached():
    """Load main table with caching"""
    return load_data()

def get_time_range(filter_val: str, now: pd.Timestamp):
    return {
        "last_1_week": now - timedelta(weeks=1),
        "last_2_weeks": now - timedelta(weeks=2),
        "last_1_month": now - timedelta(days=30),
        "last_2_months": now - timedelta(days=60)
    }.get(filter_val)

def get_trip_points(unique_id: int) -> pd.DataFrame:
    df = pd.read_sql_query(f"""
        SELECT s.UNIQUE_ID,
               s.latitude  AS start_latitude,
               s.longitude AS start_longitude,
               s.timeStart AS start_time,
               e.latitude  AS end_latitude,
               e.longitude AS end_longitude,
               e.timeStart AS end_time
        FROM {start_table} s
        LEFT JOIN {stop_table} e ON s.UNIQUE_ID = e.UNIQUE_ID
        WHERE s.UNIQUE_ID = %s
    """, engine, params=(unique_id,))
    
    return df

def get_all_trip_locations(unique_id: int) -> pd.DataFrame:
    df = pd.read_sql_query(f"""
        SELECT latitude, longitude, timeStart AS timestamp
        FROM {start_table} WHERE UNIQUE_ID = ?
        UNION ALL
        SELECT latitude, longitude, timeStart AS timestamp
        FROM {stop_table} WHERE UNIQUE_ID = ?
    """, engine, params=(unique_id, unique_id))
    
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", errors="coerce")
    return df.sort_values(by="timestamp")

# =========================
# Summary APIs
# =========================

@app.route("/safe_driving_summary")
def safe_driving_summary():
    
    filter_val = request.args.get("filter")
    df = pd.read_sql_query(f"""
        SELECT unique_id, acc_score, dec_score, cor_score, spd_score, phone_score, safe_score, timestamp
        FROM {main_table}
        WHERE safe_score IS NOT NULL
    """, engine)
    

    # normalize timestamp
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    else:
        df["timestamp"] = pd.NaT
    df = df.dropna(subset=["timestamp"])

    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    filtered = df[df["timestamp"] >= start]
    if filtered.empty:
        return jsonify({"error": "No data"}), 404

    summary = {
        "trip_count": int(filtered["unique_id"].nunique()),
        "safety_score": round(filtered["safe_score"].mean(), 2),
        "acceleration_score": round(filtered["acc_score"].mean(), 2),
        "braking_score": round(filtered["dec_score"].mean(), 2),
        "cornering_score": round(filtered["cor_score"].mean(), 2),
        "speeding_score": round(filtered["spd_score"].mean(), 2),
        "phone_usage_score": round(filtered["phone_score"].mean(), 2)
    }

    return jsonify(summary)

@app.route("/eco_driving_summary")
def eco_driving_summary():
    filter_val = request.args.get("filter")
    df = pd.read_sql_query(f"""
        SELECT unique_id, eco_score, brake_score, tire_score, fuel_score, timestamp
        FROM {main_table}
        WHERE eco_score IS NOT NULL
    """, engine)
   

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    filt = df[df["timestamp"] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404

    latest = filt.sort_values(by=["unique_id", "timestamp"]).drop_duplicates("unique_id", keep="last")
    valid = latest[
        (latest["eco_score"] > 0) |
        (latest["brake_score"] > 0) |
        (latest["tire_score"]  > 0) |
        (latest["fuel_score"]  > 0)
    ]
    if valid.empty:
        return jsonify({"error": "No valid scores"}), 404

    summary = {
        "trip_count": int(valid["unique_id"].nunique()),
        "eco_score": round(valid["eco_score"].mean(), 2),
        "brakes_score": round(valid["brake_score"].mean(), 2),
        "tires_score": round(valid["tire_score"].mean(), 2),
        "fuel_score": round(valid["fuel_score"].mean(), 2)
    }
    return jsonify(summary)

@app.route("/safety_dashboard_summary")
def safety_dashboard_summary():
    filter_val = request.args.get("filter")
    base_df = pd.read_sql_query(f"SELECT timestamp, device_id, unique_id, trip_distance_used FROM {main_table}", engine)
    scored_df = pd.read_sql_query(f"""
        SELECT unique_id, device_id, trip_distance_used, speed_kmh, acc_score,
               dec_score, cor_score, spd_score, phone_score, safe_score, timestamp
        FROM {main_table}
        WHERE safe_score IS NOT NULL
    """, engine)
    

    base_df["timestamp"] = pd.to_datetime(base_df["timestamp"], errors="coerce")
    scored_df["timestamp"] = pd.to_datetime(scored_df["timestamp"], errors="coerce")
    base_df = base_df.dropna(subset=["timestamp"])
    scored_df = scored_df.dropna(subset=["timestamp"])

    now = scored_df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    filt = scored_df[scored_df["timestamp"] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404

    latest = filt.sort_values(by=["unique_id", "timestamp"]).drop_duplicates("unique_id", keep="last")

    # Speed stats
    speed = filt.groupby("unique_id")["speed_kmh"].agg(["max", "mean"]).reset_index()
    speed = speed[speed["max"] < 300]  # sanity cap
    max_spd = round(float(speed["max"].max()), 2) if not speed.empty else 0.0
    avg_spd = round(float(speed["mean"].mean()), 2) if not speed.empty else 0.0

    # Time driven (minutes)
    time_df = base_df[base_df["timestamp"] >= start]
    if time_df.empty:
        time_min = 0.0
    else:
        time_min = round(
            (time_df.groupby("unique_id")["timestamp"].max() - time_df.groupby("unique_id")["timestamp"].min())
            .dt.total_seconds().sum() / 60.0, 2
        )

    summary = {
        "safety_score": round(latest["safe_score"].mean(), 2),
        "trips": int(latest["unique_id"].nunique()),
        "driver_trips": int(latest["device_id"].nunique()),
        "mileage_km": round(latest["trip_distance_used"].sum(), 2),
        "time_driven_minutes": time_min,
        "average_speed_kmh": avg_spd,
        "max_speed_kmh": max_spd,
        "phone_usage_percentage": round(latest["phone_score"].mean(), 2),
        "speeding_percentage": round(latest["spd_score"].mean(), 2),
        "phone_usage_speeding_percentage": round(
            ((latest["phone_score"].mean() + latest["spd_score"].mean()) / 2.0), 2
        ),
        "unique_tags_count": int(latest["device_id"].nunique())
    }
    return jsonify(summary)

@app.route("/performance_summary")
def performance_summary():
    filter_val = request.args.get("filter")

    # Load trip data
    df = load_data()
    if df.empty:
        return jsonify({"error": "No trip data found"}), 404

    # Time range filter
    now = df['timestamp'].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df['timestamp'] >= start]
    if df.empty:
        return jsonify({"error": "No data in selected range"}), 404

    # Trips cleanup
    trip_df = df.drop_duplicates("unique_id")
    trip_df = trip_df[trip_df['trip_distance_used'] <= 500]

    # Join with devices table
    with engine.begin() as conn:
        devices_df = pd.read_sql("SELECT device_id, user_id FROM devices", conn)

    trip_df = trip_df.merge(devices_df, on="device_id", how="left")

    # Calculate driving time
    trip_times = df.groupby('unique_id')['timestamp'].agg(['min', 'max'])
    total_drive_time_min = ((trip_times['max'] - trip_times['min']).dt.total_seconds().sum()) / 60

    # Metrics
    active_drivers = trip_df['device_id'].nunique()

    # Devices that appeared for the first time in this range
    historical = df[df['timestamp'] < start]['device_id'].unique().tolist()
    new_drivers = trip_df[~trip_df['device_id'].isin(historical)]['device_id'].nunique()

    summary = {
        "new_drivers": int(new_drivers),
        "active_drivers": int(active_drivers),
        "trips_number": int(trip_df['unique_id'].nunique()),
        "mileage": round(trip_df['trip_distance_used'].sum(), 2),
        "time_of_driving": round(total_drive_time_min, 2)
    }

    return jsonify(summary)




# =========================
# Trips APIs
# =========================

@app.route("/trips", methods=["GET"])
def list_trips_tripapi():
    df = load_data_cached()

    # Ensure required columns exist
    required_cols = ["unique_id", "device_id", "timestamp"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        return jsonify({"error": f"Missing column(s): {', '.join(missing)} in {main_table}"}), 400

    # Group and summarize
    # trip_distance_used may not exist in all schemas; handle safely
    agg_dict = {"device_id": "first", "timestamp": ["min", "max"]}
    if "trip_distance_used" in df.columns:
        agg_dict["trip_distance_used"] = "first"

    trips = df.groupby("unique_id").agg(agg_dict).reset_index()

    # Flatten multiindex columns
    trips.columns = [
        "unique_id",
        "device_id",
        "start_time",
        "end_time"
    ] + (["trip_distance_used"] if "trip_distance_used" in df.columns else [])

    # Replace NaN with None & convert timestamps to strings
    trips = trips.replace({np.nan: None})
    trips["start_time"] = trips["start_time"].astype(str)
    trips["end_time"] = trips["end_time"].astype(str)

    return jsonify(trips.to_dict(orient="records"))

@app.route("/trips/<int:unique_id>", methods=["GET"])
def trip_details_api(unique_id: int):
    df = load_data_cached()
    trip = df[df["unique_id"] == unique_id]
    if trip.empty:
        return jsonify({"error": "Trip not found"}), 404

    return jsonify({
        "unique_id": unique_id,
        "device_id": trip["device_id"].iloc[0],
        "start_time": str(trip["timestamp"].min()),
        "end_time": str(trip["timestamp"].max())
    })

@app.route("/trips/stats/<int:unique_id>", methods=["GET"])
def trip_stats_api(unique_id: int):
    df = load_data_cached()
    trip = df[df["unique_id"] == unique_id]
    if trip.empty:
        return jsonify({"error": "Trip not found"}), 404

    duration = (trip["timestamp"].max() - trip["timestamp"].min()).total_seconds() / 60.0
    resp = {
        "unique_id": unique_id,
        "duration_minutes": round(duration, 2)
    }
    if "trip_distance_used" in trip.columns:
        resp["distance_km"] = round(float(trip["trip_distance_used"].iloc[0]), 2)
    if "safe_score" in trip.columns and pd.notna(trip["safe_score"].iloc[0]):
        resp["safe_score"] = round(float(trip["safe_score"].iloc[0]), 2)
    return jsonify(resp)

@app.route("/trips/location/<int:unique_id>", methods=["GET"])
def trip_location_api(unique_id: int):
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
    })

@app.route("/locations/<int:unique_id>", methods=["GET"])
def raw_locations_api(unique_id: int):
    df = get_all_trip_locations(unique_id)
    if df.empty:
        return jsonify({"error": "No location data"}), 404
    df = df.dropna(subset=["latitude", "longitude", "timestamp"])
    df["timestamp"] = df["timestamp"].astype(str)
    return jsonify({
        "unique_id": unique_id,
        "locations": df[["latitude", "longitude", "timestamp"]].to_dict(orient="records")
    })

@app.route("/trips/map/<int:track_id>", methods=["GET"])
def trip_map_api(track_id: int):
    df = pd.read_sql_query(f"""
        SELECT latitude, longitude, point_date AS timestamp
        FROM {map_table} WHERE track_id = ?
    """, engine, params=(track_id,))
    
    if df.empty:
        return jsonify({"error": "Route not found"}), 404
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["latitude", "longitude", "timestamp"]).sort_values(by="timestamp")

    enriched = []
    for _, row in df.iterrows():
        enriched.append({
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "timestamp": str(row["timestamp"]),
            "location": cached_reverse_geocode(row["latitude"], row["longitude"])
        })
    return jsonify({"track_id": track_id, "route": enriched})

# =========================
# Charts / Metrics APIs
# =========================

@app.route("/summary_graph", methods=["POST"])
def summary_graph():
    params = request.json or {}
    metric = params.get("metric")
    filter_val = params.get("filter_val")

    df = load_data_cached()
    now = df["timestamp"].max()
    start_date = get_time_range(filter_val, now)
    if start_date is None:
        return jsonify({"error": f"Unsupported filter: {filter_val}"}), 400

    filtered_df = df[df["timestamp"] >= start_date]
    if filtered_df.empty:
        return jsonify({"metric": metric, "labels": [], "data": []})

    metric_map = {
        "Safety score": "safe_score",
        "Acceleration": "acc_score",
        "Braking": "dec_score",
        "Cornering": "cor_score",
        "Speeding": "spd_score",
        "Phone usage": "phone_score",
        "Registered assets": lambda d: d["device_id"].nunique(),
        "Active assets": lambda d: d["device_id"].nunique(),
        "Trips": lambda d: d.groupby(d["timestamp"].dt.date)["unique_id"].nunique(),
        "Driving time": lambda d: (d["timestamp"].max() - d["timestamp"].min()).total_seconds() / 60.0
    }

    if metric not in metric_map:
        return jsonify({"error": f"Unsupported metric: {metric}"})

    # Per-day series for certain callable metrics
    if callable(metric_map[metric]):
        if metric == "Trips":
            daily = filtered_df.groupby(filtered_df["timestamp"].dt.date)["unique_id"].nunique().dropna()
            values = daily.tolist()
            labels = daily.index.astype(str).tolist()
            return jsonify({"metric": metric, "labels": labels, "data": values})
        elif metric == "Driving time":
            daily = filtered_df.groupby(filtered_df["timestamp"].dt.date).apply(
                lambda g: (g["timestamp"].max() - g["timestamp"].min()).total_seconds() / 60.0
            ).dropna()
            values = daily.tolist()
            labels = daily.index.astype(str).tolist()
            return jsonify({"metric": metric, "labels": labels, "data": values})
        else:
            total_value = float(metric_map[metric](filtered_df))
            return jsonify({"metric": metric, "labels": [metric], "data": [total_value]})

    # Standard per-day averages for numeric columns
    series = (
        filtered_df.groupby(filtered_df["timestamp"].dt.date)[metric_map[metric]]
        .mean()
        .round(2)
        .dropna()
    )
    return jsonify({
        "metric": metric,
        "labels": series.index.astype(str).tolist(),
        "data": series.tolist()
    })

@app.route("/driver_distribution", methods=["POST"])
def driver_distribution():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    # Predefine bins and labels once
    bins = [0, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    labels = ["<45.0","45-50","50-55","55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100"]

    df = load_data_cached()
    if df.empty or not {"timestamp","safe_score","device_id"} <= set(df.columns):
        return jsonify({"labels": labels, "data": [0]*len(labels)})

    now = df["timestamp"].max()
    start_date = get_time_range(filter_val, now)
    if start_date is None:
        return jsonify({"error": f"Unsupported filter: {filter_val}"}), 400

    # Filter first (reduces data size before sorting/grouping)
    df = df[(df["timestamp"] >= start_date) & (df["safe_score"].notna())]
    if df.empty:
        return jsonify({"labels": labels, "data": [0]*len(labels)})

    # Faster way: sort once per group and take last row
    latest = df.sort_values("timestamp").groupby("device_id", observed=True).tail(1)

    # Bin into ranges
    distribution = (
        pd.cut(latest["safe_score"], bins=bins, labels=labels, right=False)
          .value_counts()
          .reindex(labels, fill_value=0)
    )

    return jsonify({"labels": labels, "data": distribution.tolist()})


@app.route("/safety_params", methods=["POST"])
def safety_params():
    params = request.json or {}
    filter_val = params.get("filter_val")

    df = load_data_cached()
    now = df["timestamp"].max()
    start_date = get_time_range(filter_val, now)
    if start_date is None:
        return jsonify({"error": f"Unsupported filter: {filter_val}"})

    filtered_df = df[df["timestamp"] >= start_date]
    if filtered_df.empty:
        return jsonify({"labels": [], "data": []})

    for col in ["acc_score", "dec_score", "cor_score", "spd_score", "phone_score"]:
        if col not in filtered_df.columns:
            filtered_df[col] = np.nan

    avg_params = {
        "Acceleration": round(filtered_df["acc_score"].mean(), 2),
        "Braking":      round(filtered_df["dec_score"].mean(), 2),
        "Cornering":    round(filtered_df["cor_score"].mean(), 2),
        "Speeding":     round(filtered_df["spd_score"].mean(), 2),
        "Phone usage":  round(filtered_df["phone_score"].mean(), 2)
    }
    return jsonify({"labels": list(avg_params.keys()), "data": list(avg_params.values())})

@app.route("/safety_graph_trend", methods=["POST"])
def safety_graph_trend():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")
    metric = params.get("metric", "safe_score")  # safe_score, acc_score, dec_score, cor_score, spd_score, phone_score

    df = load_data_cached()
    now = df["timestamp"].max()
    start_date = get_time_range(filter_val, now)
    if start_date is None:
        return jsonify({"error": f"Unsupported filter: {filter_val}"}), 400

    filtered_df = df[df["timestamp"] >= start_date].copy()
    if filtered_df.empty or metric not in filtered_df.columns:
        return jsonify({"labels": [], "data": []})

    filtered_df["date"] = filtered_df["timestamp"].dt.date
    daily_avg = (
        filtered_df.groupby("date")[metric]
        .mean()
        .reset_index()
        .dropna()
    )
    return jsonify({
        "labels": daily_avg["date"].astype(str).tolist(),
        "data": daily_avg[metric].round(2).tolist()
    })

@app.route("/mileage_daily", methods=["POST"])
def mileage_daily():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    df = load_data_cached()
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df["timestamp"] >= start]
    if df.empty:
        return jsonify({"labels": [], "data": []})

    trip_df = df.drop_duplicates("unique_id")
    if "trip_distance_used" in trip_df.columns:
        trip_df = trip_df[trip_df["trip_distance_used"] <= 500]
    else:
        return jsonify({"labels": [], "data": []})

    if trip_df.empty:
        return jsonify({"labels": [], "data": []})

    trip_df["date"] = trip_df["timestamp"].dt.date
    daily_mileage = (
        trip_df.groupby("date")["trip_distance_used"]
        .sum()
        .reset_index()
        .dropna()
    )
    return jsonify({
        "labels": daily_mileage["date"].astype(str).tolist(),
        "data": daily_mileage["trip_distance_used"].round(2).tolist()
    })

@app.route("/driving_time_daily", methods=["POST"])
def driving_time_daily():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    df = load_data_cached()
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df["timestamp"] >= start]
    if df.empty:
        return jsonify({"labels": [], "data": []})

    # one row per trip for date assignment
    trip_df = df.drop_duplicates("unique_id")

    # compute per-trip durations on full df (not only dedup)
    trip_times = df.groupby("unique_id")["timestamp"].agg(["min", "max"])
    trip_times["drive_time_min"] = (trip_times["max"] - trip_times["min"]).dt.total_seconds() / 60.0
    trip_times = trip_times.reset_index()

    trip_df = trip_df.merge(trip_times[["unique_id", "drive_time_min"]], on="unique_id", how="left")
    trip_df["date"] = trip_df["timestamp"].dt.date

    daily_time = (
        trip_df.groupby("date")["drive_time_min"]
        .sum()
        .reset_index()
        .dropna()
    )
    return jsonify({
        "labels": daily_time["date"].astype(str).tolist(),
        "data": daily_time["drive_time_min"].round(2).tolist()
    })

# Health check endpoint
@app.route("/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# =========================
# Run
# =========================
if __name__ == "__main__":
    # Initialize database connection
    setup_database()
    
    if engine:
        print("[INFO] Database connection successful ✅")
    else:
        print("[ERROR] Could not connect to database")
        exit(1)

    app.run(host="0.0.0.0", port=5000, debug=True)