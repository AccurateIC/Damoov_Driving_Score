
***Damoov_Diving_Score***
=======

```markdown
# 🚘 Driving Safety Score Prediction

This module provides two machine learning pipelines for predicting **driver safety scores** from telematics data using:

- 🧠 `MLPRegressor` (Scikit-learn)
- ⚙️ `Keras Sequential Neural Network` (TensorFlow)

These models are designed to process numerical driving data like speed, acceleration, braking, and event-derived features (e.g., jerk, hard braking) and produce a **numerical safety score** between 5–100.

---

## 📁 Project Structure

```

mlp\_score\_model/
├── config/
│   └── config.yaml              # Centralized configuration
├── csv/
│   └── merged\_output.csv       # Input driving dataset
├── src/
│   ├── MLP-driving-score.py    # MLPRegressor pipeline
│   └── NN-driving-score.py     # Keras-based NN pipeline
└── README.md

````

---

## 🧠 Models Overview

| Model               | Framework       | Description                                      |
|--------------------|------------------|--------------------------------------------------|
| `MLPRegressor`      | Scikit-learn     | Lightweight multi-layer perceptron for tabular data |
| `Keras Neural Net`  | TensorFlow (Keras) | Deep configurable neural network with dropout, early stopping |

---

## ⚙️ Configuration (`config/config.yaml`)

```yaml
data_path: "csv/merged_output.csv"
target: "safe_score"

train_test_split:
  test_size: 0.2
  random_state: 42

nn_model:
  layer1: 128
  layer2: 64
  dropout1: 0.2
  dropout2: 0.1
  optimizer: adam
  epochs: 50
  batch_size: 32
  patience: 5
````

> ✅ Shared config enables consistent training and experimentation across models.

---

## 🚀 How to Run

### ▶️ Run MLPRegressor Pipeline

```bash
python src/MLP-driving-score.py
```

### ▶️ Run Keras Neural Network Pipeline

```bash
python src/NN-driving-score.py
```

Each pipeline:

* Loads the dataset
* Cleans and scales input
* Trains the model
* Evaluates with `MAE`, `R²`
* Performs real-time single-row inference with timing


---

## 📦 Installation

Install dependencies using:

```bash
pip install pandas numpy scikit-learn tensorflow pyyaml
```

Or use:

```bash
pip install -r requirements.txt  # if provided
```

---

## 📌 Model Comparison Summary

| Feature                 | MLPRegressor | Keras NN           |
| ----------------------- | ------------ | ------------------ |
| Library                 | scikit-learn | TensorFlow         |
| Deep customization      | ❌            | ✅                  |
| Dropout & EarlyStopping | ❌            | ✅                  |
| Real-time inference     | ✅            | ✅                  |
| Ideal for tabular data  | ✅            | ✅                  |
| Performance             | Medium       | High (with tuning) |

---

## 📈 Future Enhancements

* ⏳ Add LSTM for time-sequential driving sessions
* 🔍 Feature importance and explainability (SHAP, LIME)
* 💾 Save/load models (`.pkl` or `.h5`)
* 🌐 API endpoint for real-time score predictions (FastAPI/Streamlit)

---

## 🤝 Contributing

Pull requests, suggestions, and improvements are welcome! Please fork the repo and submit a PR under a descriptive branch name.



