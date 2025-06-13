import os
import time
import yaml
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


class NeuralNetDrivingScore:
    def __init__(self, config_path):
        self.config_path = os.path.join(os.path.dirname(__file__), "..", config_path)
        self.config = self._load_config()
        self.model = None
        self.scaler = None

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def load_data(self):
        data_path = os.path.join(os.path.dirname(__file__), "..", self.config["data_path"])
        df = pd.read_csv(data_path)

        target = self.config["target"]
        X = df.drop(columns=["timestamp", target], errors='ignore')
        X = X.select_dtypes(include=[np.number])
        y = df[target]

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
        print("🔧 Training model...")
        cfg = self.config["nn_model"]
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
        print(f"📊 Test MAE: {mae:.2f}")
        print(f"📈 Test R²:  {r2:.3f}")

    def predict_one(self):
        row = self.X_test[0:1]
        start = time.perf_counter()
        pred = self.model.predict(row)[0][0]
        elapsed = (time.perf_counter() - start) * 1000
        print(f"🔮 Predicted score: {pred:.2f} (inference time: {elapsed:.2f} ms)")

    def run_all(self):
        print("🚀 Starting NeuralNetDrivingScore pipeline...")
        self.load_data()
        self.build_model()
        self.train()
        self.evaluate()
        self.predict_one()
        print("✅ Done.")


if __name__ == "__main__":
    model = NeuralNetDrivingScore("config/config.yaml")
    model.run_all()

