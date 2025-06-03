import os
import pandas as pd
import numpy as np
import joblib
from collections import deque
from scipy.stats import ks_2samp
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score


class ManualDriftDetector:
    def __init__(self, window_size=50, p_value_threshold=0.01):
        self.reference_window = deque(maxlen=window_size)
        self.test_window = deque(maxlen=window_size)
        self.p_value_threshold = p_value_threshold

    def update(self, new_data_dict):
        self.test_window.append(new_data_dict)

        if len(self.test_window) < self.test_window.maxlen:
            return {}, False

        drift_flags = {}
        drift_detected = False

        if len(self.reference_window) == self.reference_window.maxlen:
            ref_df = pd.DataFrame(self.reference_window)
            test_df = pd.DataFrame(self.test_window)

            for col in test_df.columns:
                if col in ref_df:
                    stat, p_value = ks_2samp(ref_df[col], test_df[col])
                    drift_flags[col] = p_value < self.p_value_threshold
                    if drift_flags[col]:
                        drift_detected = True

        # Slide reference window
        self.reference_window = deque(self.test_window, maxlen=self.test_window.maxlen)
        self.test_window.clear()

        return drift_flags, drift_detected


class DrivingScorePipeline:
    def __init__(self, model_path='model.pkl'):
        self.model_path = model_path
        self.drift_detector = ManualDriftDetector()
        self.model = self._load_model()
        self.data_store = []

    def _load_model(self):
        if os.path.exists(self.model_path):
            print("📦 Model loaded.")
            return joblib.load(self.model_path)
        else:
            print("🔧 Initializing new model.")
            return RandomForestRegressor(n_estimators=100)

    def calculate_driving_score(self, data):
        # Replace with actual formulation logic
        score = max(0, 100 - (abs(data["accelerationLateral"]) * 10 + abs(data["accelerationVertical"]) * 5))
        return min(score, 100)

    def preprocess_and_train(self, data):
        df = pd.DataFrame(data)
        X = df.drop(columns=["driving_score"])
        y = df["driving_score"]

        X = X.select_dtypes(include=np.number).fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print("✅ Model retrained. R² Score:", r2_score(y_test, y_pred))

        joblib.dump(self.model, self.model_path)

    def process_instance(self, raw_data):
        driving_score = self.calculate_driving_score(raw_data)
        raw_data["driving_score"] = driving_score
        self.data_store.append(raw_data)

        features_only = {k: v for k, v in raw_data.items() if k != "driving_score"}
        drift_flags, drift_detected = self.drift_detector.update(features_only)

        if drift_detected:
            print("⚠️ Drift Detected in Features:", [k for k, v in drift_flags.items() if v])
            self.preprocess_and_train(self.data_store)
        else:
            print("✅ No significant drift.")

        return driving_score


# Example simulation
if __name__ == "__main__":
    import random
    import time

    pipeline = DrivingScorePipeline()

    for i in range(200):
        sample = {
            "accelerationLateral": random.gauss(0, 1),
            "accelerationVertical": random.gauss(0, 0.5),
            "speedMedian": random.uniform(30, 70)
        }

        # Simulate drift after 100 samples
        if i > 100:
            sample["accelerationLateral"] += 3

        score = pipeline.process_instance(sample)
        print(f"[{i}] Driving Score: {score}")
        time.sleep(0.05)

