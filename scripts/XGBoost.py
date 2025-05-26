#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[4]:


# Re-import necessary libraries after kernel reset
import pandas as pd

# Reload the uploaded CSV file
file_path = "D:/Downloadss/merged_output.csv"
df = pd.read_csv(file_path)

# Columns used for calculation — as specified by user
used_features = [
    'timestamp', 'speed_kmh', 'acceleration', 'deceleration',
    'acceleration_y', 'screen_on', 'screen_blocked',
    'safe_score', 'risk_factor', 'total_penalty', 'star_rating'
]

# Keep only the specified columns
df_cleaned = df[used_features].copy()

# Display info and head of the cleaned DataFrame
df_cleaned.info(), df_cleaned.head()


# In[ ]:





# In[50]:


df['safe_score'].value_counts()


# # Catboost

# In[18]:


pip install catboost


# In[49]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt
import numpy as np

# Load your data
df = pd.read_csv("merged_output.csv")

# Define features and target (safe_score is now the target)
features = [
    "timestamp", "speed_kmh", "acceleration", "deceleration", "acceleration_y",
    "screen_on", "screen_blocked"
]
target = "safe_score"

# Drop rows with missing values
df.dropna(subset=features + [target], inplace=True)

# Convert timestamp to numeric
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["timestamp"] = df["timestamp"].astype('int64') // 10**9

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

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Split features and target
X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize CatBoostRegressor
cat_model = CatBoostRegressor(
    iterations=500,
    learning_rate=0.05,
    depth=4,
    loss_function='RMSE',
    eval_metric='RMSE',
    verbose=100,
    random_seed=42
)

# Fit the model
cat_model.fit(X_train, y_train, eval_set=(X_test, y_test), early_stopping_rounds=30)

# Predict
y_pred = cat_model.predict(X_test)

# Evaluation
print("\nMean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
print("Root Mean Squared Error (RMSE):", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R² Score:", r2_score(y_test, y_pred))

import time

start_time = time.time()
ada_preds = cat_model.predict(X_test)
end_time = time.time()

print(f"Total inference time: {end_time - start_time:.6f} seconds")
print(f"Average per data point: {(end_time - start_time)/len(X_test):.8f} seconds")

# Plot predicted vs actual
"""plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Safe Score")
plt.ylabel("Predicted Safe Score")
plt.title("Actual vs Predicted Safe Score")
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--')
plt.grid(True)
plt.tight_layout()
plt.show()"""

# Plot feature importance
"""feature_importance = model.get_feature_importance()
plt.figure(figsize=(10, 5))
plt.barh(features, feature_importance)
plt.xlabel("Importance")
plt.title("Feature Importance")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()"""


# # AdaBoost Model

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load data
df = pd.read_csv("D:/Downloadss/merged_output.csv")

# Convert timestamp to epoch seconds
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["timestamp"] = df["timestamp"].astype("int64") // 10**9

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

# Drop rows with missing values
df.dropna(subset=features + [target], inplace=True)

# Shuffle and split data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# AdaBoost with decision tree
base_estimator = DecisionTreeRegressor(max_depth=5, random_state=42)
ada_model = AdaBoostRegressor(
    estimator=base_estimator,
    n_estimators=1500,
    learning_rate=0.001,
    random_state=42,
    loss='exponential'
)

# Train
ada_model.fit(X_train, y_train)

# Predict
y_pred = ada_model.predict(X_test)

# Evaluate
print("\nMean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
print("Root Mean Squared Error (RMSE):", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R² Score:", r2_score(y_test, y_pred))

import time

start_time = time.time()
ada_preds = ada_model.predict(X_test)
end_time = time.time()

print(f"Total inference time: {end_time - start_time:.6f} seconds")
print(f"Average per data point: {(end_time - start_time)/len(X_test):.8f} seconds")

# Plot
"""plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Safe Score")
plt.ylabel("Predicted Safe Score")
plt.title("Actual vs Predicted Safe Score (AdaBoost)")
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--')
plt.grid(True)
plt.tight_layout()
plt.show()"""


# # Random Forest Model

# In[4]:


import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("D:/Downloadss/merged_output.csv")

# Convert and extract time features
"""df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
df.dropna(subset=["timestamp"], inplace=True)
df["hour"] = df["timestamp"].dt.hour
df["dayofweek"] = df["timestamp"].dt.dayofweek
df["epoch"] = df["timestamp"].astype("int64") // 10**9"""

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

# Drop rows with missing values
df.dropna(subset=features + [target], inplace=True)

# Prepare data
X = df[features]
y = df[target]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Model: Random Forest (fine-tuned)
rf_model = RandomForestRegressor(
    n_estimators=400,
    max_depth=30,
    min_samples_split=4,
    min_samples_leaf=2,
    max_features='log2',
    bootstrap=True,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = rf_model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))
print("R² Score:", r2_score(y_test, y_pred))

import time

start_time = time.time()
ada_preds = cat_model.predict(X_test)
end_time = time.time()

print(f"Total inference time: {end_time - start_time:.6f} seconds")
print(f"Average per data point: {(end_time - start_time)/len(X_test):.8f} seconds")

# Feature importance (optional)
importances = rf_model.feature_importances_
plt.barh(features, importances)
plt.title("Feature Importances")
plt.show()


# # SVR Model

# In[5]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.svm import SVR

# Load your dataset
df = pd.read_csv("D:/Downloadss/merged_output.csv")

# Convert timestamp and create time features
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

# Drop columns with too many missing values
df = df[df.columns[df.isnull().mean() < 0.3]]
df.fillna(df.median(numeric_only=True), inplace=True)

# Feature set

# Separate features and target
X = df[features]
y = df[target]

# Scale features (important for SVR)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train SVR with best-known params (from your GridSearch)
svr_model = SVR(C=1000, epsilon=0.5, kernel='rbf', gamma='scale')
svr_model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = svr_model.predict(X_test)
print("✅ SVR (Fixed Parameters) Results:")
print("R² Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

import time

start_time = time.time()
svr_preds = svr_model.predict(X_test)
end_time = time.time()

print(f"Total inference time: {end_time - start_time:.6f} seconds")
print(f"Average per data point: {(end_time - start_time)/len(X_test):.8f} seconds")

print(df[features + [target]].corr()["safe_score"].sort_values(ascending=False))



# # XGB Model

# In[6]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

# Load dataset
df = pd.read_csv("D:/Downloadss/merged_output.csv")

# Convert timestamp and create time features
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df.dropna(subset=['timestamp'], inplace=True)
df['hour'] = df['timestamp'].dt.hour
df['dayofweek'] = df['timestamp'].dt.dayofweek

# Select features and target
features = [
    "latitude", "longitude",
    "speed_kmh", "acceleration", "deceleration",
    "acceleration_y", "screen_on", "screen_blocked",
    "hour", "dayofweek"
]
target = "safe_score"

# Drop missing values in selected columns
df = df[features + [target]].dropna()

# Prepare features and target
X = df[features]
y = df[target]

# Standard scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# Train XGBoost Regressor
xgb_model = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.1,
    subsample=0.7,
    colsample_bytree=0.7,
    random_state=42
)
xgb_model.fit(X_train, y_train)

# Evaluate
y_pred = xgb_model.predict(X_test)
print("✅ XGBoost with Time & Location Features")
print("R² Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))

import time

start_time = time.time()
xgb_preds = xgb_model.predict(X_test)
end_time = time.time()

print(f"Total inference time: {end_time - start_time:.6f} seconds")
print(f"Average per data point: {(end_time - start_time)/len(X_test):.8f} seconds")

