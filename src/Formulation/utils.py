
import pandas as pd
import yaml

def load_config(path="D:/Downloadss/config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_csv_with_timestamp(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df

def finalize_event(current_event, events, timestamp_col, min_duration, value_fields):
    if not current_event:
        return
    df = pd.DataFrame(current_event)
    duration = (df[timestamp_col].iloc[-1] - df[timestamp_col].iloc[0]).total_seconds()
    if duration >= min_duration:
        event_summary = {
            "start_time": df[timestamp_col].iloc[0],
            "end_time": df[timestamp_col].iloc[-1],
            "duration_s": duration,
            "num_points": len(df)
        }
        for key, col in value_fields.items():
            if 'max' in key:
                event_summary[key] = df[col].abs().max() if 'lateral' in key else df[col].max()
            elif 'avg' in key:
                event_summary[key] = df[col].mean()
        events.append(event_summary)
