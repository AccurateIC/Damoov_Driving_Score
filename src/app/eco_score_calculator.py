
import pandas as pd

class EcoScoreCalculator:
    def __init__(self, df: pd.DataFrame, unique_id=None, external_trip_distances=None, thresholds=None, score_weights=None):
        self.df = df.copy()
        self.unique_id = unique_id
        self.external_trip_distances = external_trip_distances or {}
        self.thresholds = thresholds
        self.weights = score_weights
        self._prepare()

    def _prepare(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='s', errors='coerce')
        self.df.dropna(subset=['timestamp'], inplace=True)
        self.df['time_diff'] = self.df['timestamp'].diff().dt.total_seconds().fillna(0)

        if 'midSpeed' in self.df.columns:
            self.df['speed_kmh'] = self.df['midSpeed'] / 3600
            self.df['distance_delta'] = self.df['speed_kmh'] * self.df['time_diff']
        else:
            self.df['distance_delta'] = 0

    def count_harsh_accelerations(self):
        threshold = self.thresholds["acceleration_threshold"]
        return len(self.df[self.df['acceleration'] > threshold])

    def count_harsh_brakings(self):
        threshold = self.thresholds["braking_threshold"]
        return len(self.df[self.df['deceleration'] > threshold])

    def count_harsh_cornerings(self):
        threshold = self.thresholds["cornering_threshold"]
        if 'acceleration_y_original' in self.df.columns:
            corner_vals = self.df['acceleration_y_original']
            corner_vals = corner_vals[corner_vals < 2.0]
            return len(corner_vals[abs(corner_vals) > threshold])
        return 0

    def compute_speed_std(self):
        return self.df['midSpeed'].std() if 'midSpeed' in self.df.columns else 0

    def estimate_trip_distance(self):
        return self.df['distance_delta'].sum() or 0.0

    def calculate_scores(self):
        acc_events = self.count_harsh_accelerations()
        brake_events = self.count_harsh_brakings()
        corner_events = self.count_harsh_cornerings()
        speed_std = self.compute_speed_std()

        distance = self.external_trip_distances.get(self.unique_id, self.estimate_trip_distance())
        distance = max(distance, 0.1)  # avoid division by zero

        acc_rate = min(acc_events / distance, 20)
        brake_rate = min(brake_events / distance, 20)
        corner_rate = min(corner_events / distance, 20)

        # --- Use weights from config ---
        fuel_score = max(0, 100 - (
            acc_rate * self.weights["acc_rate_fuel"] +
            brake_rate * self.weights["brake_rate_fuel"] +
            speed_std * self.weights["speed_std_fuel"]
        ))

        tire_score = max(0, 100 - (
            acc_rate * self.weights["acc_rate_tire"] +
            brake_rate * self.weights["brake_rate_tire"] +
            corner_rate * self.weights["corner_rate_tire"]
        ))

        brake_score = max(0, 100 - (
            brake_rate * self.weights["brake_rate_brake"] +
            distance * self.weights["distance_brake"]
        ))

        eco_score = round(
            self.weights["fuel_score_weight"] * fuel_score +
            self.weights["tire_score_weight"] * tire_score +
            self.weights["brake_score_weight"] * brake_score,
            2
        )

        return {
            "fuel_score": round(fuel_score, 2),
            "tire_score": round(tire_score, 2),
            "brake_score": round(brake_score, 2),
            "eco_score": eco_score,
            "harsh_accelerations": acc_events,
            "harsh_brakings": brake_events,
            "harsh_cornerings": corner_events,
            "speed_std_dev": round(speed_std, 2),
            "trip_distance_used": round(distance, 2)
        }
