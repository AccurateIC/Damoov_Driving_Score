
import pandas as pd
import numpy as np
import time
import sqlite3
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import AdaBoostRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from catboost import CatBoostRegressor

# Path to your SQLite DB
import yaml

def load_config(path="config.yaml"):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()
SQLITE_PATH = config['database']['sqlite_path']


def load_and_preprocess_data():
    # Read the table from SQLite
    conn = sqlite3.connect(SQLITE_PATH)
    df = pd.read_sql_query("SELECT * FROM merged_output", conn)
    conn.close()

    # Original preprocessing logic
    #df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    #df.dropna(subset=['timestamp'], inplace=True)
    #df['hour'] = df['timestamp'].dt.hour
    #df['dayofweek'] = df['timestamp'].dt.dayofweek

    features = [
        "latitude", "longitude",
        "speed_kmh", "acceleration", "deceleration",
        "acceleration_y", "screen_on", "screen_blocked"
    ]
    target = "safe_score"

    df = df[features + [target]].dropna()
    print(df[['acceleration', 'deceleration', 'acceleration_y', 'safe_score']].corr())
    print(df['safe_score'].head(10))  # CSV vs SQLite version

    return df[features], df[target]

    
def evaluate_model(model, X, y, model_name="Model", label="Test"):
    start_time = time.time()
    y_pred = model.predict(X)
    end_time = time.time()
    print(f"\n✅ {model_name} ({label}) Results:")
    print("R² Score:", r2_score(y, y_pred))
    print("MAE:", mean_absolute_error(y, y_pred))
    print("RMSE:", np.sqrt(mean_squared_error(y, y_pred)))
    print(f"Total inference time: {end_time - start_time:.6f} seconds")
    print(f"Average time per data point: {(end_time - start_time) / len(X):.8f} seconds")


def run_cross_validation(model, X, y, name="Model"):
    scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    print(f"\n📊 {name} Cross-Validated R² Scores: {scores}")
    print(f"📊 Mean R²: {scores.mean():.5f}")

def run_catboost(X_train, y_train, X_val, y_val, X_test, y_test):
    model = CatBoostRegressor(iterations=500, learning_rate=0.05, depth=4,
                              loss_function='RMSE', verbose=0, random_seed=42,
                              early_stopping_rounds=20)
    model.fit(X_train, y_train, eval_set=(X_val, y_val))
    evaluate_model(model, X_val, y_val, "CatBoost", "Validation")
    evaluate_model(model, X_test, y_test, "CatBoost", "Test")

def run_adaboost(X_train, y_train, X_val, y_val, X_test, y_test):
    base = DecisionTreeRegressor(max_depth=5, random_state=42)
    model = AdaBoostRegressor(estimator=base, n_estimators=1500,
                               learning_rate=0.001, random_state=42, loss='exponential')
    model.fit(X_train, y_train)
    evaluate_model(model, X_val, y_val, "AdaBoost", "Validation")
    evaluate_model(model, X_test, y_test, "AdaBoost", "Test")

def run_random_forest(X_train, y_train, X_val, y_val, X_test, y_test):
    model = RandomForestRegressor(n_estimators=400, max_depth=30, min_samples_split=4,
                                   min_samples_leaf=2, max_features='log2', bootstrap=True,
                                   random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    evaluate_model(model, X_val, y_val, "Random Forest", "Validation")
    evaluate_model(model, X_test, y_test, "Random Forest", "Test")

def run_svr(X_train, y_train, X_val, y_val, X_test, y_test):
    model = SVR(C=1000, epsilon=0.5, kernel='rbf', gamma='scale')
    model.fit(X_train, y_train)
    evaluate_model(model, X_val, y_val, "SVR", "Validation")
    evaluate_model(model, X_test, y_test, "SVR", "Test")

def run_xgboost(X_train, y_train, X_val, y_val, X_test, y_test):
    model = XGBRegressor(n_estimators=500, max_depth=6, learning_rate=0.05,
                         subsample=0.7, colsample_bytree=0.7, random_state=42)
    model.fit(X_train, y_train,
              eval_set=[(X_val, y_val)],
              early_stopping_rounds=20, verbose=False)
    evaluate_model(model, X_val, y_val, "XGBoost", "Validation")
    evaluate_model(model, X_test, y_test, "XGBoost", "Test")

def main():
    X, y = load_and_preprocess_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_temp, y_train, y_temp = train_test_split(X_scaled, y, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    run_catboost(X_train, y_train, X_val, y_val, X_test, y_test)
    run_adaboost(X_train, y_train, X_val, y_val, X_test, y_test)
    run_random_forest(X_train, y_train, X_val, y_val, X_test, y_test)
    run_svr(X_train, y_train, X_val, y_val, X_test, y_test)
    run_xgboost(X_train, y_train, X_val, y_val, X_test, y_test)

if __name__ == "__main__":
    main() 