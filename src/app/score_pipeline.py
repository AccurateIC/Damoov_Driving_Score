
import pandas as pd
import sqlite3
from math import radians, sin, cos, acos
from pathlib import Path
import yaml
import mysql.connector

from Formulation.scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector
)

# Load config
def load_config():
    base_dir = Path(__file__).resolve().parent
    with open(base_dir / "config.yaml", "r") as f:
        return yaml.safe_load(f)

def get_connection(db_conf):
    if db_conf["type"] == "sqlite":
        return sqlite3.connect(db_conf["sqlite_path"])
    elif db_conf["type"] == "mysql":
        return mysql.connector.connect(
            host=db_conf["host"],
            port=db_conf["port"],
            user=db_conf["user"],
            password=db_conf["password"],
            database=db_conf["name"]
        )
    else:
        raise ValueError("Unsupported database type")

# Calculate spherical distance
def spherical_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return R * acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2 - lon1))

# Calculate trip distances
def calculate_trip_distances(start_df, stop_df):
    start_df = start_df.rename(columns={'latitude': 'start_lat', 'longitude': 'start_lon'})
    stop_df = stop_df.rename(columns={'latitude': 'end_lat', 'longitude': 'end_lon'})

    start_min = start_df.groupby("UNIQUE_ID")["ID"].idxmin()
    stop_max = stop_df.groupby("UNIQUE_ID")["ID"].idxmax()

    start_points = start_df.loc[start_min].copy()
    end_points = stop_df.loc[stop_max].copy()

    merged = pd.merge(start_points, end_points[['UNIQUE_ID', 'end_lat', 'end_lon']], on='UNIQUE_ID')
    merged["distance_km"] = merged.apply(
        lambda row: spherical_distance(row["start_lat"], row["start_lon"], row["end_lat"], row["end_lon"]), axis=1
    )
    return merged[["UNIQUE_ID", "distance_km"]]

