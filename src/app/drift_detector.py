
import pickle
import sqlite3
import logging
import numpy as np
import pandas as pd
from typing import Any, Dict, List, Optional, Tuple

from dataclasses import dataclass
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('drift_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================= CONFIG =============================
@dataclass
class DriftConfig:
    drift_threshold: float = 0.1
    retraining_threshold: float = 0.15
    polling_interval: int = 3600
    min_data_points: int = 1000
    numerical_features: List[str] = None
    categorical_features: List[str] = None
    target_column: str = 'target'
    model_path: str = './models/'
    data_path: str = './data/'

# ============================= DATABASE =============================
class DatabasePoller:
    def __init__(self, db_path: str, table_name: str):
        self.db_path = db_path
        self.table_name = table_name
        self.last_poll_timestamp = None

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_new_data(self):
        conn = self.connect()
        try:
            query = f"""
                SELECT * FROM {self.table_name} 
                WHERE timestamp >= datetime('now', '-1 day')
                ORDER BY timestamp DESC
            """ if self.last_poll_timestamp is None else f"""
                SELECT * FROM {self.table_name} 
                WHERE timestamp > '{self.last_poll_timestamp}'
                ORDER BY timestamp DESC
            """
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                self.last_poll_timestamp = df['timestamp'].max()
            return df
        finally:
            conn.close()

# ============================= STATISTICAL TESTS =============================
class StatisticalDriftDetector:
    def __init__(self, config: DriftConfig):
        self.config = config

    def kolmogorov_smirnov_test(self, ref, curr):
        try:
            return stats.ks_2samp(ref, curr)
        except:
            return 0.0, 1.0

    def chi_squared_test(self, ref, curr):
        try:
            ref_counts, curr_counts = ref.value_counts(), curr.value_counts()
            categories = list(set(ref_counts.index) | set(curr_counts.index))
            ref_vals = [ref_counts.get(cat, 0) for cat in categories]
            curr_vals = [curr_counts.get(cat, 0) for cat in categories]
            return stats.chisquare(curr_vals, ref_vals)
        except:
            return 0.0, 1.0

    def wasserstein_distance(self, ref, curr):
        try:
            return stats.wasserstein_distance(ref, curr)
        except:
            return 0.0

# ============================= DRIFT DETECTOR =============================
class DriftDetector:
    def __init__(self, config: DriftConfig):
        self.config = config
        self.statistical_detector = StatisticalDriftDetector(config)
        self.reference_data = None
        self.drift_history = []

    def set_reference_data(self, data: pd.DataFrame):
        self.reference_data = data.copy()

    def detect_drift(self, current_data: pd.DataFrame) -> Dict[str, Any]:
        drift_results = {"feature_drifts": {}, "drift_detected": False}
        if len(current_data) < self.config.min_data_points:
            return {"drift_detected": False, "reason": "insufficient_data"}

        drift_score = 0
        count = 0

        for col in self.config.numerical_features or []:
            if col in current_data and col in self.reference_data:
                ref, curr = self.reference_data[col].dropna(), current_data[col].dropna()
                score = self.statistical_detector.wasserstein_distance(ref, curr)
                drift_results["feature_drifts"][col] = score
                drift_score += score
                count += 1

        for col in self.config.categorical_features or []:
            if col in current_data and col in self.reference_data:
                ref, curr = self.reference_data[col].dropna(), current_data[col].dropna()
                _, p_value = self.statistical_detector.chi_squared_test(ref, curr)
                score = 1 - p_value
                drift_results["feature_drifts"][col] = score
                drift_score += score
                count += 1

        if count:
            drift_results["overall_drift_score"] = drift_score / count
            drift_results["drift_detected"] = drift_results["overall_drift_score"] > self.config.drift_threshold
        return drift_results

# ============================= MODEL RETRAINER =============================
class ModelRetrainer:
    def __init__(self, config: DriftConfig):
        self.config = config
        self.current_model = None
        self.model_version = 0

    def load_current_model(self):
        try:
            with open(f"{self.config.model_path}current_model.pkl", 'rb') as f:
                self.current_model = pickle.load(f)
            return self.current_model
        except:
            return None

    def retrain_model(self, data: pd.DataFrame):
        features = (self.config.numerical_features or []) + (self.config.categorical_features or [])
        if not all(f in data for f in features + [self.config.target_column]):
            raise ValueError("Missing columns in data")

        X, y = data[features].copy(), data[self.config.target_column]
        for col in self.config.categorical_features or []:
            X[col] = pd.Categorical(X[col]).codes
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        self.model_version += 1
        path = f"{self.config.model_path}model_v{self.model_version}.pkl"
        with open(path, 'wb') as f:
            pickle.dump(model, f)
        with open(f"{self.config.model_path}current_model.pkl", 'wb') as f:
            pickle.dump(model, f)
        return {
            "model_version": self.model_version,
            "mse": mean_squared_error(y_test, model.predict(X_test)),
            "r2": r2_score(y_test, model.predict(X_test)),
            "model_path": path
        }

# ============================= MONITOR =============================
class DriftMonitoringSystem:
    def __init__(self, config: DriftConfig, db_path: str, table_name: str):
        self.config = config
        self.db_poller = DatabasePoller(db_path, table_name)
        self.detector = DriftDetector(config)
        self.retrainer = ModelRetrainer(config)

    def initialize(self, ref_data: pd.DataFrame):
        self.detector.set_reference_data(ref_data)
        self.retrainer.load_current_model()

    def run_cycle(self):
        data = self.db_poller.get_new_data()
        if data.empty:
            return {"new_data": False}

        drift = self.detector.detect_drift(data)
        result = {"new_data": True, "drift": drift}
        if drift["drift_detected"] and drift.get("overall_drift_score", 0) > self.config.retraining_threshold:
            full_data = pd.concat([self.detector.reference_data, data], ignore_index=True)
            result["retrained"] = self.retrainer.retrain_model(full_data)
            self.detector.set_reference_data(full_data)
        return result
