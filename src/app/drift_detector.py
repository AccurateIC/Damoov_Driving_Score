# File: drift_detector.py

import os
import pickle
import sqlite3
import logging
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass
from river.drift import ADWIN
from pydantic import BaseModel
from typing import List

#from model import XGBoostModelTrainer, XGBConfig
from model import Config, LSTM_HMM_Trainer

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('drift_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ========== CONFIG ==========
@dataclass
class DriftConfig:
    drift_threshold: float = 0.1
    retraining_threshold: float = 0.15
    min_data_points: int = 1000
    numerical_features: List[str] = None
    target_column: str ='safe_score'
    model_path: str = 'models/driving_model.pkl'
    reference_db_path: str = 'csv/raxel_traker_db_200325 (1).db'
    current_db_path: str = 'csv/tracking_raw_DB_150525 (2).db'
    table_name: str = 'SampleTable'
    config_path: str = 'config.yaml'

# ========== UTILITIES ==========
def ensure_output_dir(path="drift_results"):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# ========== DATABASE FETCHER ==========
class DualDBFetcher:
    def __init__(self, ref_db_path: str, curr_db_path: str, table_name: str, limit: int = 1000):
        self.ref_db_path = ref_db_path
        self.curr_db_path = curr_db_path
        self.table_name = table_name
        self.limit = limit

    def fetch_data(self, db_path: str) -> pd.DataFrame:
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query(
                f"SELECT * FROM {self.table_name} ORDER BY timestamp DESC LIMIT {self.limit}",
                conn
            )

    def get_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.fetch_data(self.ref_db_path), self.fetch_data(self.curr_db_path)

# ========== DRIFT DETECTOR ==========
class ADWINDriftDetector:
    def __init__(self, delta: float = 0.002):
        self.delta = delta

    def detect_drift(self, ref: pd.DataFrame, curr: pd.DataFrame, features: List[str]) -> Tuple[Dict[str, float], float]:
        scores = {}
        total_score = 0
        for feat in features:
            ref_series = ref[feat].dropna()
            curr_series = curr[feat].dropna()
            series = pd.concat([ref_series, curr_series])
            detector = ADWIN(delta=self.delta)
            for value in series:
                detector.update(value)
            score = detector.estimation
            scores[feat] = score
            total_score += score
        avg_score = total_score / len(scores) if scores else 0.0
        return scores, avg_score

# ========== MONITOR ==========
class ADWINDriftMonitoring:
    def __init__(self, config: DriftConfig):
        self.config = config
        self.fetcher = DualDBFetcher(config.reference_db_path, config.current_db_path, config.table_name)
        self.detector = ADWINDriftDetector()

    def run(self):
        ref, curr = self.fetcher.get_data()
        if ref.empty or curr.empty:
            logger.warning("Insufficient data for drift detection.")
            return {"drift_detected": False, "reason": "insufficient_data"}

        drift_scores, avg_score = self.detector.detect_drift(ref, curr, self.config.numerical_features)
        drift_detected = avg_score > self.config.drift_threshold
        logger.info(f"Drift Detected: {drift_detected} | Score: {avg_score:.4f}")
        return {
            "drift_detected": drift_detected,
            "average_drift_score": avg_score,
            "feature_drifts": drift_scores,
            "ref_data": ref,
            "curr_data": curr
        }
    

# ========== MAIN ==========
if __name__ == "__main__":
    config = DriftConfig(
        numerical_features=[
            'acceleration_x_original', 'acceleration_y_original', 'acceleration_z_original',
            'acceleration', 'deceleration', 'midSpeed'
        ],
        
    )


    monitor = ADWINDriftMonitoring(config)
    result = monitor.run()

    output_dir = ensure_output_dir()
    if "ref_data" in result and "curr_data" in result:
        result["ref_data"].to_csv(os.path.join(output_dir, "reference_data.csv"), index=False)
        result["curr_data"].to_csv(os.path.join(output_dir, "current_data.csv"), index=False)

    with open(os.path.join(output_dir, "drift_result.pkl"), "wb") as f:
        pickle.dump(result, f)

    if result["drift_detected"]:
        logger.info("Retraining triggered due to detected drift.")

        # Choose ONE of the two retraining options below:

        # Option 1: Retrain DrivingSafetyScoreModel from model.py
        xgb_config = XGBConfig(
            db_path=config.current_db_path,
            table_name=config.table_name,
            target_column=config.target_column,
            onnx_export_path="XGBoost.onnx"
        )
        model = XGBoostModelTrainer(xgb_config)

        combined_df = pd.concat([result["ref_data"], result["curr_data"]])
        combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], errors='coerce')
        combined_df.dropna(subset=['timestamp'], inplace=True)
        combined_df['hour'] = combined_df['timestamp'].dt.hour
        combined_df['dayofweek'] = combined_df['timestamp'].dt.dayofweek    

        model.train_from_df(combined_df)


        # Option 2: Retrain XGBoostModelTrainer from xgboost_model.py
        # xgb_config = XGBConfig(
        #     db_path=config.current_db_path,
        #     table_name=config.table_name,
        #     target_column=config.target_column,
        #     onnx_export_path="models/xgb_model.onnx"
        # )
        # xgb_trainer = XGBoostModelTrainer(xgb_config)
        # xgb_trainer.train()

    else:
        logger.info("No significant drift detected.")


