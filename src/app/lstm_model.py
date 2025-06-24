
import sqlite3
import numpy as np
import pandas as pd
from dataclasses import dataclass
from collections import Counter, defaultdict
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, silhouette_score
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, GlobalAveragePooling1D
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from hmmlearn.hmm import GaussianHMM


@dataclass
class Config:
    db_path: str
    table_name: str
    sequence_length: int = 60
    target_column: str = "safe_score"
    model_path: str = "lstm_model.keras"
    hmm_states: int = 3
    epochs: int = 30
    step_size: int = 20


class LSTM_HMM_Trainer:
    def __init__(self, config: Config):
        self.config = config
        self.features = [
            "latitude", "longitude", "speed_kmh", "acceleration", "deceleration",
            "acceleration_y", "screen_on", "screen_blocked", "hour", "dayofweek"
        ]
        self.scaler = StandardScaler()
        self.target_scaler = StandardScaler()
        self.lstm_model = None
        self.hmm_model = None
        self.behavior_labels = {
            0: "Calm Driver",
            1: "Aggressive Driver",
            2: "Distracted Driver"
        }

    def load_data(self):
        conn = sqlite3.connect(self.config.db_path)
        df = pd.read_sql_query(f"SELECT * FROM {self.config.table_name}", conn)
        conn.close()
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df.dropna(subset=['timestamp'], inplace=True)
        df['hour'] = df['timestamp'].dt.hour
        df['dayofweek'] = df['timestamp'].dt.dayofweek
        df = df.sort_values(by=['unique_id', 'timestamp'])
        return df

    def preprocess_sequences(self, df, fit_scalers=True, return_ids=False):
        sequences, scores, ids = [], [], []
        all_data = []

        for _, trip in df.groupby('unique_id'):
            trip = trip[self.features + [self.config.target_column]].dropna()
            if len(trip) < self.config.sequence_length:
                continue
            for start in range(0, len(trip) - self.config.sequence_length + 1, self.config.step_size):
                window = trip.iloc[start:start+self.config.sequence_length]
                all_data.append(window[self.features].values)

        all_flat = np.vstack(all_data)
        if fit_scalers:
            self.scaler.fit(all_flat)

        for unique_id, trip in df.groupby('unique_id'):
            trip = trip[self.features + [self.config.target_column]].dropna()
            if len(trip) < self.config.sequence_length:
                continue
            for start in range(0, len(trip) - self.config.sequence_length + 1, self.config.step_size):
                window = trip.iloc[start:start+self.config.sequence_length]
                seq = self.scaler.transform(window[self.features].values)
                sequences.append(seq)
                scores.append(window[self.config.target_column].mean())
                if return_ids:
                    ids.append(unique_id)

        y = self.target_scaler.fit_transform(np.array(scores).reshape(-1, 1)).flatten()
        return np.array(sequences), y, ids if return_ids else None

    def build_lstm_model(self, input_shape):
        model = Sequential()
        model.add(Bidirectional(LSTM(64, return_sequences=True), input_shape=input_shape))
        model.add(GlobalAveragePooling1D())
        model.add(Dense(32, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train_lstm(self):
        df = self.load_data()
        X, y, _ = self.preprocess_sequences(df, fit_scalers=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        self.lstm_model = self.build_lstm_model((X.shape[1], X.shape[2]))

        callbacks = [
            EarlyStopping(patience=6, restore_best_weights=True),
            ReduceLROnPlateau(factor=0.5, patience=3, verbose=1)
        ]

        self.lstm_model.fit(
            X_train, y_train,
            epochs=self.config.epochs,
            batch_size=16,
            validation_split=0.2,
            callbacks=callbacks,
            verbose=1
        )

        y_pred = self.lstm_model.predict(X_test).flatten()
        y_test_orig = self.target_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
        y_pred_orig = self.target_scaler.inverse_transform(y_pred.reshape(-1, 1)).flatten()

        r2 = r2_score(y_test_orig, y_pred_orig)
        mae = mean_absolute_error(y_test_orig, y_pred_orig)
        rmse = np.sqrt(mean_squared_error(y_test_orig, y_pred_orig))

        print("\n📊 Enhanced LSTM Evaluation:")
        print(f"R² Score: {r2:.4f}")
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")

        self.lstm_model.save(self.config.model_path)

    def train_hmm(self):
        df = self.load_data()
        X, _, _ = self.preprocess_sequences(df, fit_scalers=False)

        flat_data = np.concatenate(X, axis=0)
        lengths = [len(seq) for seq in X]

        self.hmm_model = GaussianHMM(
            n_components=self.config.hmm_states,
            covariance_type="diag",
            n_iter=1000,
            random_state=42
        )
        self.hmm_model.fit(flat_data, lengths)
        print("✅ HMM model trained on trip sequences.")

        # Silhouette score
        labels = []
        for seq in X:
            state = Counter(self.hmm_model.predict(seq)).most_common(1)[0][0]
            labels.extend([state]*len(seq))
        score = silhouette_score(flat_data, labels)
        print(f"🔍 Silhouette Score: {score:.3f}")

    def predict_driver_behaviors(self):
        df = self.load_data()
        X, _, ids = self.preprocess_sequences(df, fit_scalers=False, return_ids=True)

        results = defaultdict(list)
        for i, seq in enumerate(X):
            uid = ids[i]
            states = self.hmm_model.predict(seq)
            dominant_state = Counter(states).most_common(1)[0][0]
            results[uid].append(dominant_state)

        final_predictions = []
        for uid, state_list in results.items():
            majority = Counter(state_list).most_common(1)[0][0]
            label = self.behavior_labels.get(majority, "Unknown")
            final_predictions.append({"unique_id": uid, "driver_behavior": label})

        df_result = pd.DataFrame(final_predictions)
        df_result.to_csv("D:/Downloadss/driver_behavior_predictions.csv", index=False)
        print(f"✅ Predicted behavior for {len(final_predictions)} unique trips. Saved to CSV.")
        for r in final_predictions:
            print(r)
        return final_predictions
