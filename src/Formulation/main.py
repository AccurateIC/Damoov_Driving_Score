
import yaml
import pandas as pd
import sqlite3
from scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector,
    assign_coefficient
)
from utils import load_config

# === Load config ===
config = load_config()
db_path = "csv/raxel_traker_db_200325 (1).db"

# === Step 1: Load CSVs and save to database if needed ===
conn = sqlite3.connect(db_path)

csv_files = {
    "trip_distances_output": config["files"]["trip_distances_output"],
    "main_data": config["files"]["main_data"],
    "sample_data": config["files"]["sample_data"],
    "events_start": config["files"]["events_start"],
    "events_stop": config["files"]["events_stop"]
}

for table_name, csv_path in csv_files.items():
    print(f"➡ Loading {csv_path} to table '{table_name}' (if not exists)...")
    # Check if table exists
    table_check_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    if not pd.read_sql_query(table_check_query, conn).empty:
        print(f"✅ Table '{table_name}' already exists. Skipping CSV import.")
        continue

    # Read CSV and save to DB
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"✅ Table '{table_name}' created from {csv_path}")

# === Step 2: Read data from database tables ===
print("\n🔍 Reading data from database tables...")
distance_df = pd.read_sql_query("SELECT * FROM trip_distances_output", conn)
trip_distance_dict = dict(zip(distance_df['UNIQUE_ID'], distance_df['distance_km']))

df = pd.read_sql_query("SELECT * FROM main_data", conn)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

conn.close()

# === Step 3: Calculate trip scores ===
weights = config["weights"]
trip_scores = []

for uid in df['unique_id'].unique():
    trip_distance = trip_distance_dict.get(uid, 50.0)
    if trip_distance <= 1.0:
        continue

    trip_df = df[df['unique_id'] == uid].copy()

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

# === Step 4: Output results ===
score_df = pd.DataFrame(trip_scores)
print(score_df)