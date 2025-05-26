
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

DATA_PATH = "D:/Downloadss/merged_output.csv"

def load_and_preprocess_data():
    df = pd.read_csv(DATA_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    df['hour'] = df['timestamp'].dt.hour
    df['dayofweek'] = df['timestamp'].dt.dayofweek

    features = [
        "latitude", "longitude",
        "speed_kmh", "acceleration", "deceleration",
        "acceleration_y", "screen_on", "screen_blocked",
        "hour", "dayofweek"
    ]
    target = "safe_score"
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

def run_catboost(X_train, X_test, y_train, y_test):
    model = CatBoostRegressor(iterations=500, learning_rate=0.05, depth=4,
                              loss_function='RMSE', verbose=0, random_seed=42)
    model.fit(X_train, y_train)
    evaluate_model(model, X_test, y_test, "CatBoost")

def run_adaboost(X_train, X_test, y_train, y_test):
    base = DecisionTreeRegressor(max_depth=5, random_state=42)
    model = AdaBoostRegressor(estimator=base, n_estimators=1500,
                               learning_rate=0.001, random_state=42, loss='exponential')
    model.fit(X_train, y_train)
    evaluate_model(model, X_test, y_test, "AdaBoost")

def run_random_forest(X_train, X_test, y_train, y_test):
    model = RandomForestRegressor(n_estimators=400, max_depth=30, min_samples_split=4,
                                   min_samples_leaf=2, max_features='log2', bootstrap=True,
                                   random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    evaluate_model(model, X_test, y_test, "Random Forest")

def run_svr(X_train, X_test, y_train, y_test):
    model = SVR(C=1000, epsilon=0.5, kernel='rbf', gamma='scale')
    model.fit(X_train, y_train)
    evaluate_model(model, X_test, y_test, "SVR")

def run_xgboost(X_train, X_test, y_train, y_test):
    model = XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.1,
                         subsample=0.7, colsample_bytree=0.7, random_state=42)
    model.fit(X_train, y_train)
    evaluate_model(model, X_test, y_test, "XGBoost")

def main():
    X, y = load_and_preprocess_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    run_catboost(X_train, X_test, y_train, y_test)
    run_adaboost(X_train, X_test, y_train, y_test)
    run_random_forest(X_train, X_test, y_train, y_test)
    run_svr(X_train, X_test, y_train, y_test)
    run_xgboost(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main()
