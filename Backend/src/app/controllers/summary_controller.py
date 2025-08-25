import pandas as pd
from flask import request, jsonify
from src.app.db_queries import (
    load_main_table, load_main_table_cached,
    get_safe_driving_rows, get_eco_driving_rows, get_devices_table, get_performance_data, load_df
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
"""def eco_driving_summary():
    filter_val = request.args.get("filter")
    df = get_eco_driving_rows()
    if df.empty:
        return jsonify({"error": "No data"}), 404

    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    filt = df[df["timestamp"] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404

    latest = (
        filt.sort_values(by=["unique_id", "timestamp"])
            .drop_duplicates("unique_id", keep="last")
    )
    valid = latest[
        (latest["eco_score"]  > 0) |
        (latest["brake_score"]> 0) |
        (latest["tire_score"] > 0) |
        (latest["fuel_score"] > 0)
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
    return jsonify(summary)"""

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
"""def safety_dashboard_summary():
    from ..db_queries import load_main_table  # local import to avoid circulars
    filter_val = request.args.get("filter")

    # Base and scored frames from main table
    base_df = load_main_table()[["timestamp", "device_id", "unique_id", "trip_distance_used"]].copy()
    scored_df = load_main_table()[[
        "unique_id","device_id","trip_distance_used","speed_kmh",
        "acc_score","dec_score","cor_score","spd_score","phone_score","safe_score","timestamp"
    ]].copy().dropna(subset=["safe_score"])

    if base_df.empty or scored_df.empty:
        return jsonify({"error": "No data"}), 404

    now = pd.to_datetime(scored_df["timestamp"]).max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    # Filter by time
    base_df["timestamp"] = pd.to_datetime(base_df["timestamp"], errors="coerce")
    scored_df["timestamp"] = pd.to_datetime(scored_df["timestamp"], errors="coerce")
    base_df = base_df.dropna(subset=["timestamp"])
    scored_df = scored_df.dropna(subset=["timestamp"])

    filt = scored_df[scored_df["timestamp"] >= start]
    if filt.empty:
        return jsonify({"error": "No data"}), 404

    latest = (
        filt.sort_values(by=["unique_id", "timestamp"])
            .drop_duplicates("unique_id", keep="last")
    )

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
        per_trip = time_df.groupby("unique_id")["timestamp"].agg(["min", "max"])
        time_min = round((per_trip["max"] - per_trip["min"]).dt.total_seconds().sum() / 60.0, 2)

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
    return jsonify(summary)"""

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

def performance_summary():
    filter_val = request.args.get("filter", "last_1_month")

    # Load datasets
    df = get_performance_data()
    devices = get_devices_table()

    if df.empty:
        return jsonify({"error": "No data"}), 404

    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if start is None:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df["timestamp"] >= start]
    if df.empty:
        return jsonify({"error": "No data"}), 404

    # Latest record per device
    latest = (
        df.sort_values("timestamp")
          .groupby("device_id", observed=True)
          .tail(1)
    )

    # Metrics
    summary = {
        "safety_score": round(latest["safe_score"].mean(), 2),
        "acceleration": round(latest["acc_score"].mean(), 2),
        "braking": round(latest["dec_score"].mean(), 2),
        "cornering": round(latest["cor_score"].mean(), 2),
        "speeding": round(latest["spd_score"].mean(), 2),
        "phone_usage": round(latest["phone_score"].mean(), 2),
        "registered_assets": int(devices["device_id"].nunique()),
        "active_assets": int(latest["device_id"].nunique()),
        "trips": int(df["unique_id"].nunique()),
        "driving_time_minutes": round((df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 60.0, 2)
    }
    return jsonify(summary)