# The main pipeline
"""def run_score_pipeline(db_conf, config):
    conn = get_connection(db_conf)

    main_df = pd.read_sql("SELECT * FROM {}".format(db_conf["main_table"]), conn)
    start_df = pd.read_sql("SELECT * FROM {}".format(db_conf["start_table"]), conn)
    stop_df = pd.read_sql("SELECT * FROM {}".format(db_conf["stop_table"]), conn)
    main_df['timestamp'] = pd.to_datetime(main_df['timestamp'])

    trip_distances_df = calculate_trip_distances(start_df, stop_df)
    trip_distance_dict = dict(zip(trip_distances_df['UNIQUE_ID'], trip_distances_df['distance_km']))

    weights = config['weights']
    trip_scores = []

    for uid in main_df['unique_id'].unique():
        trip_distance = trip_distance_dict.get(uid, 50.0)
        trip_df = main_df[main_df['unique_id'] == uid].copy()

        # Apply data cleaning
        trip_df = trip_df[(trip_df['speed_kmh'] >= 1.0) & (trip_df['speed_kmh'] <= 160.0)]

        if len(trip_df) < 10 or trip_distance <= 1.0:
            continue

        # Acceleration
        acc = DamoovAccelerationScorer(**config['acceleration'])
        acc.df = trip_df
        acc.detect_events()
        acc.calculate_penalties()
        acc_score = acc.get_events()['penalty_acc'].sum() if not acc.get_events().empty else 0

        # Deceleration
        dec = DamoovDeccelerationScorer(**config['deceleration'])
        dec.df = trip_df
        dec.detect_events()
        dec.calculate_penalties()
        dec_score = dec.get_events()['penalty_braking'].sum() if not dec.get_events().empty else 0

        # Cornering
        cor = DamoovCorneringScorer(**config['cornering'])
        cor.df = trip_df
        cor.detect_events()
        cor.calculate_penalties()
        cor_score = cor.get_events()['penalty_cornering'].sum() if not cor.get_events().empty else 0

        # Speeding
        spd = SpeedingDetectorFixedLimit(**config['speeding'])
        spd.df = trip_df
        spd.detect_speeding()
        spd.assign_penalties()
        spd_score = spd.get_events()['penalty_speeding'].sum() if not spd.get_events().empty else 0

        # Phone Usage
        phone = PhoneUsageDetector(**config['phone_usage'])
        phone.df = trip_df
        phone.detect_phone_usage()
        phone.assign_penalties()
        phone_score = phone.get_events()['penalty_phone'].sum() if not phone.get_events().empty else 0

        total_penalty = (
            weights["acceleration_weight"] * acc_score +
            weights["braking_weight"] * dec_score +
            weights["cornering_weight"] * cor_score +
            weights["speeding_weight"] * spd_score +
            weights["phone_usage_weight"] * phone_score
        )

        # Normalize penalty by trip distance
        penalty_per_km = total_penalty / trip_distance
        trip_scores.append({
            'unique_id': uid,
            'penalty_per_km': penalty_per_km
        })

    # Create dataframe for normalization step
    score_df = pd.DataFrame(trip_scores)

    # Apply Min-Max Normalization AFTER aggregation
    min_penalty = score_df['penalty_per_km'].min()
    max_penalty = score_df['penalty_per_km'].max()

    if max_penalty == min_penalty:
        score_df['safe_score'] = 100.0
    else:
        score_df['safe_score'] = 100 * (1 - (score_df['penalty_per_km'] - min_penalty) / (max_penalty - min_penalty))
        score_df['safe_score'] = score_df['safe_score'].round(2)

    score_df['risk_factor'] = score_df['penalty_per_km'].round(4)
    score_df['total_penalty'] = score_df['penalty_per_km'].round(4) * 1  # keep same for compatibility

    # Star Rating logic
    score_df['star_rating'] = score_df['safe_score'].apply(lambda s: 5 if s >= 95 else 4 if s >= 85 else 3 if s >= 75 else 2 if s >= 65 else 1)

    print(score_df)

    # Drop old scoring columns
    main_df = main_df.drop(columns=['safe_score', 'risk_factor', 'total_penalty', 'star_rating'], errors='ignore')

    updated_df = pd.merge(main_df, score_df, on='unique_id', how='left')
    updated_df.to_sql("SampleTable", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ SQLite SampleTable updated with normalized scores.")
"""

