import numpy as np
import pandas as pd
from datetime import timedelta

def get_time_range(filter_val: str, now: pd.Timestamp):
    """Map filter key to start datetime."""
    return {
        "last_1_week":  now - timedelta(weeks=1),
        "last_2_weeks": now - timedelta(weeks=2),
        "last_1_month": now - timedelta(days=30),
        "last_2_months":now - timedelta(days=60),
    }.get(filter_val)

def normalize_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure dataframe has a valid 'timestamp' column as pandas datetime."""
    if df is None or df.empty:
        return df
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    elif "tick_timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["tick_timestamp"], unit="s", errors="coerce")
    else:
        for cand in ("timeStart", "created_at", "point_date"):
            if cand in df.columns:
                df["timestamp"] = pd.to_datetime(df[cand], errors="coerce")
                break
        else:
            df["timestamp"] = pd.NaT
    df = df.dropna(subset=["timestamp"])
    return df

def optimize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lightweight dtype optimization following your original logic."""
    if df is None or df.empty:
        return df
    if "unique_id" in df.columns:
        df["unique_id"] = pd.to_numeric(df["unique_id"], errors="coerce").astype("Int64")
    if "device_id" in df.columns:
        df["device_id"] = df["device_id"].astype("category")
    for col in ["acc_score","dec_score","cor_score","spd_score","phone_score","safe_score",
                "trip_distance_used","speed_kmh","eco_score","brake_score","tire_score","fuel_score"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def to_records_json(df: pd.DataFrame):
    """NaN→None & timestamps→str for JSON responses."""
    if df is None or df.empty:
        return []
    out = df.replace({np.nan: None}).copy()
    for c in out.columns:
        if str(out[c].dtype).startswith("datetime"):
            out[c] = out[c].astype(str)
    return out.to_dict(orient="records")
