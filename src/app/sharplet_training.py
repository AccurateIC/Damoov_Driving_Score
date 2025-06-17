
import pandas as pd
import numpy as np
import sqlite3
import joblib

from tslearn.shapelets import ShapeletModel
from tslearn.preprocessing import TimeSeriesScalerMinMax
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load data from DB
db_path = "csv/tracking_raw_DB_150525 (2).db"  # Replace
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM SampleTable", conn)
conn.close()

# For demo, assume you have safe_score column (you can modify your labels accordingly)
df = df.dropna(subset=['safe_score'])
df['label'] = df['safe_score'].apply(lambda x: 1 if x >= 80 else 0)

# Prepare timeseries features (e.g. use speed for now)
X = []
y = []

for uid in df['unique_id'].unique():
    temp = df[df['unique_id'] == uid]
    if len(temp) >= 30:  # minimum length
        X.append(temp['speed_kmh'].values)
        y.append(temp['label'].values[0])

# Pad sequences to same length
from tensorflow.keras.preprocessing.sequence import pad_sequences
X_padded = pad_sequences(X, maxlen=100, padding='post', dtype='float32')

# Normalize
scaler = TimeSeriesScalerMinMax()
X_scaled = scaler.fit_transform(X_padded)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build Shapelet Model
n_shapelets_per_size = {10: 5, 20: 5}
shapelet_sizes = n_shapelets_per_size.keys()

shp_clf = ShapeletModel(
    n_shapelets_per_size=n_shapelets_per_size,
    weight_regularizer=.01,
    max_iter=100
)

shp_clf.fit(X_train, y_train)

# Test accuracy
y_pred = shp_clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(shp_clf, "models/shapelet_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
