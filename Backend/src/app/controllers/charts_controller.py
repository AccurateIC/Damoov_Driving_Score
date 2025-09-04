import pandas as pd
from flask import request, jsonify
#from src.app.db_queries import load_main_table_cached as load_df
from src.app.db_queries import load_df
from src.app.utils.helpers import get_time_range, normalize_timestamp
from src.app.db_queries import get_safety_graph_data, get_mileage_graph_data, get_engine

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
    df = load_df(["timestamp", col] if metric not in ["Driving time"] else ["timestamp", "device_id"])
    if df.empty:
        return jsonify({"metric": metric, "labels": [], "data": []})

    # filter by date range
    start_date = get_time_range(filter_val, df["timestamp"].max())
    if not start_date:
        return jsonify({"error": f"Unsupported filter: {filter_val}"}), 400
    df = df[df["timestamp"] >= start_date].dropna()
    if df.empty:
        return jsonify({"metric": metric, "labels": [], "data": []})

    # metrics
    if metric == "Trips":
        grp = df.groupby(df["timestamp"].dt.date)["unique_id"].nunique()
    elif metric == "Driving time":
        df = df.sort_values(["device_id", "timestamp"])
        df["delta"] = df.groupby("device_id")["timestamp"].diff().dt.total_seconds().div(60)
        df["driving_minutes"] = df["delta"].where((df["delta"] > 0) & (df["delta"] <= 5), 0)
        grp = df.groupby(df["timestamp"].dt.date)["driving_minutes"].sum().round(2)


    elif metric in ["Registered assets", "Active assets"]:
        return jsonify({"metric": metric, "labels": [metric], "data": [df["device_id"].nunique()]})
    else:
        grp = df.groupby(df["timestamp"].dt.date)[col].mean().round(2)

    return jsonify({"metric": metric, "labels": grp.index.astype(str).tolist(), "data": grp.fillna(0).tolist()})
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

    # ✅ only fetch required columns
    cols = ["timestamp","acc_score","dec_score","cor_score","spd_score","phone_score"]
    df = load_df(cols)
    if df.empty:
        return jsonify({"labels": [], "data": []})

    # ✅ filter quickly
    now = df["timestamp"].max()
    start_date = get_time_range(filter_val, now)
    if not start_date:
        return jsonify({"error": f"Unsupported filter: {filter_val}"})

    df = df[df["timestamp"] >= start_date]

    # ✅ vectorized, dropna automatically
    avg_params = df[cols[1:]].mean(skipna=True).round(2).to_dict()

    # rename keys to match your labels
    rename_map = {
        "acc_score": "Acceleration",
        "dec_score": "Braking",
        "cor_score": "Cornering",
        "spd_score": "Speeding",
        "phone_score": "Phone usage"
    }
    avg_params = {rename_map[k]: v for k, v in avg_params.items()}

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

    #engine = get_engine()
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if start is None:
        return jsonify({"error": f"Unsupported filter: {filter_val}"}), 400

    df = get_mileage_graph_data(start)
    if df.empty:
        return jsonify({"labels": [], "data": []})

    df["date"] = df["timestamp"].dt.date
    daily_mileage = df.groupby("date")["trip_distance_used"].sum().reset_index().dropna()

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


def driving_trips_daily():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    df = load_df(["unique_id", "timestamp"])
    if df.empty:
        return jsonify({"labels": [], "data": []})

    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df["timestamp"] >= start]
    if df.empty:
        return jsonify({"labels": [], "data": []})

    trip_df = df.drop_duplicates("unique_id")
    trip_df["date"] = trip_df["timestamp"].dt.date

    daily_trips = trip_df.groupby("date")["unique_id"].nunique().reset_index()

    return jsonify({
        "labels": daily_trips["date"].astype(str).tolist(),
        "data": daily_trips["unique_id"].tolist()
    })


def overall_analytics_summary():

    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_month")

    # ✅ only load required columns
    cols = [
        "unique_id", "device_id", "trip_distance_used", "speed_kmh",
        "acc_score", "dec_score", "cor_score", "spd_score", "phone_score",
        "safe_score", "timestamp"
    ]
    df = load_df(required_cols=cols)

    if df.empty or df["timestamp"].isna().all():
        return jsonify({"error": "No data"}), 404

    # ✅ filter quickly
    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df["timestamp"] >= start]
    if df.empty:
        return jsonify({"error": "No data"}), 404

    # ✅ latest per trip
    idx = df.groupby("unique_id")["timestamp"].idxmax()
    latest = df.loc[idx]

    # ✅ speed stats
    speed_group = df.groupby("unique_id")["speed_kmh"]
    max_spd = speed_group.max().clip(upper=300).max()
    avg_spd = speed_group.mean().mean()

    # ✅ time driven
    per_trip = df.groupby("unique_id")["timestamp"].agg(["min", "max"])
    time_min = (per_trip["max"] - per_trip["min"]).dt.total_seconds().sum() / 60.0

    # ✅ aggregate scores
    agg = latest.agg({
        "safe_score": "mean",
        "phone_score": "mean",
        "spd_score": "mean",
        "acc_score": "mean",
        "dec_score": "mean",
        "cor_score": "mean",
        "trip_distance_used": "sum"
    }).to_dict()

    params = {
        "Phone usage": round(agg["phone_score"], 2),
        "Acceleration": round(agg["acc_score"], 2),
        "Brakes": round(agg["dec_score"], 2),
        "Cornering": round(agg["cor_score"], 2),
        "Speeding": round(agg["spd_score"], 2),
    }

    overall_scoring = round(agg["safe_score"], 2)

    stats = {
        "average_speed": round(avg_spd, 2),
        "max_speed": round(max_spd, 2) if pd.notna(max_spd) else 0.0,
        "time_minutes": round(time_min, 2),
        "mileage_km": round(agg["trip_distance_used"], 2)
    }

    labels = list(params.keys())
    data = list(params.values())

    return jsonify({
        "overall_scoring": overall_scoring,
        "params": params,
        "stats": stats,
        "labels": labels,
        "data": data
    })

def speeding_analysis():
    params = request.json or {}
    filter_val = params.get("filter_val", "last_1_day")
    SPEED_LIMIT = 40  # fixed

    # ✅ only fetch required columns
    df = load_df(["unique_id", "timestamp", "speed_kmh"])
    if df.empty:
        return jsonify({"labels": [], "speeds": [], "colors": []})

    now = df["timestamp"].max()
    start = get_time_range(filter_val, now)
    if not start:
        return jsonify({"error": "Invalid filter"}), 400

    df = df[df["timestamp"] >= start]

    # Resample into 30-minute bins
    df = df.set_index("timestamp")
    bins = df["speed_kmh"].resample("1H").mean().dropna().reset_index()

    bins = bins[bins["speed_kmh"] > 5]   # keep speeds > 5 km/h

    bins["time"] = bins["timestamp"].dt.strftime("%H:%M")
    bins["color"] = bins["speed_kmh"].apply(lambda x: "red" if x > SPEED_LIMIT else "green")

    return jsonify({
        "labels": bins["time"].tolist(),
        "speeds": bins["speed_kmh"].round(2).tolist(),
        "colors": bins["color"].tolist()
    })