def run_score_pipeline(db_conf, config):
    conn = get_connection(db_conf)

    main_df = pd.read_sql(f"SELECT * FROM {db_conf['main_table']}", conn)
    start_df = pd.read_sql(f"SELECT * FROM {db_conf['start_table']}", conn)
    stop_df = pd.read_sql(f"SELECT * FROM {db_conf['stop_table']}", conn)
    main_df['timestamp'] = pd.to_datetime(main_df['timestamp'])

    trip_distances_df = calculate_trip_distances(start_df, stop_df)
    trip_distance_dict = dict(zip(trip_distances_df['UNIQUE_ID'], trip_distances_df['distance_km']))

    weights = config['weights']
    trip_scores = []

    for uid in main_df['unique_id'].unique():
        trip_distance = trip_distance_dict.get(uid, 50.0)
        trip_df = main_df[main_df['unique_id'] == uid].copy()

        # Apply data cleaning
        trip_df = trip_df[(trip_df['speed_kmh'] >= 1.0) & (trip_df['speed_kmh'] <= 160.0)]

        if len(trip_df) < 10 or trip_distance <= 1.0:
            continue

        # Acceleration
        acc = DamoovAccelerationScorer(**config['acceleration'])
        acc.df = trip_df
        acc.detect_events()
        acc.calculate_penalties()
        acc_score = acc.get_events()['penalty_acc'].sum() if not acc.get_events().empty else 0

        # Deceleration
        dec = DamoovDeccelerationScorer(**config['deceleration'])
        dec.df = trip_df
        dec.detect_events()
        dec.calculate_penalties()
        dec_score = dec.get_events()['penalty_braking'].sum() if not dec.get_events().empty else 0

        # Cornering
        cor = DamoovCorneringScorer(**config['cornering'])
        cor.df = trip_df
        cor.detect_events()
        cor.calculate_penalties()
        cor_score = cor.get_events()['penalty_cornering'].sum() if not cor.get_events().empty else 0

        # Speeding
        spd = SpeedingDetectorFixedLimit(**config['speeding'])
        spd.df = trip_df
        spd.detect_speeding()
        spd.assign_penalties()
        spd_score = spd.get_events()['penalty_speeding'].sum() if not spd.get_events().empty else 0

        # Phone Usage
        phone = PhoneUsageDetector(**config['phone_usage'])
        phone.df = trip_df
        phone.detect_phone_usage()
        phone.assign_penalties()
        phone_score = phone.get_events()['penalty_phone'].sum() if not phone.get_events().empty else 0

        total_penalty = (
            weights["acceleration_weight"] * acc_score +
            weights["braking_weight"] * dec_score +
            weights["cornering_weight"] * cor_score +
            weights["speeding_weight"] * spd_score +
            weights["phone_usage_weight"] * phone_score
        )

        # Normalize penalty by trip distance
        penalty_per_km = total_penalty / trip_distance
        trip_scores.append({
            'unique_id': uid,
            'penalty_per_km': penalty_per_km
        })

    # Create dataframe for normalization step
    score_df = pd.DataFrame(trip_scores)

    if score_df.empty:
        print("⚠️ No valid trips to score.")
        conn.close()
        return

    # Apply Min-Max Normalization AFTER aggregation
    min_penalty = score_df['penalty_per_km'].min()
    max_penalty = score_df['penalty_per_km'].max()

    if max_penalty == min_penalty:
        score_df['safe_score'] = 100.0
    else:
        score_df['safe_score'] = 100 * (1 - (score_df['penalty_per_km'] - min_penalty) / (max_penalty - min_penalty))
        score_df['safe_score'] = score_df['safe_score'].round(2)

    score_df['risk_factor'] = score_df['penalty_per_km'].round(4)
    score_df['total_penalty'] = score_df['penalty_per_km'].round(4)
    score_df['star_rating'] = score_df['safe_score'].apply(
        lambda s: 5 if s >= 95 else 4 if s >= 85 else 3 if s >= 75 else 2 if s >= 65 else 1
    )

    # Prepare DriftTable data
    drift_df = pd.merge(
        main_df[['unique_id', 'user_id']].drop_duplicates(),
        score_df[['unique_id', 'safe_score', 'risk_factor', 'total_penalty', 'star_rating']],
        on="unique_id",
        how="inner"
    )

    # Append new scores into DriftTable
    drift_table = "DriftTable"
    
    cursor = conn.cursor()

# Ensure table exists
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {drift_table} (
    unique_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    safe_score FLOAT,
    risk_factor FLOAT,
    total_penalty FLOAT,
    star_rating INT
    )
    """)
    conn.commit()

# Insert rows safely using ON DUPLICATE KEY UPDATE
    for _, row in drift_df.iterrows():
        cursor.execute(f"""
    INSERT INTO {drift_table} (unique_id, user_id, safe_score, risk_factor, total_penalty, star_rating)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        safe_score=VALUES(safe_score),
        risk_factor=VALUES(risk_factor),
        total_penalty=VALUES(total_penalty),
        star_rating=VALUES(star_rating)
    """, (
        row['unique_id'],
        row['user_id'],
        row['safe_score'],
        row['risk_factor'],
        row['total_penalty'],
        row['star_rating']
    ))
    conn.commit()
    conn.close()


   

    print("✅ DriftTable updated with new scores.")

