
# distance_utils.py

import pandas as pd
from math import radians, sin, cos, acos

def spherical_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return R * acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon2 - lon1))

def calculate_trip_distance_from_points(df: pd.DataFrame) -> float:
    """
    Calculate trip distance from GPS points for single trip dataframe.
    """
    df = df.sort_values('timestamp')
    total_distance = 0.0

    for i in range(1, len(df)):
        lat1, lon1 = df.iloc[i-1]['latitude'], df.iloc[i-1]['longitude']
        lat2, lon2 = df.iloc[i]['latitude'], df.iloc[i]['longitude']
        total_distance += spherical_distance(lat1, lon1, lat2, lon2)

    return total_distance

def calculate_trip_distances(start_df, stop_df):
    """
    This is your original DB based calculation for full pipelines.
    """
    start_df = start_df.rename(columns={'latitude': 'start_lat', 'longitude': 'start_lon'})
    stop_df = stop_df.rename(columns={'latitude': 'end_lat', 'longitude': 'end_lon'})

    start_min = start_df.groupby("UNIQUE_ID")["ID"].idxmin()
    stop_max = stop_df.groupby("UNIQUE_ID")["ID"].idxmax()

    start_points = start_df.loc[start_min].copy()
    end_points = stop_df.loc[stop_max].copy()

    merged = pd.merge(start_points, end_points[['UNIQUE_ID', 'end_lat', 'end_lon']], on='UNIQUE_ID')

    merged["distance_km"] = merged.apply(
        lambda row: spherical_distance(row["start_lat"], row["start_lon"], row["end_lat"], row["end_lon"]), axis=1
    )
    return merged[["UNIQUE_ID", "distance_km"]]
