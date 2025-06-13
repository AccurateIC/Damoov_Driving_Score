import os
import time
import yaml
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.neural_network import MLPRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


class DrivingScoreBase:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self._load_config() 
        self.df = None

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def load_and_clean_data(self):
        df = pd.read_csv(self.config["data_path"])
        to_drop = [
            "ID", "unique_id", "device_id", "number",
            "tick_timestamp", "start_date", "end_date",
            "established_indexA", "established_indexB",
            "risk_factor", "total_penalty", "star_rating"
        ]
        df = df.drop(columns=[c for c in to_drop if c in df.columns])

        if not np.issubdtype(df["timestamp"].dtype, np.datetime64):
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.dropna(subset=["timestamp"])
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek

        if {"acceleration_x_original", "acceleration_y_original", "acceleration_z_original"}.issubset(df.columns):
            df["accel_mag"] = np.sqrt(
                df["acceleration_x_original"] ** 2 +
                df["acceleration_y_original"] ** 2 +
                df["acceleration_z_original"] ** 2
            )
            df["jerk"] = (
                df["accel_mag"].diff() /
                df["timestamp"].diff().dt.total_seconds()
            ).fillna(0)

        if "deceleration" in df.columns:
            df["hard_brake"] = (df["deceleration"] > 3).astype(int)
        if "acceleration" in df.columns:
            df["hard_accel"] = (df["acceleration"] > 3).astype(int)

        df = df.fillna(0)
        df = df[(df["safe_score"] < 100) & (df["safe_score"] >= 5)].copy()
        self.df = df


class MLPDrivingScoreModel(DrivingScoreBase):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.model_pipeline = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def prepare_features_and_labels(self):
        target = "safe_score"
        X = self.df.drop(columns=[target, "timestamp"])
        y = self.df[target]
        numeric_features = self.config["features"]["numeric"]
        numeric_features = [c for c in numeric_features if c in X.columns]

        numeric_transformer = Pipeline([("scaler", StandardScaler())])
        preprocessor = ColumnTransformer([("num", numeric_transformer, numeric_features)])

        model_config = self.config["model"]
        self.model_pipeline = Pipeline([
            ("prep", preprocessor),
            ("mlp", MLPRegressor(
                hidden_layer_sizes=tuple(model_config["hidden_layer_sizes"]),
                activation=model_config["activation"],
                solver=model_config["solver"],
                max_iter=model_config["max_iter"],
                random_state=model_config["random_state"]
            ))
        ])

        X = X.replace([np.inf, -np.inf], np.nan).dropna()
        y = y.loc[X.index]
        self.X, self.y = X, y

    def split_data(self):
        split_config = self.config["train_test_split"]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y,
            test_size=split_config["test_size"],
            random_state=split_config["random_state"]
        )

    def train(self):
        print("🔧 Training MLP model...")
        start = time.time()
        self.model_pipeline.fit(self.X_train, self.y_train)
        print(f"✅ Training time: {time.time() - start:.2f} seconds")

    def evaluate(self):
        y_pred = self.model_pipeline.predict(self.X_test)
        rmse = mean_squared_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        print(f"📊 MLP Test RMSE: {rmse:.2f}")
        print(f"📈 MLP Test R²:   {r2:.3f}")

    def predict_one(self):
        row = self.X_test.iloc[[0]].replace([np.inf, -np.inf], np.nan).fillna(0)
        start = time.perf_counter()
        pred = self.model_pipeline.predict(row)[0]
        elapsed = (time.perf_counter() - start) * 1000
        print(f"🔮 MLP Predicted score: {pred:.2f} (inference time: {elapsed:.2f} ms)")


class KerasDrivingScoreModel(DrivingScoreBase):
    def __init__(self, config_path):
        super().__init__(config_path)
        self.model = None
        self.scaler = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def prepare_data(self):
        target = self.config["target"]
        X = self.df.drop(columns=["timestamp", target], errors='ignore')
        X = X.select_dtypes(include=[np.number])
        y = self.df[target]
        X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, y,
            test_size=self.config["train_test_split"]["test_size"],
            random_state=self.config["train_test_split"]["random_state"]
        )

    def build_model(self):
        cfg = self.config["nn_model"]
        self.model = Sequential([
            Dense(cfg["layer1"], activation='relu', input_shape=(self.X_train.shape[1],)),
            Dropout(cfg.get("dropout1", 0.2)),
            Dense(cfg["layer2"], activation='relu'),
            Dropout(cfg.get("dropout2", 0.1)),
            Dense(1)
        ])
        self.model.compile(optimizer=cfg["optimizer"], loss='mse', metrics=['mae'])

    def train(self):
        cfg = self.config["nn_model"]
        print("🔧 Training Keras model...")
        start = time.time()

        early_stop = EarlyStopping(
            monitor='val_loss',
            patience=cfg.get("patience", 5),
            restore_best_weights=True
        )

        self.model.fit(
            self.X_train, self.y_train,
            epochs=cfg["epochs"],
            batch_size=cfg["batch_size"],
            validation_split=0.1,
            callbacks=[early_stop],
            verbose=1
        )
        print(f"✅ Training time: {time.time() - start:.2f} seconds")

    def evaluate(self):
        y_pred = self.model.predict(self.X_test).flatten()
        mae = mean_absolute_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        print(f"📊 Keras Test MAE: {mae:.2f}")
        print(f"📈 Keras Test R²:  {r2:.3f}")

    def predict_one(self):
        row = self.X_test[0:1]
        start = time.perf_counter()
        pred = self.model.predict(row)[0][0]
        elapsed = (time.perf_counter() - start) * 1000
        print(f"🔮 Keras Predicted score: {pred:.2f} (inference time: {elapsed:.2f} ms)")


# Unified entry point
if __name__ == "__main__":
    config_path = "config/config.yaml"

    print("\n=== Running MLPDrivingScoreModel ===")
    mlp_model = MLPDrivingScoreModel(config_path)
    mlp_model.load_and_clean_data()
    mlp_model.prepare_features_and_labels()
    mlp_model.split_data()
    mlp_model.train()
    mlp_model.evaluate()
    mlp_model.predict_one()

    print("\n=== Running KerasDrivingScoreModel ===")
    keras_model = KerasDrivingScoreModel(config_path)
    keras_model.load_and_clean_data()
    keras_model.prepare_data()
    keras_model.build_model()
    keras_model.train()
    keras_model.evaluate()
    keras_model.predict_one()


