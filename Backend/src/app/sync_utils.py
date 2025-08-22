
# src/app/sync_utils.py
from sqlalchemy import text

def sync_old_to_new(engine, config):
    old_table = config['database']['old_table']
    new_table = config['database']['main_table']

    # Explicitly list all columns you want to sync
    columns = [
        "ID", "latitude", "longitude", "timestamp", "tick_timestamp", "speed_kmh", "midSpeed",
        "course", "height", "acceleration", "deceleration", "lateral", "yaw", "total_meters",
        "established_indexA", "established_indexB", "start_date", "end_date", "unique_id",
        "number", "device_id", "user_id", "acceleration_x", "acceleration_y", "acceleration_z",
        "gyroscope_x", "gyroscope_y", "gyroscope_z",
        "acceleration_x_original", "acceleration_y_original", "acceleration_z_original",
        "gyroscope_x_original", "gyroscope_y_original", "gyroscope_z_original",
        "accuracy", "screen_on", "screen_blocked", "vehicle_indicators", "quantile"
    ]

    # Backtick + alias prefix for SELECT part
    insert_cols = ", ".join([f"`{c}`" for c in columns])
    select_cols = ", ".join([
       "FROM_UNIXTIME(o.`timestamp`) AS `timestamp`" if c == "timestamp" else f"o.`{c}`"
       for c in columns
])

    sql = f"""
        INSERT INTO {new_table} ({insert_cols})
        SELECT {select_cols}
        FROM {old_table} o
        LEFT JOIN {new_table} n ON o.unique_id = n.unique_id
        WHERE n.unique_id IS NULL
    """

    with engine.begin() as conn:
        conn.execute(text(sql))
