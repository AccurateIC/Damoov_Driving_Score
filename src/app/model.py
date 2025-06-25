
import sqlite3
import numpy as np
import pandas as pd
from dataclasses import dataclass
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from hmmlearn.hmm import GaussianHMM

@dataclass
class Config:
    db_path: str
    table_name: str
    sequence_length: int = 60
    target_column: str = "safe_score"
    model_path: str = "lstm_model.h5"
    hmm_states: int = 3

class LSTM_HMM_Trainer:
    def __init__(self, config: Config):
        self.config = config
        self.features = [
            "latitude", "longitude", "speed_kmh", "acceleration", "deceleration",
            "acceleration_y", "screen_on", "screen_blocked", "hour", "dayofweek"
        ]
        self.scaler = MinMaxScaler()
        self.lstm_model = None
        self.hmm_model = None
        self.behavior_labels = {
            0: "Calm Driver",
            1: "Aggressive Driver",
            2: "Distracted Driver"
        }

    def load_sequences(self, return_ids=False):
        conn = sqlite3.connect(self.config.db_path)
        df = pd.read_sql_query(f"SELECT * FROM {self.config.table_name}", conn)
        conn.close()

        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df.dropna(subset=['timestamp'], inplace=True)
        df['hour'] = df['timestamp'].dt.hour
        df['dayofweek'] = df['timestamp'].dt.dayofweek
        df = df.sort_values(by=['unique_id', 'timestamp'])

        sequences, scores, ids = [], [], []

        for unique_id, trip_data in df.groupby('unique_id'):
            trip_data = trip_data[self.features + [self.config.target_column]].dropna()
            if len(trip_data) < self.config.sequence_length:
                continue
            seq = trip_data[self.features].values[:self.config.sequence_length]
            seq_scaled = self.scaler.fit_transform(seq)
            score = trip_data[self.config.target_column].iloc[0]
            sequences.append(seq_scaled)
            scores.append(score)
            if return_ids:
                ids.append(unique_id)

        return np.array(sequences), np.array(scores), ids if return_ids else None

    def build_lstm_model(self, input_shape):
        model = Sequential()
        model.add(LSTM(64, input_shape=input_shape, return_sequences=True))
        model.add(Dropout(0.3))
        model.add(LSTM(32))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train_lstm(self):
        X, y, _ = self.load_sequences()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.lstm_model = self.build_lstm_model((X.shape[1], X.shape[2]))
        self.lstm_model.fit(X_train, y_train, epochs=20, batch_size=8, validation_split=0.2)

        y_pred = self.lstm_model.predict(X_test).flatten()
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred, squared=False)

        print("\n📊 LSTM Evaluation:")
        print(f"R² Score: {r2:.4f}")
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")

        self.lstm_model.save(self.config.model_path)

    def train_hmm(self):
        X, _, _ = self.load_sequences()
        flat_data = np.concatenate(X, axis=0)
        lengths = [len(seq) for seq in X]

        self.hmm_model = GaussianHMM(n_components=self.config.hmm_states, covariance_type="diag", n_iter=1000)
        self.hmm_model.fit(flat_data, lengths)
        print("✅ HMM model trained on trip sequences.")

    def predict_driver_behaviors(self):
        X, _, ids = self.load_sequences(return_ids=True)
        results = []

        for i, seq in enumerate(X):
            states = self.hmm_model.predict(seq)
            dominant_state = Counter(states).most_common(1)[0][0]
            label = self.behavior_labels.get(dominant_state, "Unknown")
            results.append({"unique_id": ids[i], "driver_behavior": label})

        print(f"✅ Predicted behavior for {len(results)} trips.")
        return results
