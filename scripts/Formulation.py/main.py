
import yaml
import pandas as pd
from scorers import (
    DamoovAccelerationScorer,
    DamoovDeccelerationScorer,
    DamoovCorneringScorer,
    SpeedingDetectorFixedLimit,
    PhoneUsageDetector,
    assign_coefficient
)
from utils import load_config

# === Load config and main data ===
config = load_config()
distance_df = pd.read_csv(config["files"]["trip_distances_output"])
trip_distance_dict = dict(zip(distance_df['UNIQUE_ID'], distance_df['distance_km']))

df = pd.read_csv(config["files"]["main_data"])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

weights = config["weights"]
trip_scores = []

# === Per-trip processing ===
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

    """risk_factor = total_penalty / trip_distance if trip_distance > 0 else 1
    safe_score = round(max(0, 100 - (risk_factor * 100)), 2)"""

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

# === Output ===
score_df = pd.DataFrame(trip_scores)
print(score_df)
