from river.drift import ADWIN
from collections import defaultdict

class DriftDetector:
    def __init__(self):
        self.detectors = defaultdict(ADWIN)

    def update(self, X):
        drift_results = {}
        for feature, value in X.items():
            self.detectors[feature].update(value)
            drift_results[feature] = self.detectors[feature].change_detected
        return drift_results