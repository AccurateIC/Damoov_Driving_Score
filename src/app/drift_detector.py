import os
import pickle
import sqlite3
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

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
    categorical_features: List[str] = None
    target_column: str = 'safety_score'
    model_path: str = 'models/'
    data_path: str = 'csv/raxel_traker_db_200325 (1).db'

# ========== UTILITIES ==========
def ensure_output_dir(path="drift_results"):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# ========== DATABASE FETCHER ==========
class DatabaseBatchFetcher:
    def __init__(self, db_path: str, table_name: str, batch_size: int = 1000):
        self.db_path = db_path
        self.table_name = table_name
        self.batch_size = batch_size

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_batches(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        conn = self.connect()
        try:
            df = pd.read_sql_query(f"""
                SELECT * FROM {self.table_name}
                ORDER BY timestamp DESC
                LIMIT {self.batch_size * 2}
            """, conn)
            if len(df) < self.batch_size * 2:
                return pd.DataFrame(), pd.DataFrame()
            current_batch = df.iloc[:self.batch_size].copy()
            reference_batch = df.iloc[self.batch_size:self.batch_size * 2].copy()
            return reference_batch, current_batch
        finally:
            conn.close()

# ========== DRIFT DETECTOR ==========
class StatisticalDriftDetector:
    def __init__(self, config: DriftConfig):
        self.config = config

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

class DriftDetector:
    def __init__(self, config: DriftConfig):
        self.config = config
        self.statistical_detector = StatisticalDriftDetector(config)
        self.reference_data = None

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

class DriftMonitoringSystem:
    def __init__(self, config: DriftConfig, db_path: str, table_name: str):
        self.config = config
        self.db_fetcher = DatabaseBatchFetcher(db_path, table_name)

    def run_cycle(self) -> Dict[str, Any]:
        ref_data, curr_data = self.db_fetcher.get_batches()
        if ref_data.empty or curr_data.empty:
            return {"drift_detected": False, "reason": "insufficient_data"}

        detector = DriftDetector(self.config)
        detector.set_reference_data(ref_data)
        drift = detector.detect_drift(curr_data)
        return {
            "drift": drift,
            "reference_data": ref_data,
            "current_data": curr_data
        }

# ========== VISUALIZATION ==========
def plot_data_drift(reference_data: pd.DataFrame, current_data: pd.DataFrame, drift_result: Dict[str, Any], config: DriftConfig):
    sns.set(style="whitegrid")
    num_features = config.numerical_features or []
    cat_features = config.categorical_features or []

    for col in num_features:
        if col in reference_data and col in current_data:
            plt.figure(figsize=(10, 5))
            sns.kdeplot(reference_data[col].dropna(), label="Reference", shade=True)
            sns.kdeplot(current_data[col].dropna(), label="Current", shade=True)
            plt.title(f'Distribution Comparison for {col}\nDrift Score: {drift_result["feature_drifts"].get(col, 0):.4f}')
            plt.xlabel(col)
            plt.ylabel('Density')
            plt.legend()
            plt.tight_layout()
            plt.show()

    for col in cat_features:
        if col in reference_data and col in current_data:
            plt.figure(figsize=(10, 5))
            ref_counts = reference_data[col].value_counts(normalize=True)
            curr_counts = current_data[col].value_counts(normalize=True)
            all_categories = sorted(set(ref_counts.index) | set(curr_counts.index))
            ref_vals = [ref_counts.get(cat, 0) for cat in all_categories]
            curr_vals = [curr_counts.get(cat, 0) for cat in all_categories]

            df_plot = pd.DataFrame({
                "Category": all_categories,
                "Reference": ref_vals,
                "Current": curr_vals
            })

            df_plot = pd.melt(df_plot, id_vars=["Category"], var_name="Dataset", value_name="Proportion")
            sns.barplot(data=df_plot, x="Category", y="Proportion", hue="Dataset")
            plt.title(f'Category Distribution for {col}\nDrift Score: {drift_result["feature_drifts"].get(col, 0):.4f}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    drift_scores = drift_result["feature_drifts"]
    if drift_scores:
        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(drift_scores.values()), y=list(drift_scores.keys()), orient="h")
        plt.axvline(x=config.drift_threshold, color="red", linestyle="--", label="Drift Threshold")
        plt.title("Feature Drift Scores")
        plt.xlabel("Drift Score")
        plt.ylabel("Features")
        plt.legend()
        plt.tight_layout()
        plt.show()

# ========== MAIN EXECUTION ==========
if __name__ == "__main__":
    config = DriftConfig(
        drift_threshold=0.1,
        retraining_threshold=0.15,
        numerical_features=[
            'acceleration_x_original', 'acceleration_y_original', 'acceleration_z_original',
            'acceleration', 'deceleration', 'midSpeed'
        ],
        categorical_features=['weather'],
        target_column='safety_score',
        model_path='models/',
        data_path='csv/raxel_traker_db_200325 (1).db'
    )

    drift_system = DriftMonitoringSystem(config, db_path=config.data_path, table_name='SampleTable')
    result = drift_system.run_cycle()

    output_dir = ensure_output_dir()

    if "reference_data" in result and "current_data" in result:
        result["reference_data"].to_csv(os.path.join(output_dir, "reference_data.csv"), index=False)
        result["current_data"].to_csv(os.path.join(output_dir, "current_data.csv"), index=False)

    with open(os.path.join(output_dir, "drift_result.pkl"), "wb") as f:
        pickle.dump(result["drift"], f)

    print("Drift Detection Result:")
    print(result["drift"])

    if result["drift"].get("drift_detected"):
        plot_data_drift(result["reference_data"], result["current_data"], result["drift"], config)

