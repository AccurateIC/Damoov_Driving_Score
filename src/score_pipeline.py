
import pandas as pd
import sqlite3
from math import radians, sin, cos, acos
from Formulation.scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector
)

def spherical_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return R * acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2 - lon1))

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

def run_score_pipeline(db_path, config):
    conn = sqlite3.connect(db_path)

    main_df = pd.read_sql_query("SELECT * FROM Cleaned_SampleTable", conn)
    start_df = pd.read_sql_query("SELECT * FROM EventsStartPointTable", conn)
    stop_df = pd.read_sql_query("SELECT * FROM EventsStopPointTable", conn)
    main_df['timestamp'] = pd.to_datetime(main_df['timestamp'], unit='s')

    trip_distances_df = calculate_trip_distances(start_df, stop_df)
    trip_distance_dict = dict(zip(trip_distances_df['UNIQUE_ID'], trip_distances_df['distance_km']))

    conn.close()

    weights = config['weights']
    trip_scores = []

    for uid in main_df['unique_id'].unique():
        trip_distance = trip_distance_dict.get(uid, 50.0)
        if trip_distance <= 1.0:
            continue

        trip_df = main_df[main_df['unique_id'] == uid].copy()

        acc = DamoovAccelerationScorer(**config['acceleration'])
        acc.df = trip_df
        acc.detect_events()
        acc.calculate_penalties()
        acc_score = acc.get_events()['penalty_acc'].sum() if not acc.get_events().empty else 0

        dec = DamoovDeccelerationScorer(**config['deceleration'])
        dec.df = trip_df
        dec.detect_events()
        dec.calculate_penalties()
        dec_score = dec.get_events()['penalty_braking'].sum() if not dec.get_events().empty else 0

        cor = DamoovCorneringScorer(**config['cornering'])
        cor.df = trip_df
        cor.detect_events()
        cor.calculate_penalties()
        cor_score = cor.get_events()['penalty_cornering'].sum() if not cor.get_events().empty else 0

        spd = SpeedingDetectorFixedLimit(**config['speeding'])
        spd.df = trip_df
        spd.detect_speeding()
        spd.assign_penalties()
        spd_score = spd.get_events()['penalty_speeding'].sum() if not spd.get_events().empty else 0

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

        risk_factor = total_penalty / trip_distance if trip_distance > 0 else 1
        safe_score = round(100 * (1 / (1 + risk_factor)), 2)
        star = 5 if safe_score == 100 else 4 if safe_score >= 90 else 3 if safe_score >= 80 else 2 if safe_score >= 70 else 1

        trip_scores.append({
            'unique_id': uid,
            'safe_score': safe_score,
            'risk_factor': round(risk_factor, 4),
            'total_penalty': round(total_penalty, 4),
            'star_rating': star
        })

    score_df = pd.DataFrame(trip_scores)
    print(score_df)

    # === Merge scores into SampleTable and update existing rows ===
    updated_df = pd.merge(main_df, score_df, on='unique_id', how='left')

    with sqlite3.connect(db_path) as conn:
    # Overwrite SampleTable with new columns
     updated_df.to_sql("SampleTable", conn, if_exists="replace", index=False)
    print("✅ SampleTable updated with scoring results.")
