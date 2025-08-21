import pandas as pd
from src.app.Formulation.utils import load_csv_with_timestamp, finalize_event

class DamoovAccelerationScorer:
    def __init__(self, threshold, min_speed, min_duration, max_gap):
        self.threshold = threshold
        self.min_speed = min_speed
        self.min_duration = min_duration
        self.max_gap = max_gap

    def detect_events(self):
        df = self.df[(self.df['acceleration'] > self.threshold) & (self.df['speed_kmh'] >= self.min_speed)]
        df = df.sort_values(by='timestamp').reset_index(drop=True)

        events, current_event = [], []
        for _, point in df.iterrows():
            if not current_event or (point['timestamp'] - current_event[-1]['timestamp']).total_seconds() <= self.max_gap:
                current_event.append(point)
            else:
                finalize_event(current_event, events, 'timestamp', self.min_duration,
                               {'max_acceleration': 'acceleration', 'avg_speed_kmh': 'speed_kmh'})
                current_event = [point]

        finalize_event(current_event, events, 'timestamp', self.min_duration,
                       {'max_acceleration': 'acceleration', 'avg_speed_kmh': 'speed_kmh'})
        self.events_df = pd.DataFrame(events)

    def calculate_penalties(self):
        if self.events_df.empty:
            self.events_df['penalty_acc'] = 0.0
        else:
            self.events_df['penalty_acc'] = (
                0.0825 * self.events_df['avg_speed_kmh'] +
                1.0135 * self.events_df['duration_s'] +
                0.1003 * self.events_df['max_acceleration']
            )

    def get_events(self):
        return self.events_df


class DamoovDeccelerationScorer:
    def __init__(self, dec_threshold, min_speed, min_duration, max_gap):
        self.dec_threshold = dec_threshold
        self.min_speed = min_speed
        self.min_duration = min_duration
        self.max_gap = max_gap

    def detect_events(self):
        df = self.df[(self.df['deceleration'] > self.dec_threshold) & (self.df['speed_kmh'] >= self.min_speed)]
        df = df.sort_values(by='timestamp').reset_index(drop=True)

        events, current_event = [], []
        for _, point in df.iterrows():
            if not current_event or (point['timestamp'] - current_event[-1]['timestamp']).total_seconds() <= self.max_gap:
                current_event.append(point)
            else:
                finalize_event(current_event, events, 'timestamp', self.min_duration,
                               {'max_deceleration': 'deceleration', 'avg_speed_kmh': 'speed_kmh'})
                current_event = [point]

        finalize_event(current_event, events, 'timestamp', self.min_duration,
                       {'max_deceleration': 'deceleration', 'avg_speed_kmh': 'speed_kmh'})
        self.events_df = pd.DataFrame(events)

    def calculate_penalties(self):
        if self.events_df.empty:
            self.events_df['penalty_braking'] = 0.0
        else:
            self.events_df['penalty_braking'] = (
                0.1101 * self.events_df['avg_speed_kmh'] +
                0.7565 * self.events_df['duration_s'] +
                -0.0882 * abs(self.events_df['max_deceleration'])
            )

    def get_events(self):
        return self.events_df


class DamoovCorneringScorer:
    def __init__(self, accy_threshold, min_speed, min_duration, max_gap):
        self.accy_threshold = accy_threshold
        self.min_speed = min_speed
        self.min_duration = min_duration
        self.max_gap = max_gap

    def detect_events(self):
        df = self.df[(self.df['acceleration_y_original'].abs() > self.accy_threshold) & (self.df['speed_kmh'] >= self.min_speed)]
        df = df.sort_values(by='timestamp').reset_index(drop=True)

        events, current_event = [], []
        for _, point in df.iterrows():
            if not current_event or (point['timestamp'] - current_event[-1]['timestamp']).total_seconds() <= self.max_gap:
                current_event.append(point)
            else:
                finalize_event(current_event, events, 'timestamp', self.min_duration,
                               {'avg_speed_kmh': 'speed_kmh'})
                current_event = [point]

        finalize_event(current_event, events, 'timestamp', self.min_duration,
                       {'avg_speed_kmh': 'speed_kmh'})
        self.events_df = pd.DataFrame(events)

    def calculate_penalties(self):
        if self.events_df.empty:
            self.events_df['penalty_cornering'] = 0.0
        else:
            self.events_df['penalty_cornering'] = (
                0.0825 * self.events_df['avg_speed_kmh'] +
                0.1422 * self.events_df['duration_s']
            )

    def get_events(self):
        return self.events_df


