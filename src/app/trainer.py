import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from src.app.model import save_onnx_model

class OnlineTrainer:
    def __init__(self, model):
        self.model = model

    def update(self, X, y):
        self.model.fit(X, y, xgb_model=self.model)
        save_onnx_model(self.model)
        return "Model retrained and saved."