import pandas as pd

df = pd.read_csv("driving_score_dataset.csv")

df["timeStart"] = pd.to_datetime(df["timeStart"], unit='ms') 

df = df.sort_values(by=["UNIQUE_ID", "timeStart"]) 

df["speed_diff"] = df.groupby("UNIQUE_ID")["max_speed"].diff()

hb_threshold = -3.2  
ha_threshold = 3
hc_threshold = 4.2 

df["harsh_braking"] = (df["speed_diff"] < hb_threshold).astype(int)
df["harsh_acceleration"] = (df["speed_diff"] > ha_threshold).astype(int)
df["harsh_cornering"] = (df["accelerationLateral"].abs() > hc_threshold).astype(int)

hb_count = df["harsh_braking"].sum()
ha_count = df["harsh_acceleration"].sum()
hc_count = df["harsh_cornering"].sum()

wb = 5
wa= 3
wc= 2

def calculate_score(group):
    total_events = len(group)
    
    hb_severity = group["harsh_braking"].sum() / total_events
    ha_severity = group["harsh_acceleration"].sum() / total_events
    hc_severity = group["harsh_cornering"].sum() / total_events

    score = 100 - (wb * hb_severity) - (wa * ha_severity) - (wc * hc_severity)
    return round(score, 2)

driving_scores = df.groupby("UNIQUE_ID").apply(calculate_score).reset_index()
driving_scores.columns = ["UNIQUE_ID", "Driving_Score"]

print(driving_scores)