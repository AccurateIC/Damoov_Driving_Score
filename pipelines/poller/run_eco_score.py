
import sqlite3
import pandas as pd
from eco_score_calculator import EcoScoreCalculator
from score_pipeline import calculate_trip_distances
from pathlib import Path 
import yaml
import logging
import sys

# === SETUP LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === LOAD CONFIG FILE ===
def load_config():
    base_dir = Path(__file__).resolve().parent.parent.parent
    config_path = base_dir / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"❌ config.yaml not found at {config_path}")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# === LOAD CONFIG ===
try:
    config = load_config()
    db_config = config["database"]
    thresholds = config["thresholds"]
    event_thresholds = config["event_thresholds"]
    score_weights = config["score_weights"]
except FileNotFoundError as e:
    logging.error(str(e))
    sys.exit(1)
except KeyError as e:
    logging.error("❌ Missing key in config.yaml: %s", e)
    sys.exit(1)
except yaml.YAMLError as e:
    logging.error("❌ Failed to parse config.yaml: %s", e)
    sys.exit(1)

# === CONFIG ===
DB_PATH = db_config["sqlite_path"]
TABLE_NAME = db_config["main_table"]
START_TABLE = db_config["start_table"]
STOP_TABLE = db_config["stop_table"]

# === LOAD DATA ===
try:
    conn = sqlite3.connect(DB_PATH)
except sqlite3.Error as e:
    logging.error("❌ Failed to connect to database: %s", e)
    sys.exit(1)

try:
    main_df = pd.read_sql_query(
        f"""
        SELECT unique_id, timestamp, acceleration, deceleration, 
               acceleration_y_original, midSpeed 
        FROM {TABLE_NAME}
        """,
        conn
    )
    start_df = pd.read_sql_query(f"SELECT * FROM {START_TABLE}", conn)
    stop_df = pd.read_sql_query(f"SELECT * FROM {STOP_TABLE}", conn)
except Exception as e:
    logging.error("❌ Failed to read from tables: %s", e)
    conn.close()
    sys.exit(1)

conn.close()

# === CALCULATE EXTERNAL DISTANCES PER TRIP ===
trip_distance_df = calculate_trip_distances(start_df, stop_df)
trip_distance_df.columns = [col.lower() for col in trip_distance_df.columns]
trip_distance_dict = dict(zip(trip_distance_df["unique_id"], trip_distance_df["distance_km"]))

# === RUN ECO SCORE CALCULATOR FOR EACH TRIP ===
eco_scores = []

for uid, trip_df in main_df.groupby("unique_id"):
    if len(trip_df) < 20:
        continue  # Skip short trips

    try:
        calculator = EcoScoreCalculator(
            df=trip_df,
            unique_id=uid,
            external_trip_distances=trip_distance_dict,
            thresholds=event_thresholds,
            score_weights=score_weights
        )
        score_result = calculator.calculate_scores()
        score_result["unique_id"] = uid
        eco_scores.append(score_result)

    except Exception as e:
        logging.warning("⚠️ Failed to calculate score for unique_id=%s: %s", uid, e)

# === OUTPUT ===
eco_df = pd.DataFrame(eco_scores)
eco_df_filtered = eco_df[eco_df["trip_distance_used"] > thresholds["trip_distance_min"]].reset_index(drop=True)

logging.info("✅ Eco scores calculated successfully. Filtered %d trips with distance > %.2f km", 
             len(eco_df_filtered), thresholds["trip_distance_min"])

pd.set_option("display.max_rows", None)
logging.info("\n%s", eco_df_filtered.to_string(index=False))

# Optional: save to file
output_path = "eco_scores.csv"
eco_df_filtered.to_csv(output_path, index=False)
logging.info("✅ Saved results to %s", output_path)
