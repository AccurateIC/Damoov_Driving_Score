import pandas as pd
from flask import request, jsonify
from src.app.db_queries import (
    load_main_table, load_main_table_cached, get_engine, get_trip_level_data, get_badge_aggregates,
    get_safe_driving_rows, get_eco_driving_rows, get_devices_table, get_performance_data, load_df, get_trip_points_batch, get_top_safe_drivers, get_top_aggressive_drivers
)
from src.app.utils.helpers import get_time_range

# ---------- /safe_driving_summary ----------
def safe_driving_summary():
    filter_val = request.args.get("filter")
    df = get_safe_driving_rows()
    if df.empty:
        return jsonify({"error": "No data"}), 404

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

# ---------- /eco_driving_summary ----------

def eco_driving_summary():
    filter_val = request.args.get("filter")

    # Only load required columns
    cols = ["unique_id", "eco_score", "brake_score", "tire_score", "fuel_score", "timestamp"]
    df = load_df(required_cols=cols)
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        return jsonify({"error": "No data"}), 404

    # Determine time filter
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    filt = df[df["timestamp"] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404

    # Get latest record per trip
    idx = filt.groupby("unique_id")["timestamp"].idxmax()
    latest = filt.loc[idx]

    # Only keep rows with any valid eco-driving score
    valid = latest[
        (latest["eco_score"] > 0) |
        (latest["brake_score"] > 0) |
        (latest["tire_score"] > 0) |
        (latest["fuel_score"] > 0)
    ]
    if valid.empty:
        return jsonify({"error": "No valid scores"}), 404

    # Vectorized aggregation
    agg = valid.agg({
        "eco_score": "mean",
        "brake_score": "mean",
        "tire_score": "mean",
        "fuel_score": "mean",
        "unique_id": "nunique"
    }).to_dict()

    summary = {
        "trip_count": int(agg["unique_id"]),
        "eco_score": round(agg["eco_score"], 2),
        "brakes_score": round(agg["brake_score"], 2),
        "tires_score": round(agg["tire_score"], 2),
        "fuel_score": round(agg["fuel_score"], 2)
    }

    return jsonify(summary)


# ---------- /safety_dashboard_summary ----------
def safety_dashboard_summary():
    filter_val = request.args.get("filter")

    cols = [
        "unique_id", "device_id", "trip_distance_used", "speed_kmh",
        "acc_score", "dec_score", "cor_score", "spd_score", "phone_score",
        "safe_score", "timestamp"
    ]
    df = load_df(required_cols=cols)
    df = df.dropna(subset=["timestamp", "safe_score"])
    if df.empty:
        return jsonify({"error": "No data"}), 404

    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    filt = df[df["timestamp"] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404

    # latest per trip
    idx = filt.groupby("unique_id")["timestamp"].idxmax()
    latest = filt.loc[idx]

    # speed stats
    speed = filt.groupby("unique_id")["speed_kmh"].agg(["max", "mean"])
    speed = speed[speed["max"] < 300]
    max_spd = round(float(speed["max"].max()), 2) if not speed.empty else 0.0
    avg_spd = round(float(speed["mean"].mean()), 2) if not speed.empty else 0.0

    # time driven
    per_trip = filt.groupby("unique_id")["timestamp"].agg(["min", "max"])
    time_min = round((per_trip["max"] - per_trip["min"]).dt.total_seconds().sum() / 60.0, 2)

    agg = latest.agg({
        "safe_score": "mean",
        "phone_score": "mean",
        "spd_score": "mean",
        "trip_distance_used": "sum",
        "device_id": "nunique",
        "unique_id": "nunique"
    }).to_dict()

    summary = {
        "safety_score": round(agg["safe_score"], 2),
        "trips": int(agg["unique_id"]),
        "driver_trips": int(agg["device_id"]),
        "mileage_km": round(agg["trip_distance_used"], 2),
        "time_driven_minutes": time_min,
        "average_speed_kmh": avg_spd,
        "max_speed_kmh": max_spd,
        "phone_usage_percentage": round(agg["phone_score"], 2),
        "speeding_percentage": round(agg["spd_score"], 2),
        "phone_usage_speeding_percentage": round((agg["phone_score"] + agg["spd_score"]) / 2.0, 2),
        "unique_tags_count": int(agg["device_id"])
    }

    return jsonify(summary)


# ---------- /performance_summary ----------
def performance_summary():
    filter_val = request.args.get("filter")

    # Load minimal data
    cols = ["unique_id", "device_id", "trip_distance_used", "timestamp"]
    df = load_df(required_cols=cols).dropna(subset=["timestamp"])
    if df.empty:
        return jsonify({"error": "No data"}), 404

    # Time range
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400
    df = df[df["timestamp"] >= start]
    if df.empty:
        return jsonify({"error": "No data in selected range"}), 404

    # One row per trip
    trip_df = df.drop_duplicates("unique_id")
    trip_df = trip_df[trip_df["trip_distance_used"] <= 500]
    if trip_df.empty:
        return jsonify({"error": "No valid trips"}), 404

    # --- OPTIMIZED: Batch load trip points ---
    trip_ids = trip_df["unique_id"].tolist()
    all_points = get_trip_points_batch(trip_ids)  # new batch function

    # Vectorized validity filter
    mask = (
        (all_points["start_latitude"] != 0) &
        (all_points["end_latitude"] != 0) &
        (all_points["start_longitude"] != 0) &
        (all_points["end_longitude"] != 0) &
        (all_points["start_time"].notna()) &
        (all_points["end_time"].notna())
    )
    valid_trip_ids = all_points.loc[mask, "UNIQUE_ID"].unique()
    if len(valid_trip_ids) == 0:
        return jsonify({"error": "No valid trips"}), 404

    # Final filtered data
    trip_df = trip_df[trip_df["unique_id"].isin(valid_trip_ids)]
    df = df[df["unique_id"].isin(valid_trip_ids)]

    # Driving time
    trip_times = df.groupby("unique_id")["timestamp"].agg(["min", "max"])
    total_drive_time_min = ((trip_times["max"] - trip_times["min"]).dt.total_seconds().sum()) / 60

    summary = {
        "new_drivers": trip_df["device_id"].nunique(),
        "active_drivers": trip_df["device_id"].nunique(),
        "trips_number": trip_df["unique_id"].nunique(),
        "mileage": round(trip_df["trip_distance_used"].sum(), 2),
        "time_of_driving": round(total_drive_time_min, 2)
    }

    return jsonify(summary)

# API for specific user
#@app.route("/user_safety_summary", methods=["GET"])
import logging
# configure logging once in your app (usually in flask_server.py)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def user_safety_dashboard_summary():
    user_id = request.args.get("user_id")
    filter_val = request.args.get("filter")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    cols = [
        "unique_id", "device_id", "trip_distance_used", "speed_kmh",
        "acc_score", "dec_score", "cor_score", "phone_score",
        "safe_score", "timestamp", "user_id"
    ]
    df = load_df(required_cols=cols)
    df = df.dropna(subset=["timestamp", "safe_score", "trip_distance_used"])

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user_id"}), 400

    # filter by user
    df = df[df["user_id"] == user_id]
    if df.empty:
        return jsonify({"error": "No data for this user"}), 404

    # ---- time filter ----
    if filter_val:
        now = df["timestamp"].max()
        start = get_time_range(filter_val, now)
        if not start:
            return jsonify({"error": "Invalid filter"}), 400
        df = df[df["timestamp"] >= start]
        if df.empty:
            return jsonify({"error": "No data in this filter"}), 404

    # ---- latest row per trip ----
    idx = df.groupby("unique_id")["timestamp"].idxmax()
    latest = df.loc[idx]

    # ---- filter out unrealistic trips (1–300 km) ----
    latest = latest[(latest["trip_distance_used"] >= 1) & (latest["trip_distance_used"] <= 300)]

    trips = latest["unique_id"].nunique()
    mileage = latest["trip_distance_used"].sum()

    # ---- speed stats ----
    speed = latest.groupby("unique_id")["speed_kmh"].agg(["max", "mean"])
    speed = speed[speed["max"] < 300]
    max_spd = round(float(speed["max"].max()), 2) if not speed.empty else 0.0
    avg_spd = round(float(speed["mean"].mean()), 2) if not speed.empty else 0.0

    # ---- time driven ----
    per_trip = df[df["unique_id"].isin(latest["unique_id"])]
    per_trip = per_trip.groupby("unique_id")["timestamp"].agg(["min", "max"])
    time_min = round((per_trip["max"] - per_trip["min"]).dt.total_seconds().sum() / 60.0, 2)

    # ---- averages ----
    valid_rows = df[df["unique_id"].isin(latest["unique_id"])]
    agg = valid_rows.agg({
        "safe_score": "mean",
        "phone_score": "mean"
    }).to_dict()

    summary = {
        "safety_score": round(agg["safe_score"], 2) if not pd.isna(agg["safe_score"]) else 0.0,
        "trips": int(trips),
        "mileage_km": round(mileage, 2),
        "time_driven_minutes": time_min,
        "average_speed_kmh": avg_spd,
        "max_speed_kmh": max_spd,
        "phone_usage_percentage": round(agg["phone_score"], 2) if not pd.isna(agg["phone_score"]) else 0.0,
    }

    return jsonify(summary)
# ---------- /top_drivers ----------
def fetch_top_drivers(limit: int = 3):
    """
    Returns top safe and aggressive drivers (avg score basis).
    """
    df = get_trip_level_data()
    if df.empty:
        return {"safe_drivers": [], "aggressive_drivers": []}

    # Ensure 1 row per trip (unique_id)
    trip_level = df.groupby(["unique_id", "device_id", "name"]).agg(
        score=("safe_score", "max"),
        distance=("trip_distance_used", "max")
    ).reset_index()

    # Aggregate at driver level
    driver_stats = trip_level.groupby(["device_id", "name"]).agg(
        avg_score=("score", "mean"),
        total_distance=("distance", "sum")
    ).reset_index()

    # Top safe (highest avg_score)
    safe_drivers = (
        driver_stats.sort_values("avg_score", ascending=False)
        .head(limit)
        .to_dict(orient="records")
    )

    # Top aggressive (lowest avg_score)
    aggressive_drivers = (
        driver_stats.sort_values("avg_score", ascending=True)
        .head(limit)
        .to_dict(orient="records")
    )
    return {"safe_drivers": safe_drivers, "aggressive_drivers": aggressive_drivers}

# ==========================
#        BADGES LOGIC
# ==========================
def assign_badges(agg, trips: int):
    badges = []

    avg_star = int(agg.get("star_rating") or 0)
    avg_speed_score = float(agg.get("spd_score") or 0.0)

    # ⭐ Star performer (excellent rating)
    if avg_star >= 5:
        badges.append("Star performer ⭐")

    # 🏆 Top driver candidate (very good rating)
    if avg_star >= 4:
        badges.append("Top driver candidate 🏆")

    # 📈 Consistency streak (good drivers with 5+ trips)
    if avg_star >= 4 and trips >= 30:
        badges.append(f"Consistency streak ({trips} trips) 📈")

    # ⚠️ Overspeed analysis (on scale 1–10, higher means more overspeeding)
    if avg_speed_score > 4.5:
        badges.append("Overspeeding frequently⚠️")
    elif avg_speed_score > 3:
        badges.append("Overspeeding Occasionally🚦")
    elif avg_speed_score > 2:
        badges.append("Usually drives within limits 🚘")
    else:
        badges.append("Maintains safe speed ✅")

    return badges

def assign_badges_api():
    user_id = request.args.get("user_id", type=int)
    filter_val = request.args.get("filter", "last_1_month")
    
    try:
        agg, trips, user_name = get_badge_aggregates(user_id=user_id, filter_val=filter_val)
    except ValueError as e:
        if str(e) == "user_not_found":
            return jsonify({"error": "User not found", "user_id": user_id}), 404
        else:
            raise

    badges = assign_badges(agg, trips)

    return jsonify({
        "filter": filter_val,
        "user_id": user_id,
        "user_name": user_name,
        "agg": agg,
        "trips": trips,
        "badges": badges
    })
