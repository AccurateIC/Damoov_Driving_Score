
import pandas as pd

"""class EcoScoreCalculator:
    def __init__(self, df: pd.DataFrame, unique_id=None, external_trip_distances=None):
        self.df = df.copy()
        self.unique_id = unique_id
        self.external_trip_distances = external_trip_distances or {}
        self._prepare()

    def _prepare(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit = 's', errors='coerce')
        self.df.dropna(subset=['timestamp'], inplace=True)
        self.df['time_diff'] = self.df['timestamp'].diff().dt.total_seconds().fillna(0)
       # print(self.df['timestamp'].head())

        if 'midSpeed' in self.df.columns:
            self.df['speed_kmh'] = self.df['midSpeed'] / 3600
            self.df['distance_delta'] = self.df['speed_kmh'] * self.df['time_diff']
        else:
            self.df['distance_delta'] = 0

        if 'speed_kmh' in self.df.columns:
         print("\n🔍 Speed difference stats:")
         print((self.df['speed_kmh'] - self.df['midSpeed']).describe())

    def count_harsh_accelerations(self, threshold=0.8):  # ✅ Tuned threshold
        return len(self.df[self.df['acceleration'] > threshold])

    def count_harsh_brakings(self, threshold=0.6):  # ✅ Tuned threshold
        return len(self.df[self.df['deceleration'] > threshold])

    def count_harsh_cornerings(self, threshold=0.25):  # ✅ Tuned threshold
        if 'acceleration_y_original' in self.df.columns:
            corner_vals = self.df['acceleration_y_original']
            corner_vals = corner_vals[corner_vals < 2.0]  # filter outliers
            return len(corner_vals[abs(corner_vals) > threshold])
        return 0

    def compute_speed_std(self):
        return self.df['midSpeed'].std() if 'midSpeed' in self.df.columns else 0

    def estimate_trip_distance(self):
        return self.df['distance_delta'].sum() or 1.0

    def calculate_scores(self):
        acc_events = self.count_harsh_accelerations()
        brake_events = self.count_harsh_brakings()
        corner_events = self.count_harsh_cornerings()
        speed_std = self.compute_speed_std()

        # ✅ Use external distance if available
        if self.unique_id and self.unique_id in self.external_trip_distances:
            distance = self.external_trip_distances[self.unique_id]
        else:
            distance = self.estimate_trip_distance()

        # ✅ Realistic scoring weights and logic
        fuel_score = max(0, 100 - (acc_events * 2 + brake_events * 2 + speed_std * 2))
        tire_score = max(0, 100 - (acc_events + brake_events + corner_events))
        brake_score = max(0, 100 - (brake_events * 2 + distance * 0.5))

        eco_score = round(0.4 * fuel_score + 0.3 * tire_score + 0.3 * brake_score, 2)
        #self.df['midSpeed'].describe()
      
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
"""
"""import pandas as pd

class EcoScoreCalculator:
    def __init__(self, df: pd.DataFrame, unique_id=None, external_trip_distances=None):
        self.df = df.copy()
        self.unique_id = unique_id
        self.external_trip_distances = external_trip_distances or {}
        self._prepare()

    def _prepare(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='s', errors='coerce')
        self.df.dropna(subset=['timestamp'], inplace=True)
        self.df['time_diff'] = self.df['timestamp'].diff().dt.total_seconds().fillna(0)

        if 'midSpeed' in self.df.columns:
            # midSpeed is already in km/h → convert to km/s
            self.df['speed_kmh'] = self.df['midSpeed'] / 3600
            self.df['distance_delta'] = self.df['speed_kmh'] * self.df['time_diff']
        else:
            self.df['distance_delta'] = 0

    def count_harsh_accelerations(self, threshold=0.8):
        return len(self.df[self.df['acceleration'] > threshold])

    def count_harsh_brakings(self, threshold=0.6):
        return len(self.df[self.df['deceleration'] > threshold])

    def count_harsh_cornerings(self, threshold=0.25):
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

        # Use external trip distance if provided
        if self.unique_id and self.unique_id in self.external_trip_distances:
            distance = self.external_trip_distances[self.unique_id]
        else:
            distance = self.estimate_trip_distance()

        # ✅ Handle short trip cases safely
        if distance < 0.1:  # Less than 100 meters
            return {
                "fuel_score": None,
                "tire_score": None,
                "brake_score": None,
                "eco_score": None,
                "harsh_accelerations": acc_events,
                "harsh_brakings": brake_events,
                "harsh_cornerings": corner_events,
                "speed_std_dev": round(speed_std, 2),
                "trip_distance_used": round(distance, 2),
                "valid_trip": False,
                "note": "Trip too short (< 0.1 km)"
            }

        # Normal scoring
        fuel_score = max(0, 100 - (acc_events * 2 + brake_events * 2 + speed_std * 2))
        tire_score = max(0, 100 - (acc_events + brake_events + corner_events))
        brake_score = max(0, 100 - (brake_events * 2 + distance * 0.5))

        eco_score = round(0.4 * fuel_score + 0.3 * tire_score + 0.3 * brake_score, 2)

        return {
            "fuel_score": round(fuel_score, 2),
            "tire_score": round(tire_score, 2),
            "brake_score": round(brake_score, 2),
            "eco_score": eco_score,
            "harsh_accelerations": acc_events,
            "harsh_brakings": brake_events,
            "harsh_cornerings": corner_events,
            "speed_std_dev": round(speed_std, 2),
            "trip_distance_used": round(distance, 2),
            "valid_trip": True,
            "note": None
        }
"""

