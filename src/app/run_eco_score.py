
import sqlite3
import pandas as pd
from eco_score_calculator import EcoScoreCalculator
from score_pipeline import calculate_trip_distances  # Make sure this is importable

# === CONFIG ===
DB_PATH = "D:/Downloadss/Updated_db/Updated_db.db"
TABLE_NAME = "SampleTable"
START_TABLE = "EventsStartPointTable"
STOP_TABLE = "EventsStopPointTable"

# === LOAD DATA ===
conn = sqlite3.connect(DB_PATH)
#main_df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
main_df = pd.read_sql_query(
    "SELECT unique_id, timestamp, acceleration, deceleration, acceleration_y_original, midSpeed FROM SampleTable",
    conn
)

start_df = pd.read_sql_query(f"SELECT * FROM {START_TABLE}", conn)
stop_df = pd.read_sql_query(f"SELECT * FROM {STOP_TABLE}", conn)
conn.close()

# === CALCULATE EXTERNAL DISTANCES PER TRIP ===
trip_distance_df = calculate_trip_distances(start_df, stop_df)
trip_distance_dict = dict(zip(trip_distance_df["UNIQUE_ID"], trip_distance_df["distance_km"]))

# === RUN ECO SCORE CALCULATOR FOR EACH TRIP ===
eco_scores = []

for uid in main_df["unique_id"].unique():
    trip_df = main_df[main_df["unique_id"] == uid].copy()
    
    if len(trip_df) < 20:
        continue  # Skip very short trips

    calculator = EcoScoreCalculator(
        df=trip_df,
        unique_id=uid,
        external_trip_distances=trip_distance_dict
    )

    score_result = calculator.calculate_scores()
    score_result["unique_id"] = uid
    eco_scores.append(score_result)

# === OUTPUT ===
eco_df = pd.DataFrame(eco_scores)
eco_df_filtered = eco_df[eco_df["trip_distance_used"] > 1.0].reset_index(drop=True)
#print(eco_df.head())
#eco_df.to_csv("D:/Downloadss/eco_scores.csv", index=False)
print("✅ Eco scores calculated and saved to eco_scores.csv")
pd.set_option("display.max_rows", None)  # ✅ Show full DataFrame
print(eco_df) 