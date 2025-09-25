# File: drift_detector.py

import os
import pickle
import logging
import yaml
import pandas as pd
import mysql.connector
from dataclasses import dataclass
from river.drift import ADWIN

from model import XGBoostModelTrainer, XGBConfig
from score_pipeline import run_score_pipeline

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("drift_detection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========== CONFIG ==========
@dataclass
class DriftConfig:
    drift_threshold: float = 0.1
    retraining_threshold: float = 0.15
    target_column: str = "safe_score"
    config_path: str = "config.yaml"


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


# ========== DB FETCHER ==========
class MySQLFetcher:
    def __init__(self, db_conf: dict):
        self.db_conf = db_conf

    def connect(self):
        return mysql.connector.connect(
            host=self.db_conf["host"],
            port=self.db_conf["port"],
            user=self.db_conf["user"],
            password=self.db_conf["password"],
            database=self.db_conf["name"]
        )

    def fetch_today_data(self, table: str) -> pd.DataFrame:
        conn = self.connect()
        query = f"""
            SELECT * FROM {table}
            WHERE DATE(timestamp) = CURDATE()
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df


# ========== DRIFT DETECTOR ==========
class ADWINDriftMonitor:
    def __init__(self, drift_config: DriftConfig, db_conf: dict):
        self.drift_config = drift_config
        self.db_conf = db_conf
        self.detector = ADWIN(delta=0.002)
        self.fetcher = MySQLFetcher(db_conf)

    def run(self):
        today_df = self.fetcher.fetch_today_data(self.db_conf["main_table"])
        if today_df.empty:
            logger.warning("No trips found for today — skipping drift detection")
            return {"drift_detected": False, "reason": "no_data"}

        drift_detected = False
        for val in today_df[self.drift_config.target_column].dropna():
            self.detector.update(val)
            if self.detector.change_detected:
                drift_detected = True

        logger.info(f"Drift Detected: {drift_detected}")
        return {
            "drift_detected": drift_detected,
            "today_rows": len(today_df)
        }


# ========== MAIN ==========
if __name__ == "__main__":
    db_conf = load_config()["database"]
    drift_conf = DriftConfig()

    monitor = ADWINDriftMonitor(drift_conf, db_conf)
    result = monitor.run()

    os.makedirs("drift_results", exist_ok=True)
    with open("drift_results/drift_result.pkl", "wb") as f:
        pickle.dump(result, f)

    if result["drift_detected"]:
        logger.info("⚠️ Retraining triggered due to detected drift.")

        # Step 1: Recompute safe scores for trips
        run_score_pipeline(
            db_conf=db_conf,
            config=load_config()
        )

        # Step 2: Retrain XGBoost
        xgb_conf = XGBConfig(
            db_path=None,  # not used in MySQL fetch
            table_name=db_conf["main_table"],
            target_column=drift_conf.target_column,
            onnx_export_path="XGBoost.onnx"
        )
        model = XGBoostModelTrainer(xgb_conf)
        model.train()

    else:
        logger.info("✅ No significant drift detected.")