class SpeedingDetectorFixedLimit:
    def __init__(self, speed_limit, min_duration, max_gap):
        self.speed_limit = speed_limit
        self.min_duration = min_duration
        self.max_gap = max_gap

    def detect_speeding(self):
        df = self.df[self.df['speed_kmh'] > self.speed_limit].copy()
        df = df.sort_values(by='timestamp').reset_index(drop=True)
        df['over_limit_by_avg'] = df['speed_kmh'] - self.speed_limit

        events, current_event = [], []
        for _, point in df.iterrows():
            if not current_event or (point['timestamp'] - current_event[-1]['timestamp']).total_seconds() <= self.max_gap:
                current_event.append(point)
            else:
                finalize_event(current_event, events, 'timestamp', self.min_duration,
                               {'avg_speed_kmh': 'speed_kmh', 'over_limit_by_avg': 'over_limit_by_avg'})
                current_event = [point]

        finalize_event(current_event, events, 'timestamp', self.min_duration,
                       {'avg_speed_kmh': 'speed_kmh', 'over_limit_by_avg': 'over_limit_by_avg'})
        self.events_df = pd.DataFrame(events)

    def assign_penalties(self):
        if self.events_df.empty:
            self.events_df['penalty_speeding'] = 0.0
            return

        # Assign coefficients based on over-speed
        self.events_df['coefficient'] = self.events_df['over_limit_by_avg'].apply(assign_coefficient)
        self.events_df['penalty_point'] = self.events_df['duration_s'] * self.events_df['coefficient']

        # Normalize penalty_point column per trip
        min_p = self.events_df['penalty_point'].min()
        max_p = self.events_df['penalty_point'].max()

        if max_p != min_p:
            self.events_df['penalty_speeding'] = (
                (self.events_df['penalty_point'] - min_p) / (max_p - min_p)
            )
        else:
            self.events_df['penalty_speeding'] = 0.0

    def get_events(self):
        return self.events_df


class PhoneUsageDetector:
    def __init__(self, min_duration, max_gap):
        self.min_duration = min_duration
        self.max_gap = max_gap

    def detect_phone_usage(self):
        df = self.df.copy()
        df['phone_usage_flag'] = ((df['screen_on'] == 1) & (df['screen_blocked'] == 0)).astype(int)
        df = df[df['phone_usage_flag'] == 1].sort_values(by='timestamp').reset_index(drop=True)

        events, current_event = [], []
        for _, point in df.iterrows():
            if not current_event or (point['timestamp'] - current_event[-1]['timestamp']).total_seconds() <= self.max_gap:
                current_event.append(point)
            else:
                finalize_event(current_event, events, 'timestamp', self.min_duration,
                               {'avg_speed_kmh': 'speed_kmh'})
                current_event = [point]

        finalize_event(current_event, events, 'timestamp', self.min_duration,
                       {'avg_speed_kmh': 'speed_kmh'})
        self.events_df = pd.DataFrame(events)

    def assign_penalties(self):
        if self.events_df.empty:
            self.events_df['penalty_phone'] = 0.0
        else:
            self.events_df['penalty_phone'] = self.events_df['duration_s'] * 0.6  # ✅ Fixed coefficient

    def get_events(self):
        return self.events_df



def assign_coefficient(over_speed):
    if over_speed <= 0: return 0
    elif over_speed <= 40: return 0.0434
    elif over_speed <= 55: return 0.2372
    elif over_speed <= 105: return 0.2929
    else:
        return 0.4821
    
    