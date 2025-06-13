
import pandas as pd
import sqlite3
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

def analyze_trip(db_path, config, target_uid):
    conn = sqlite3.connect(db_path)
    main_df = pd.read_sql_query("SELECT * FROM SampleTable", conn)
    conn.close()

    # Filter for this unique_id
    trip_df = main_df[main_df['unique_id'] == target_uid].copy()
    trip_df['timestamp'] = pd.to_datetime(trip_df['timestamp'])

    print(f"\n🧪 Analysis for unique_id: {target_uid}")
    print(f"➤ Total rows: {len(trip_df)}")
    print(f"➤ Speed (km/h): min={trip_df['speed_kmh'].min():.2f}, max={trip_df['speed_kmh'].max():.2f}, mean={trip_df['speed_kmh'].mean():.2f}")
    print(f"➤ Acceleration (km/h): min={trip_df['acceleration'].min():.2f}, max={trip_df['acceleration'].max():.2f}, mean={trip_df['acceleration'].mean():.2f}")

    weights = config['weights']
    acc = DamoovAccelerationScorer(**config['acceleration'])
    acc.df = trip_df
    acc.detect_events()
    acc.calculate_penalties()
    acc_penalty = acc.df['penalty_acc'].sum()
    print(f"🚗 Acceleration Events → Penalty: {acc_penalty:.2f}")

    # Braking
    dec = DamoovDeccelerationScorer(**config['deceleration'])
    dec.df = trip_df
    dec.detect_events()
    dec.calculate_penalties()
    dec_penalty = dec.df['penalty_braking'].sum()
    print(f"🛑 Braking Events → Penalty: {dec_penalty:.2f}")

    # Cornering
    cor = DamoovCorneringScorer(**config['cornering'])
    cor.df = trip_df
    cor.detect_events()
    cor.calculate_penalties()
    cor_penalty = cor.df['penalty_cornering'].sum()
    print(f"↪️ Cornering Events → Penalty: {cor_penalty:.2f}")

    # Speeding
    spd = SpeedingDetectorFixedLimit(**config['speeding'])
    spd.df = trip_df
    spd.detect_speeding()
    spd.assign_penalties()
    spd_penalty = spd.df['penalty_speeding'].sum()
    print(f"🚓 Speeding Events → Penalty: {spd_penalty:.2f}")

    # Phone usage
    phone = PhoneUsageDetector(**config['phone_usage'])
    phone.df = trip_df
    phone.detect_phone_usage()
    phone.assign_penalties()
    phone_penalty = phone.df['penalty_phone'].sum()
    print(f"📱 Phone Usage Events → Penalty: {phone_penalty:.2f}")

    total_penalty = (
        weights["acceleration_weight"] * acc_penalty +
        weights["braking_weight"] * dec_penalty +
        weights["cornering_weight"] * cor_penalty +
        weights["speeding_weight"] * spd_penalty +
        weights["phone_usage_weight"] * phone_penalty
    )

    print(f"\n🧾 Total Weighted Penalty: {total_penalty:.4f}")
    print("✅ Analysis complete.")

if __name__ == "__main__":
    config = load_config()
    db_path = Path(__file__).resolve().parent / config['database']['sqlite_path']
    analyze_trip(str(db_path), config, target_uid=617714292)
