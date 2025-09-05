# score_pipeline.py
import pandas as pd
from math import radians, sin, cos, acos
from pathlib import Path
import yaml
from sqlalchemy import text
from eco_score_calculator import EcoScoreCalculator

from Formulation.scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector
)

# ---------------------------
# Load config
# ---------------------------
def load_config():
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    with open(base_dir / "config.yaml", "r") as f:
        return yaml.safe_load(f)

# ---------------------------
# Spherical distance (vincenty-lite)
# ---------------------------


def spherical_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    val = sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2 - lon1)
    val = min(1.0, max(-1.0, val))  # 👈 clamp to [-1, 1]

    return R * acos(val)

def calculate_trip_distances(start_df, stop_df):
    start_df = start_df.rename(columns={'latitude': 'start_lat', 'longitude': 'start_lon'})
    stop_df  = stop_df.rename(columns={'latitude': 'end_lat',   'longitude': 'end_lon'})

    start_min = start_df.groupby("UNIQUE_ID")["ID"].idxmin()
    stop_max  = stop_df.groupby("UNIQUE_ID")["ID"].idxmax()

    start_points = start_df.loc[start_min].copy()
    end_points   = stop_df.loc[stop_max].copy()

    merged = pd.merge(start_points, end_points[['UNIQUE_ID', 'end_lat', 'end_lon']], on='UNIQUE_ID')
    merged["distance_km"] = merged.apply(
        lambda row: spherical_distance(row["start_lat"], row["start_lon"], row["end_lat"], row["end_lon"]), axis=1
    )
    return merged[["UNIQUE_ID", "distance_km"]]

