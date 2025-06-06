from skl2onnx.common.data_types import FloatTensorType
from onnxmltools.convert import convert_xgboost
import onnx

# Ensure that onnx is installed (pip install onnx)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor
#from catboost import CatBoostRegressor

# ONNX-related imports
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from onnxmltools.convert import convert_xgboost
from onnxmltools.convert.common.data_types import FloatTensorType
import onnx

import sqlite3

DB_PATH = "csv/raxel_traker_db_200325 (1).db"  # <-- Set your database path here
TABLE_NAME = "SampleTable"  # <-- Replace with your actual table name

def load_and_preprocess_data():
    # Connect to SQLite DB
    conn = sqlite3.connect(DB_PATH)

    # Load data into DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)

    # Close connection
    conn.close()

    # Process timestamp and add features
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek

    # Define features and target
    features = [
        "latitude", "longitude",
        "speed_kmh", "acceleration", "deceleration",
        "acceleration_y", "screen_on", "screen_blocked",
        "hour", "dayofweek"
    ]
    target = "safe_score"

    # Final dataset
    df = df[features + [target]].dropna()
    return df[features], df[target]


def evaluate_model(model, X_test, y_test, model_name="Model"):
    start_time = time.time()
    y_pred = model.predict(X_test)
    end_time = time.time()
    print(f"\n✅ {model_name} Results:")
    print("R² Score:", r2_score(y_test, y_pred))
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
    print(f"Total inference time: {end_time - start_time:.6f} seconds")
    print(f"Average time per data point: {(end_time - start_time) / len(X_test):.8f} seconds")

def export_to_onnx(model, X_sample, name):
    try:
        initial_type = [('float_input', FloatTensorType([None, X_sample.shape[1]]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)
        with open(f"{name}.onnx", "wb") as f:
            f.write(onnx_model.SerializeToString())
        print(f"✅ Exported {name} to {name}.onnx")
    except Exception as e:
        print(f"❌ Failed to export {name} to ONNX: {e}")


def run_xgboost(X_train, X_test, y_train, y_test):
    model = XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.1,
                         subsample=0.7, colsample_bytree=0.7, random_state=42)
    model.fit(X_train, y_train)
    evaluate_model(model, X_test, y_test, "XGBoost")

    # Export using onnxmltools
    try:
        initial_type = [('float_input', FloatTensorType([None, X_test.shape[1]]))]
        onnx_model = convert_xgboost(model, initial_types=initial_type)
        with open("XGBoost.onnx", "wb") as f:
            f.write(onnx_model.SerializeToString())
        print("✅ Exported XGBoost to XGBoost.onnx")
    except Exception as e:
        print(f"❌ Failed to export XGBoost to ONNX: {e}")

def main():
    X, y = load_and_preprocess_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)


    run_xgboost(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main()


