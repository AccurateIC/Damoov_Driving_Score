

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from scipy.stats import ks_2samp, chi2_contingency

# --- SETTINGS ---
#DB_PATH = "D:/Downloadss/result/data.sqlite"  # Update with your actual path if needed
TABLE_NAME = "merged_output"

import yaml

def load_config(path="config.yaml"):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()
SQLITE_PATH = config['database']['sqlite_path']

SELECTED_COLS = [
    "latitude", "longitude", "speed_kmh", "acceleration", "deceleration",
    "acceleration_y", "screen_on", "screen_blocked", "safe_score"
]
BASELINE_PATH = "baseline_stats.json"

def main():
    # --- LOAD DATA ---
    conn = sqlite3.connect(SQLITE_PATH)
    df = pd.read_sql_query(f"SELECT {', '.join(SELECTED_COLS)} FROM {TABLE_NAME}", conn)
    conn.close()

    # --- CONVERT TO NUMERIC ---
    df = df.apply(pd.to_numeric, errors='coerce')

    # --- BASIC STATS & MISSING VALUES ---
    print("📊 Basic Summary Statistics:")
    print(df.describe())

    print("\n❗ Missing Values:")
    print(df.isnull().sum())

    # --- PLOT DISTRIBUTIONS ---
    for col in SELECTED_COLS:
        plt.figure(figsize=(6, 3))
        sns.histplot(df[col], kde=True, bins=30, color="skyblue")
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()

    # --- ENHANCED EDA ---
    # 1] Boxplots for continuous features
    subset_cols = ["speed_kmh", "acceleration", "deceleration", "acceleration_y", "safe_score"]
    plt.figure(figsize=(12, 6))
    df[subset_cols].boxplot()
    plt.title("Boxplots of Continuous Features")
    plt.tight_layout()
    plt.show()

    # 2️] Correlation Matrix Heatmap
    corr_matrix = df.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

    # 3️] Pairwise Scatter Plots
    sns.pairplot(df[subset_cols].dropna())
    plt.suptitle("Pairwise Scatter Plots of Key Variables", y=1.02)
    plt.show()

    # 4️] Countplots for binary features
    for col in ["screen_on", "screen_blocked"]:
        plt.figure(figsize=(4, 3))
        sns.countplot(data=df, x=col, palette="Set2")
        plt.title(f"Countplot of {col}")
        plt.tight_layout()
        plt.show()

    # --- CREATE BASELINE PROFILE FOR DRIFT DETECTION ---
    baseline = {}
    for col in SELECTED_COLS:
        baseline[col] = {
            "mean": df[col].mean(),
            "std": df[col].std(),
            "min": df[col].min(),
            "max": df[col].max(),
            "median": df[col].median(),
            "missing": int(df[col].isnull().sum()),
            "non_missing": int(df[col].notnull().sum())
        }

    # Save baseline to JSON
    with open(BASELINE_PATH, "w") as f:
        json.dump(baseline, f, indent=2)

    print(f"\n✅ Baseline saved to '{BASELINE_PATH}'")

    # --- OPTIONAL: DRIFT CHECK ON FUTURE DATA ---
    # Example usage for future data drift check:
    # future_df = pd.read_csv("future_data.csv")  # Load future data
    # ks_stat, p_value = ks_2samp(df['speed_kmh'].dropna(), future_df['speed_kmh'].dropna())
    # print(f"KS-test p-value for speed_kmh: {p_value}")

    # --- FINAL SUMMARY ---
    print("\n🔍 Final Dataset Shape:", df.shape)
    print("\n🔍 Final Missing Value Summary:")
    print(df.isnull().sum())

if __name__ == "__main__":
    main()
