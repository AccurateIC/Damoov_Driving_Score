import yaml
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score


class DrivingSafetyScoreModel:
    def __init__(self, config_path):
        # Load configuration from YAML file
        self.config_path = config_path
        self.config = self._load_config()

        # Placeholder variables for dataset, pipeline, and train-test splits
        self.df = None
        self.model_pipeline = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def _load_config(self):
        # Load and return parsed YAML configuration
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def load_and_clean_data(self):
        # Load the dataset
        df = pd.read_csv(self.config["data_path"])

        # Drop irrelevant or non-predictive columns
        to_drop = [
            "ID", "unique_id", "device_id", "number",
            "tick_timestamp", "start_date", "end_date",
            "established_indexA", "established_indexB",
            "risk_factor", "total_penalty", "star_rating"
        ]
        df = df.drop(columns=[c for c in to_drop if c in df.columns])

        # Ensure timestamps are in datetime format
        if not np.issubdtype(df["timestamp"].dtype, np.datetime64):
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])

        # Extract hour and day of week as features
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek

        # Calculate acceleration magnitude and jerk if axis data is available
        if {"acceleration_x_original", "acceleration_y_original", "acceleration_z_original"}.issubset(df.columns):
            df["accel_mag"] = np.sqrt(
                df["acceleration_x_original"]**2 +
                df["acceleration_y_original"]**2 +
                df["acceleration_z_original"]**2
            )
            df["jerk"] = (
                df["accel_mag"].diff() /
                df["timestamp"].diff().dt.total_seconds()
            ).fillna(0)

        # Flag hard braking and acceleration events
        if "deceleration" in df.columns:
            df["hard_brake"] = (df["deceleration"] > 3).astype(int)
        if "acceleration" in df.columns:
            df["hard_accel"] = (df["acceleration"] > 3).astype(int)

        # Fill missing values and filter outliers in the target column
        df = df.fillna(0)
        df = df[(df["safe_score"] < 100) & (df["safe_score"] >= 5)].copy()

        # Store cleaned dataframe
        self.df = df

    def prepare_features_and_labels(self):
        # Define target and features
        target = "safe_score"
        X = self.df.drop(columns=[target, "timestamp"])
        y = self.df[target]

        # Read numeric features from config and filter valid ones
        numeric_features = self.config["features"]["numeric"]
        numeric_features = [c for c in numeric_features if c in X.columns]

        # Define preprocessing pipeline for numeric features
        numeric_transformer = Pipeline([
            ("scaler", StandardScaler())
        ])

        preprocessor = ColumnTransformer([
            ("num", numeric_transformer, numeric_features)
        ])

        # Load model configuration and define full pipeline
        model_config = self.config["model"]
        model_pipeline = Pipeline([
            ("prep", preprocessor),
            ("mlp", MLPRegressor(
                hidden_layer_sizes=tuple(model_config["hidden_layer_sizes"]),
                activation=model_config["activation"],
                solver=model_config["solver"],
                max_iter=model_config["max_iter"],
                random_state=model_config["random_state"]
            ))
        ])

        # Clean input data
        X = X.replace([np.inf, -np.inf], np.nan).dropna()
        y = y.loc[X.index]

        # Store features, labels, and pipeline
        self.X, self.y = X, y
        self.model_pipeline = model_pipeline

    def split_data(self):
        # Perform train-test split using config values
        split_config = self.config["train_test_split"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y,
            test_size=split_config["test_size"],
            random_state=split_config["random_state"]
        )

    def train_model(self):
        # Train model and time the training process
        print("Training model...")
        start = time.time()
        self.model_pipeline.fit(self.X_train, self.y_train)
        end = time.time()
        print(f"✅ Training completed in {end - start:.2f} seconds")

    def evaluate_model(self):
        # Evaluate performance on test set
        y_pred = self.model_pipeline.predict(self.X_test)
        rmse = mean_squared_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)

        print(f"Test RMSE: {rmse:.3f}")
        print(f"Test R²:   {r2:.3f}")
        print("safe_score min:", self.y.min())
        print("safe_score max:", self.y.max())
        print("safe_score mean:", self.y.mean())

    def predict_single_row(self, single_row_df):
        """
        Predict safe_score for a single row and measure inference time.

        Args:
            single_row_df (pd.DataFrame or pd.Series): A single row of input features
        Returns:
            tuple: (predicted_value, inference_time_in_ms)
        """
        if isinstance(single_row_df, pd.Series):
            single_row_df = single_row_df.to_frame().T

        # Clean the row
        single_row_df = single_row_df.replace([np.inf, -np.inf], np.nan).fillna(0)

        # Time the inference
        start_time = time.perf_counter()
        prediction = self.model_pipeline.predict(single_row_df)
        end_time = time.perf_counter()

        inference_time_ms = (end_time - start_time) * 1000
        print(f"Predicted safe_score: {prediction[0]:.2f}")
        print(f"Inference time: {inference_time_ms:.3f} ms")

        return prediction[0], inference_time_ms

    def run_all(self):
        # Orchestrate full pipeline execution
        print("🚀 Starting full pipeline...")
        total_start = time.time()

        self.load_and_clean_data()
        self.prepare_features_and_labels()
        self.split_data()
        self.train_model()
        self.evaluate_model()

        # Run and time a single-row inference
        print("\n🔍 Evaluating single-row prediction...")
        single_row = self.X_test.iloc[[0]]
        _, inference_time = self.predict_single_row(single_row)
        print(f"✅ Single row prediction took {inference_time:.3f} ms")

        total_end = time.time()
        print(f"\n✅ Total execution time: {total_end - total_start:.2f} seconds")


# ------------------ RUNNING SCRIPT ------------------ #
if __name__ == "__main__":
    model = DrivingSafetyScoreModel("config.yaml")
    model.run_all()