# ---------------------------
# Main pipeline (engine-aware)
# ---------------------------
def run_score_pipeline(engine, config):
    db       = config['database']
    dialect  = engine.url.get_backend_name()  # "mysql" or "sqlite"
    main_tbl = db['main_table']
    start_tbl= db['start_table']
    stop_tbl = db['stop_table']

    # Read only needed columns from main table
    main_cols = "unique_id, device_id, tick_timestamp, timestamp, speed_kmh, acceleration, deceleration, acceleration_y_original, screen_on, screen_blocked"
    main_df = pd.read_sql_query(f"SELECT {main_cols} FROM {main_tbl}", engine)
    start_df = pd.read_sql_query(f"SELECT * FROM {start_tbl}", engine)
    stop_df  = pd.read_sql_query(f"SELECT * FROM {stop_tbl}", engine)

    # Clean + timestamps
    if 'timestamp' in main_df.columns:
        main_dffrop = main_df.dropna(subset=['timestamp'])
    # Recompute from tick epoch if available
    if 'tick_timestamp' in main_df.columns:
        main_df['timestamp'] = pd.to_datetime(main_df['tick_timestamp'], unit = 's', errors='coerce')

    trip_distances_df = calculate_trip_distances(start_df, stop_df)
    trip_distance_dict = dict(zip(trip_distances_df['UNIQUE_ID'], trip_distances_df['distance_km']))

    weights = config['weights']
    trip_scores = []

    for uid in main_df['unique_id'].dropna().unique():
        trip_distance = trip_distance_dict.get(uid, 50.0)
        trip_df = main_df[main_df['unique_id'] == uid].copy()

        # reasonable speed filter
        trip_df = trip_df[(trip_df['speed_kmh'] >= 1.0) & (trip_df['speed_kmh'] <= 160.0)]

        if len(trip_df) < 10 or trip_distance <= 1.0:
            continue

        # Acceleration
        acc = DamoovAccelerationScorer(**config['acceleration']); acc.df = trip_df
        acc.detect_events(); acc.calculate_penalties()
        acc_score = acc.get_events()['penalty_acc'].sum() if not acc.get_events().empty else 0

        # Braking
        dec = DamoovDeccelerationScorer(**config['deceleration']); dec.df = trip_df
        dec.detect_events(); dec.calculate_penalties()
        dec_score = dec.get_events()['penalty_braking'].sum() if not dec.get_events().empty else 0

        # Cornering
        cor = DamoovCorneringScorer(**config['cornering']); cor.df = trip_df
        cor.detect_events(); cor.calculate_penalties()
        cor_score = cor.get_events()['penalty_cornering'].sum() if not cor.get_events().empty else 0

        # Speeding
        spd = SpeedingDetectorFixedLimit(**config['speeding']); spd.df = trip_df
        spd.detect_speeding(); spd.assign_penalties()
        spd_score = spd.get_events()['penalty_speeding'].sum() if not spd.get_events().empty else 0

        # Phone usage
        phone = PhoneUsageDetector(**config['phone_usage']); phone.df = trip_df
        phone.detect_phone_usage(); phone.assign_penalties()
        phone_score = phone.get_events()['penalty_phone'].sum() if not phone.get_events().empty else 0

        total_penalty = (
            weights["acceleration_weight"] * acc_score +
            weights["braking_weight"]      * dec_score +
            weights["cornering_weight"]    * cor_score +
            weights["speeding_weight"]     * spd_score +
            weights["phone_usage_weight"]  * phone_score
        )

        penalty_per_km = total_penalty / trip_distance

        # Eco score
        event_thresholds = config.get("event_thresholds")
        score_weights    = config.get("score_weights")
        eco = EcoScoreCalculator(trip_df, unique_id=uid,
                                 external_trip_distances=trip_distance_dict,
                                 thresholds=event_thresholds, score_weights=score_weights)
        eco_results = eco.calculate_scores()

        trip_scores.append({
            'unique_id': uid,
            'penalty_per_km': round(penalty_per_km, 2),
            'acc_score': round(acc_score, 2),
            'dec_score': round(dec_score, 2),
            'cor_score': round(cor_score, 2),
            'spd_score': round(spd_score, 2),
            'phone_score': round(phone_score, 2),
            'fuel_score': eco_results['fuel_score'],
            'tire_score': eco_results['tire_score'],
            'brake_score': eco_results['brake_score'],
            'eco_score': eco_results['eco_score'],
            'harsh_accelerations': eco_results['harsh_accelerations'],
            'harsh_brakings': eco_results['harsh_brakings'],
            'harsh_cornerings': eco_results['harsh_cornerings'],
            'speed_std_dev': eco_results['speed_std_dev'],
            'trip_distance_used': eco_results['trip_distance_used']
        })

    score_df = pd.DataFrame(trip_scores)
    if score_df.empty:
        print("No valid trips to process after filtering. Exiting pipeline.")
        return

    # Normalize to safe_score
    min_penalty = score_df['penalty_per_km'].min()
    max_penalty = score_df['penalty_per_km'].max()
    if max_penalty == min_penalty:
        score_df['safe_score'] = 100.0
    else:
        score_df['safe_score'] = 100 * (1 - (score_df['penalty_per_km'] - min_penalty) / (max_penalty - min_penalty))
        score_df['safe_score'] = score_df['safe_score'].round(2)

    score_df['risk_factor']  = score_df['penalty_per_km'].round(4)
    score_df['total_penalty']= score_df['penalty_per_km'].round(4)
    score_df['star_rating']  = score_df['safe_score'].apply(lambda s: 5 if s >= 95 else 4 if s >= 85 else 3 if s >= 75 else 2 if s >= 65 else 1)

    # ---------------------------
    # WRITE BACK: safe, schema-preserving approach
    # ---------------------------
    # create temp table with updates
    tmp_table = "_tmp_score_updates"
    score_df.to_sql(tmp_table, engine, if_exists="replace", index=False, method='multi', chunksize=5000)

    # Ensure columns exist in main table (MySQL only; SQLite adds on the fly in UPDATE)
    scoring_cols_mysql = {
        "penalty_per_km": "FLOAT",
        "acc_score": "FLOAT", "dec_score": "FLOAT", "cor_score": "FLOAT",
        "spd_score": "FLOAT", "phone_score": "FLOAT",
        "fuel_score": "FLOAT", "tire_score": "FLOAT", "brake_score": "FLOAT", "eco_score": "FLOAT",
        "harsh_accelerations": "INT", "harsh_brakings": "INT", "harsh_cornerings": "INT",
        "speed_std_dev": "FLOAT", "trip_distance_used": "FLOAT",
        "safe_score": "FLOAT", "risk_factor": "FLOAT", "total_penalty": "FLOAT",
        "star_rating": "INT"
    }

    with engine.begin() as conn:
      if dialect == "mysql":
        # 1️⃣ Get existing columns in the table
        existing_cols = {
            row[0] for row in conn.exec_driver_sql(f"SHOW COLUMNS FROM {main_tbl}")
        }

        # 2️⃣ Add missing columns safely
        for col, typ in scoring_cols_mysql.items():
            if col not in existing_cols:
                try:
                    conn.exec_driver_sql(
                        f"ALTER TABLE {main_tbl} ADD COLUMN {col} {typ} NULL"
                    )
                    print(f"✅ Added column {col}")
                except Exception as e:
                    print(f"⚠️ Could not add column {col}: {e}")

        # 3️⃣ Perform the update from tmp_table
        set_clause = ", ".join(
            [f"{main_tbl}.{c} = {tmp_table}.{c}" for c in scoring_cols_mysql.keys()]
        )
        conn.exec_driver_sql(f"""
            UPDATE {main_tbl}
            JOIN {tmp_table} ON {main_tbl}.unique_id = {tmp_table}.unique_id
            SET {set_clause}
        """)

        conn.exec_driver_sql(f"DROP TABLE {tmp_table}")

      else:
        # SQLite: multi-column correlated update
        existing_cols = {
            r['name'] for r in conn.exec_driver_sql(f"PRAGMA table_info({main_tbl})")
        }
        for col, typ in scoring_cols_mysql.items():
            if col not in existing_cols:
                try:
                    conn.exec_driver_sql(f"ALTER TABLE {main_tbl} ADD COLUMN {col} {typ}")
                except Exception:
                    pass

        set_clause = ", ".join(
            [f"{col} = (SELECT {col} FROM {tmp_table} WHERE {tmp_table}.unique_id = {main_tbl}.unique_id)"
             for col in scoring_cols_mysql.keys()]
        )
        conn.exec_driver_sql(f"""
            UPDATE {main_tbl}
            SET {set_clause}
            WHERE unique_id IN (SELECT unique_id FROM {tmp_table})
        """)
        conn.exec_driver_sql(f"DROP TABLE {tmp_table}")


    print(f"✅ {main_tbl} updated with Safe Score and Eco Score.")
