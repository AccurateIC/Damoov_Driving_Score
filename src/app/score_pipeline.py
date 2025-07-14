"""
import pandas as pd
import sqlite3
from math import radians, sin, cos, acos
from pathlib import Path
import yaml

from Formulation.scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector
)

def load_config():
    base_dir = Path(__file__).resolve().parent
    with open(base_dir / "config.yaml", "r") as f:
        return yaml.safe_load(f)

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

    main_df = pd.read_sql_query("SELECT * FROM SampleTable", conn)
    start_df = pd.read_sql_query("SELECT * FROM EventsStartPointTable", conn)
    stop_df = pd.read_sql_query("SELECT * FROM EventsStopPointTable", conn)
    main_df['timestamp'] = pd.to_datetime(main_df['timestamp'])

    trip_distances_df = calculate_trip_distances(start_df, stop_df)
    trip_distance_dict = dict(zip(trip_distances_df['UNIQUE_ID'], trip_distances_df['distance_km']))

    weights = config['weights']
    trip_scores = []

    for uid in main_df['unique_id'].unique():
        trip_distance = trip_distance_dict.get(uid, 50.0)
        if trip_distance <= 1.0:
            continue

        trip_df = main_df[main_df['unique_id'] == uid].copy()

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

    # Drop old scoring columns if they exist
    main_df = main_df.drop(
        columns=['safe_score', 'risk_factor', 'total_penalty', 'star_rating'],
        errors='ignore'
    )

    # Merge with new scores
    updated_df = pd.merge(main_df, score_df, on='unique_id', how='left')

    # Replace full table with updated data
    updated_df.to_sql("SampleTable", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ SQLite SampleTable updated with new scores (all trips).")
"""
import pandas as pd
import sqlite3
from math import radians, sin, cos, acos
from pathlib import Path
import yaml
from eco_score_calculator import EcoScoreCalculator 

from Formulation.scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector
)

 # Importing your EcoScoreCalculator
# Load config
def load_config():
    base_dir = Path(__file__).resolve().parent
    with open(base_dir / "config.yaml", "r") as f:
        return yaml.safe_load(f)

# Calculate spherical distance (Haversine)
def spherical_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return R * acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2 - lon1))

# Calculate distances for each trip
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

# Main Scoring Pipeline
def run_score_pipeline(db_path, config):
    conn = sqlite3.connect(db_path)

    #main_df = pd.read_sql_query("SELECT * FROM SampleTable", conn)
    main_df = pd.read_sql_query("SELECT unique_id, tick_timestamp, timestamp, speed_kmh, acceleration, deceleration, acceleration_y_original, screen_on, screen_blocked FROM SampleTable", conn)

    start_df = pd.read_sql_query("SELECT * FROM EventsStartPointTable", conn)
    stop_df = pd.read_sql_query("SELECT * FROM EventsStopPointTable", conn)
    main_df = main_df.dropna(subset=['timestamp'])
    main_df['timestamp'] = pd.to_datetime(main_df['tick_timestamp'], unit='s', errors='coerce')
   

    trip_distances_df = calculate_trip_distances(start_df, stop_df)
    trip_distance_dict = dict(zip(trip_distances_df['UNIQUE_ID'], trip_distances_df['distance_km']))

    weights = config['weights']
    trip_scores = []

    for uid in main_df['unique_id'].unique():
        trip_distance = trip_distance_dict.get(uid, 50.0)
        trip_df = main_df[main_df['unique_id'] == uid].copy()

        trip_df = trip_df[(trip_df['speed_kmh'] >= 1.0) & (trip_df['speed_kmh'] <= 160.0)]

        if len(trip_df) < 10 or trip_distance <= 1.0:
            continue

        # Score: Acceleration
        acc = DamoovAccelerationScorer(**config['acceleration'])
        acc.df = trip_df
        acc.detect_events()
        acc.calculate_penalties()
        acc_score = acc.get_events()['penalty_acc'].sum() if not acc.get_events().empty else 0

        # Score: Braking
        dec = DamoovDeccelerationScorer(**config['deceleration'])
        dec.df = trip_df
        dec.detect_events()
        dec.calculate_penalties()
        dec_score = dec.get_events()['penalty_braking'].sum() if not dec.get_events().empty else 0

        # Score: Cornering
        cor = DamoovCorneringScorer(**config['cornering'])
        cor.df = trip_df
        cor.detect_events()
        cor.calculate_penalties()
        cor_score = cor.get_events()['penalty_cornering'].sum() if not cor.get_events().empty else 0

        # Score: Speeding
        spd = SpeedingDetectorFixedLimit(**config['speeding'])
        spd.df = trip_df
        spd.detect_speeding()
        spd.assign_penalties()
        spd_score = spd.get_events()['penalty_speeding'].sum() if not spd.get_events().empty else 0

        # Score: Phone Usage
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

        penalty_per_km = total_penalty / trip_distance
        
        event_thresholds = config.get("event_thresholds")
        score_weights = config.get("score_weights")
        # ⚡ ECO Score
        eco = EcoScoreCalculator(trip_df, unique_id=uid, external_trip_distances=trip_distance_dict, thresholds=event_thresholds, score_weights=score_weights)
        eco_results = eco.calculate_scores()

        trip_scores.append({
            'unique_id': uid,
            'penalty_per_km': penalty_per_km,
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
        conn.close()
        return

    # Normalize penalty to get safe_score
    min_penalty = score_df['penalty_per_km'].min()
    max_penalty = score_df['penalty_per_km'].max()

    if max_penalty == min_penalty:
        score_df['safe_score'] = 100.0
    else:
        score_df['safe_score'] = 100 * (1 - (score_df['penalty_per_km'] - min_penalty) / (max_penalty - min_penalty))
        score_df['safe_score'] = score_df['safe_score'].round(2)

    score_df['risk_factor'] = score_df['penalty_per_km'].round(4)
    score_df['total_penalty'] = score_df['penalty_per_km'].round(4)
    score_df['star_rating'] = score_df['safe_score'].apply(lambda s: 5 if s >= 95 else 4 if s >= 85 else 3 if s >= 75 else 2 if s >= 65 else 1)

    print(score_df)

    # Clean old score columns if present
    main_df = main_df.drop(columns=[
        'safe_score', 'risk_factor', 'total_penalty', 'star_rating',
        'penalty_per_km', 'eco_score', 'fuel_score', 'tire_score', 'brake_score',
        'harsh_accelerations', 'harsh_brakings', 'harsh_cornerings',
        'speed_std_dev', 'trip_distance_used'
    ], errors='ignore')

    updated_df = pd.merge(main_df, score_df, on='unique_id', how='left')
    updated_df.to_sql("SampleTable", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ SampleTable updated with both Safe Score and Eco Score.")
