
import os
import time
import sqlite3
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import sys

# SHAP & plotting
import shap
import matplotlib.pyplot as plt

# ONNX conversion
from skl2onnx.common.data_types import FloatTensorType
from skl2onnx import convert_sklearn
from onnxmltools.convert import convert_xgboost

# For relative imports if needed
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "app"))


@dataclass
class XGBConfig:
    db_path: str
    table_name: str
    target_column: str = "safe_score"
    onnx_export_path: str = "XGBoost.onnx"


class XGBoostModelTrainer:
    def __init__(self, config: XGBConfig):
        self.config = config
        self.features = [
            "latitude", "longitude",
            "speed_kmh", "acceleration", "deceleration",
            "acceleration_y", "screen_on", "screen_blocked",
            "hour", "dayofweek"
        ]
        self.model = None
        self.scaler = StandardScaler()

    def load_data(self):
        print("📥 Loading data from database...")
        conn = sqlite3.connect(self.config.db_path)
        df = pd.read_sql_query(f"SELECT * FROM {self.config.table_name}", conn)
        conn.close()

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df.dropna(subset=['timestamp'], inplace=True)
        df['hour'] = df['timestamp'].dt.hour
        df['dayofweek'] = df['timestamp'].dt.dayofweek

        df = df[self.features + [self.config.target_column]].dropna()
        print(f"✅ Loaded {len(df)} rows.")
        return df[self.features], df[self.config.target_column]

    def train(self):
        print("\n🚀 Starting training pipeline...")
        X, y = self.load_data()
        print("📊 Scaling and splitting data...")
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        print("🧠 Training XGBoost model...")
        self.model = XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.1,
                                  subsample=0.7, colsample_bytree=0.7, random_state=42)
        self.model.fit(X_train, y_train)

        print("📈 Evaluating model...")
        self.evaluate(X_test, y_test)

        print("📦 Exporting model to ONNX...")
        self.export_to_onnx(X_test)

        print("🔍 Generating SHAP explanations...")
        self.explain_model_with_shap(X_test)

    def train_from_df(self, df: pd.DataFrame):
        print("\n🚀 Starting training from DataFrame...")
        required_cols = self.features + [self.config.target_column]
        df_clean = df[required_cols].dropna()

        X = df_clean[self.features]
        y = df_clean[self.config.target_column]
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

        print("🧠 Training XGBoost model...")
        self.model = XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.1,
                                  subsample=0.7, colsample_bytree=0.7, random_state=42)
        self.model.fit(X_train, y_train)

        print("📈 Evaluating model...")
        self.evaluate(X_test, y_test)

        print("📦 Exporting model to ONNX...")
        self.export_to_onnx(X_test)

        print("🔍 Generating SHAP explanations...")
        self.explain_model_with_shap(X_test)

    def evaluate(self, X_test, y_test):
        start_time = time.time()
        y_pred = self.model.predict(X_test)
        end_time = time.time()

        print(f"\n✅ Evaluation Results:")
        print("R² Score:", r2_score(y_test, y_pred))
        print("MAE:", mean_absolute_error(y_test, y_pred))
        print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
        print(f"⏱️ Total inference time: {end_time - start_time:.6f} seconds")
        print(f"⏱️ Avg time per sample: {(end_time - start_time) / len(X_test):.8f} seconds")

    def export_to_onnx(self, X_sample):
        try:
            initial_type = [('float_input', FloatTensorType([None, X_sample.shape[1]]))]
            onnx_model = convert_xgboost(self.model, initial_types=initial_type)
            with open(self.config.onnx_export_path, "wb") as f:
                f.write(onnx_model.SerializeToString())
            print(f"✅ Exported XGBoost model to {self.config.onnx_export_path}")
        except Exception as e:
            print(f"❌ Failed to export ONNX model: {e}")

    def explain_model_with_shap(self, X_sample):
        if self.model is None:
            raise ValueError("Model is not trained yet.")
        print("\n📊 Generating SHAP summary plot...")

        try:
            explainer = shap.Explainer(self.model)
            shap_values = explainer(X_sample)

            shap.summary_plot(shap_values, X_sample, feature_names=self.features)
            plt.show()  # Required to display the plot in terminal-based script

            # Optional fallback: save to file
            # shap.summary_plot(shap_values, X_sample, feature_names=self.features, show=False)
            # plt.savefig("shap_summary.png")
            # print("📁 SHAP summary plot saved as shap_summary.png")

        except Exception as e:
            print(f"❌ Failed to generate SHAP plot: {e}")