"""import pandas as pd

class EcoScoreCalculator:
    def __init__(self, df: pd.DataFrame, unique_id=None, external_trip_distances=None):
        self.df = df.copy()
        self.unique_id = unique_id
        self.external_trip_distances = external_trip_distances or {}
        self._prepare()

    def _prepare(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='s', errors='coerce')
        before_drop = len(self.df)
        self.df.dropna(subset=['timestamp'], inplace=True)
        after_drop = len(self.df)
        print(f"🧹 Dropped {before_drop - after_drop} rows with invalid timestamps for ID {self.unique_id}")

        self.df['time_diff'] = self.df['timestamp'].diff().dt.total_seconds().fillna(0)

        if 'midSpeed' in self.df.columns:
            self.df['speed_kmh'] = self.df['midSpeed'] / 3600
            self.df['distance_delta'] = self.df['speed_kmh'] * self.df['time_diff']
        else:
            self.df['distance_delta'] = 0

    def count_harsh_accelerations(self, threshold=0.8):
        return len(self.df[self.df['acceleration'] > threshold])

    def count_harsh_brakings(self, threshold=0.6):
        return len(self.df[self.df['deceleration'] > threshold])

    def count_harsh_cornerings(self, threshold=0.25):
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

        # Use external trip distance if available
        if self.unique_id and self.unique_id in self.external_trip_distances:
            distance = self.external_trip_distances[self.unique_id]
        else:
            distance = self.estimate_trip_distance()

        # Debug log: always print what's going on
        print(f"✅ Calculating score for ID: {self.unique_id}, distance: {round(distance, 3)} km")

        # TEMP: Score everything, even very short trips — for debugging!
        # To re-enable filtering, uncomment this block:
        #
        # if distance < 0.1:
        #     return {
        #         "fuel_score": None,
        #         "tire_score": None,
        #         "brake_score": None,
        #         "eco_score": None,
        #         "harsh_accelerations": acc_events,
        #         "harsh_brakings": brake_events,
        #         "harsh_cornerings": corner_events,
        #         "speed_std_dev": round(speed_std, 2),
        #         "trip_distance_used": round(distance, 2),
        #         "valid_trip": False,
        #         "note": "Trip too short (< 0.1 km)"
        #     }

        fuel_score = max(0, 100 - (acc_events * 2 + brake_events * 2 + speed_std * 2))
        tire_score = max(0, 100 - (acc_events + brake_events + corner_events))
        brake_score = max(0, 100 - (brake_events * 2 + distance * 0.5))
        eco_score = round(0.4 * fuel_score + 0.3 * tire_score + 0.3 * brake_score, 2)

        return {
            "fuel_score": round(fuel_score, 2),
            "tire_score": round(tire_score, 2),
            "brake_score": round(brake_score, 2),
            "eco_score": eco_score,
            "harsh_accelerations": acc_events,
            "harsh_brakings": brake_events,
            "harsh_cornerings": corner_events,
            "speed_std_dev": round(speed_std, 2),
            "trip_distance_used": round(distance, 2),
            "valid_trip": True,
            "note": None
        }"""

import pandas as pd

class EcoScoreCalculator:
    def __init__(self, df: pd.DataFrame, unique_id=None, external_trip_distances=None):
        self.df = df.copy()
        self.unique_id = unique_id
        self.external_trip_distances = external_trip_distances or {}
        self._prepare()

    def _prepare(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='s', errors='coerce')
        before_drop = len(self.df)
        self.df.dropna(subset=['timestamp'], inplace=True)
        after_drop = len(self.df)

        #print(f"🧹 Dropped {before_drop - after_drop} rows with invalid timestamps for ID {self.unique_id}")
        self.df['time_diff'] = self.df['timestamp'].diff().dt.total_seconds().fillna(0)

        if 'midSpeed' in self.df.columns:
            self.df['speed_kmh'] = self.df['midSpeed'] / 3600
            self.df['distance_delta'] = self.df['speed_kmh'] * self.df['time_diff']
        else:
            self.df['distance_delta'] = 0

    def count_harsh_accelerations(self, threshold=0.8):
        return len(self.df[self.df['acceleration'] > threshold])

    def count_harsh_brakings(self, threshold=0.6):
        return len(self.df[self.df['deceleration'] > threshold])

    def count_harsh_cornerings(self, threshold=0.25):
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

        # ✅ Use external distance if available
        distance = self.external_trip_distances.get(self.unique_id, self.estimate_trip_distance())

       # print(f"✅ Calculating score for ID: {self.unique_id}, distance: {round(distance, 3)} km")

        fuel_score = max(0, 100 - (acc_events * 2 + brake_events * 2 + speed_std * 2))
        tire_score = max(0, 100 - (acc_events + brake_events + corner_events))
        brake_score = max(0, 100 - (brake_events * 2 + distance * 0.5))
        eco_score = round(0.4 * fuel_score + 0.3 * tire_score + 0.3 * brake_score, 2)

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
