import pandas as pd
from flask import request, jsonify
#from src.app.db_queries import load_main_table_cached as load_df
from src.app.db_queries import load_df
from src.app.utils.helpers import get_time_range, normalize_timestamp
from src.app.db_queries import get_safety_graph_data

# ---------- /summary_graph (POST) ----------

def summary_graph():
    params = request.json or {}
    metric = params.get("metric")
    filter_val = params.get("filter_val")

    metric_map = {
        "Safety score": "safe_score", 
        "Acceleration": "acc_score",
        "Braking": "dec_score", 
        "Cornering": "cor_score",
        "Speeding": "spd_score", 
        "Phone usage": "phone_score",
        "Registered assets": "device_id", 
        "Active assets": "device_id",
        "Trips": "unique_id", 
        "Driving time": "timestamp",
    }
    if metric not in metric_map:
        return jsonify({"error": f"Unsupported metric: {metric}"}), 400

    col = metric_map[metric]

    # 🟢 Handle special case: Driving time → only timestamp needed
    if metric == "Driving time":
        df = load_df(["timestamp"])
    else:
        df = load_df(["timestamp", col] if col != "timestamp" else ["timestamp"])

    if df.empty:
        return jsonify({"metric": metric, "labels": [], "data": []})

    now, start_date = df["timestamp"].max(), get_time_range(filter_val, df["timestamp"].max())
    if not start_date:
        return jsonify({"error": f"Unsupported filter: {filter_val}"}), 400

    df = df[df["timestamp"] >= start_date]
    if df.empty:
        return jsonify({"metric": metric, "labels": [], "data": []})

    # Special cases
    if metric == "Trips":
        grp = df.groupby(df["timestamp"].dt.date)["unique_id"].nunique()
    elif metric == "Driving time":
        grp = df.groupby(df["timestamp"].dt.date).apply(
            lambda g: (g["timestamp"].max() - g["timestamp"].min()).total_seconds() / 60
        )
    elif metric in ["Registered assets", "Active assets"]:
        return jsonify({
            "metric": metric,
            "labels": [metric],
            "data": [df["device_id"].nunique()]
        })
    else:
        grp = df.groupby(df["timestamp"].dt.date)[col].mean().round(2)

    return jsonify({
        "metric": metric,
        "labels": grp.index.astype(str).tolist(),
        "data": grp.tolist()
    })

"""def summary_graph():
    try:
        params = request.json or {}
        metric = params.get("metric")
        filter_val = params.get("filter_val")  # e.g., "last_1_week"

        if not metric:
            return jsonify({"error": "Metric is required"}), 400

        # Load required cols
        cols = ["timestamp", metric]
        df = load_df(required_cols=cols)

        if df is None or df.empty:
            return jsonify({"error": "No data found"}), 404

        df = normalize_timestamp(df)
        if df.empty:
            return jsonify({"error": "No valid timestamps"}), 404

        # ✅ special handling for driving_time
        if metric.lower() in ["driving_time", "Driving Time"]:
            # Convert timedelta or string to minutes
            df[metric] = pd.to_timedelta(df[metric], errors="coerce").dt.total_seconds() / 60.0

        # Group by date
        df["date"] = df["timestamp"].dt.date
        grouped = df.groupby("date")[metric].sum().reset_index()   # sum makes sense for time

        result = {
            "data": [float(x) if pd.notna(x) else 0 for x in grouped[metric]],
            "labels": [str(d) for d in grouped["date"]],
            "metric": metric
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500"""


# ---------- /driver_distribution (POST) ----------
def driver_distribution():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    bins = [0, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    labels = ["<45.0","45-50","50-55","55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100"]

    # ✅ Load only required columns
    df = load_df(["timestamp", "safe_score", "device_id"])
    if df.empty or not {"timestamp","safe_score","device_id"} <= set(df.columns):
        return jsonify({"labels": labels, "data": [0]*len(labels)})

    now = df["timestamp"].max()
    start_date = get_time_range(filter_val, now)
    if start_date is None:
        return jsonify({"error": f"Unsupported filter: {filter_val}"}), 400

    df = df[(df["timestamp"] >= start_date) & (df["safe_score"].notna())]
    if df.empty:
        return jsonify({"labels": labels, "data": [0]*len(labels)})

    latest = (
        df.sort_values("timestamp")
          .groupby("device_id", observed=True)
          .tail(1)
    )

    distribution = (
        pd.cut(latest["safe_score"], bins=bins, labels=labels, right=False)
          .value_counts()
          .reindex(labels, fill_value=0)
    )

    return jsonify({"labels": labels, "data": distribution.tolist()})


# ---------- /safety_params (POST) ----------
def safety_params():
    params = request.json or {}
    filter_val = params.get("filter_val")

    df = load_df()
    now = df["timestamp"].max()
    start_date = get_time_range(filter_val, now)
    if start_date is None:
        return jsonify({"error": f"Unsupported filter: {filter_val}"})

    filtered_df = df[df["timestamp"] >= start_date]
    if filtered_df.empty:
        return jsonify({"labels": [], "data": []})

    for col in ["acc_score","dec_score","cor_score","spd_score","phone_score"]:
        if col not in filtered_df.columns:
            filtered_df[col] = pd.NA

    avg_params = {
        "Acceleration": round(filtered_df["acc_score"].mean(), 2),
        "Braking":      round(filtered_df["dec_score"].mean(), 2),
        "Cornering":    round(filtered_df["cor_score"].mean(), 2),
        "Speeding":     round(filtered_df["spd_score"].mean(), 2),
        "Phone usage":  round(filtered_df["phone_score"].mean(), 2)
    }
    return jsonify({"labels": list(avg_params.keys()), "data": list(avg_params.values())})

# ---------- /safety_graph_trend (POST) ----------
def safety_graph_trend():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")
    metric = params.get("metric", "safe_score")

    df = get_safety_graph_data()
    if df.empty:
        return jsonify({"labels": [], "data": []})

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
# ---------- /mileage_daily (POST) ----------
def mileage_daily():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    df = load_df()
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

# ---------- /driving_time_daily (POST) ----------
def driving_time_daily():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    df = load_df()
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df["timestamp"] >= start]
    if df.empty:
        return jsonify({"labels": [], "data": []})

    trip_df = df.drop_duplicates("unique_id")
    trip_times = df.groupby("unique_id")["timestamp"].agg(["min", "max"])
    trip_times["drive_time_min"] = (trip_times["max"] - trip_times["min"]).dt.total_seconds() / 60.0
    trip_times = trip_times.reset_index()

    trip_df = trip_df.merge(trip_times[["unique_id", "drive_time_min"]], on="unique_id", how="left")
    trip_df["date"] = trip_df["timestamp"].dt.date

    daily_time = trip_df.groupby("date")["drive_time_min"].sum().reset_index().dropna()
    return jsonify({
        "labels": daily_time["date"].astype(str).tolist(),
        "data": daily_time["drive_time_min"].round(2).tolist()
    })
