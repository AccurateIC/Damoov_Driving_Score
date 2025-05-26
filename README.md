

```markdown
# MLP-Based Driving Safety Score Model

This module provides a machine learning pipeline for predicting driving safety scores using an MLP (Multi-Layer Perceptron) regressor. It is a self-contained feature within the Damoov_Diving_Score repository.

---


---

## 🧠 Features

- Cleans and preprocesses telematics data
- Extracts time, acceleration, and behavioral features
- Trains a robust `MLPRegressor` using scikit-learn
- Evaluates the model using RMSE and R² metrics
- Supports single-row inference with time profiling
- Fully configurable via `config.yaml`

---

## ⚙️ Configuration (`config.yaml`)

```yaml
data_path: "merged_output.csv"

model:
  hidden_layer_sizes: [100, 50]
  activation: relu
  solver: adam
  max_iter: 200
  random_state: 42

train_test_split:
  test_size: 0.2
  random_state: 42

features:
  numeric:
    - latitude
    - longitude
    - speed_kmh
    - midSpeed
    - total_meters
    - acceleration
    - deceleration
    - acceleration_x_original
    - acceleration_y_original
    - acceleration_z_original
    - accel_mag
    - jerk
    - hard_brake
    - hard_accel
    - screen_on
    - screen_blocked
````

---

## 🚀 How to Run

```bash
cd mlp_score_model
python driving_safety_score_model.py
```

This will:

* Load and clean the data
* Train the MLP model
* Evaluate it
* Perform a timed prediction on a single sample row

---

## 🧪 Example Output

```
🚀 Starting full pipeline...
✅ Training completed in 2.12 seconds
Test RMSE: 2.85
Test R²:   0.89
Predicted safe_score: 82.37
Inference time: 1.17 ms
✅ Total execution time: 4.23 seconds
```

---

## 📦 Dependencies

You can install all required libraries with:

```bash
pip install pandas numpy scikit-learn pyyaml
```

---

## 🧩 Integration

To integrate into other systems:

```python
from driving_safety_score_model import DrivingSafetyScoreModel

model = DrivingSafetyScoreModel("config.yaml")
model.run_all()
```

You can also use `predict_single_row()` for real-time inference.

---

## 📄 License

This feature inherits the license of the main Damoov\_Diving\_Score repository.

---


