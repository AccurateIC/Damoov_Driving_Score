
import pandas as pd
from sqlalchemy import text
from functools import lru_cache
from .utils.db import setup_database, CONFIG
from .utils.helpers import normalize_timestamp, optimize_columns, get_time_range
from .utils.helpers import normalize_timestamp, optimize_columns, get_time_range

db_cfg = CONFIG.get("database", {})

main_table  = db_cfg.get("main_table")
start_table = db_cfg.get("start_table")
stop_table  = db_cfg.get("stop_table")

main_table  = db_cfg.get("main_table")
start_table = db_cfg.get("start_table")
stop_table  = db_cfg.get("stop_table")
old_table   = db_cfg.get("old_table", "")
map_table   = db_cfg.get("map_table")


# Always fetch a valid engine just before querying
def get_engine():
    return setup_database()
# ---------- core loaders ----------

def load_main_table() -> pd.DataFrame:
    """Load the main table with normalization & light optimization."""
    engine = get_engine()
    df = pd.read_sql(f"SELECT * FROM {main_table}", con=engine)
    df = normalize_timestamp(df)
    df = optimize_columns(df)
    return df

def load_df(required_cols=None) -> pd.DataFrame:
    """
    Load only the requested columns from the main table.
    Always deduplicates columns to avoid pandas errors.
    """
    engine = get_engine()

    if required_cols:
        if isinstance(required_cols, (list, tuple, set)):
            # Deduplicate & preserve order
            required_cols = list(dict.fromkeys(required_cols))
            cols = ", ".join(required_cols)
        else:
            cols = str(required_cols)
        sql = text(f"SELECT {cols} FROM {main_table}")
    else:
        sql = text(f"SELECT * FROM {main_table}")

    df = pd.read_sql(sql, con=engine)

    # Drop duplicate column names if any slipped in
    df = df.loc[:, ~df.columns.duplicated()]

    # Normalize timestamp if present
    if "timestamp" in df.columns:
        try:
            df = normalize_timestamp(df)
        except Exception as e:
            print(f"[WARN] Timestamp normalization failed: {e}")
            # fallback: just keep it raw
            pass

    return df

@lru_cache(maxsize=1)
def load_main_table_cached():
    """Simple cache for repeated reads (no TTL, but cuts repeated hits)."""
    return load_main_table()

def get_safe_driving_rows() -> pd.DataFrame:
    engine = get_engine()
    df = pd.read_sql(
        text(f"""
            SELECT unique_id, device_id, trip_distance_used, speed_kmh,
                   acc_score, dec_score, cor_score, spd_score, phone_score,
                   safe_score, timestamp
            FROM {main_table}
            WHERE safe_score IS NOT NULL
        """),
        con=engine
    )
    return normalize_timestamp(df)

def get_eco_driving_rows() -> pd.DataFrame:
    engine = get_engine()
    df = pd.read_sql(
        text(f"""
            SELECT unique_id, eco_score, brake_score, tire_score, fuel_score, timestamp
            FROM {main_table}
            WHERE eco_score IS NOT NULL
        """),
        con=engine
    )
    return normalize_timestamp(df)

def get_trip_points(unique_id: int) -> pd.DataFrame:
    engine = get_engine()
    sql = text(f"""
        SELECT s.UNIQUE_ID,
               s.latitude  AS start_latitude,
               s.longitude AS start_longitude,
               s.timeStart AS start_time,
               e.latitude  AS end_latitude,
               e.longitude AS end_longitude,
               e.timeStart AS end_time
        FROM {start_table} s
        LEFT JOIN {stop_table} e ON s.UNIQUE_ID = e.UNIQUE_ID
        WHERE s.UNIQUE_ID = :uid
    """)
    return pd.read_sql(sql, con=engine, params={"uid": unique_id})

def get_trip_points_batch(unique_ids: list[int]) -> pd.DataFrame:
    """
    Fetch start and end points for multiple trips in one query.
    Much faster than calling get_trip_points() inside a loop.
    """
    if not unique_ids:
        return pd.DataFrame()

    engine = get_engine()
    sql = text(f"""
        SELECT s.UNIQUE_ID,
               s.latitude  AS start_latitude,
               s.longitude AS start_longitude,
               s.timeStart AS start_time,
               e.latitude  AS end_latitude,
               e.longitude AS end_longitude,
               e.timeStart AS end_time
        FROM {start_table} s
        LEFT JOIN {stop_table} e 
               ON s.UNIQUE_ID = e.UNIQUE_ID
        WHERE s.UNIQUE_ID IN :uids
    """)
    
    return pd.read_sql(sql, con=engine, params={"uids": tuple(unique_ids)})

def get_all_trip_locations(unique_id: int) -> pd.DataFrame:
    engine = get_engine()
    sql = text(f"""
        SELECT latitude, longitude, timeStart AS timestamp
        FROM {start_table} WHERE UNIQUE_ID = :uid
        UNION ALL
        SELECT latitude, longitude, timeStart AS timestamp
        FROM {stop_table} WHERE UNIQUE_ID = :uid
    """)
    df = pd.read_sql(sql, con=engine, params={"uid": unique_id})
    return normalize_timestamp(df).sort_values("timestamp")

def get_trip_map(track_id: int) -> pd.DataFrame:
    engine = get_engine()
    sql = text(f"""
        SELECT latitude, longitude, point_date AS timestamp
        FROM {map_table} WHERE track_id = :tid
    """)
    df = pd.read_sql(sql, con=engine, params={"tid": track_id})
    return normalize_timestamp(df).sort_values("timestamp")

def get_devices_table() -> pd.DataFrame:
    """Devices lookup used by performance_summary."""
    engine = get_engine()
    try:
        return pd.read_sql(text("SELECT device_id, user_id FROM devices"), con=engine)
    except Exception:
        # Fallback empty frame if 'devices' missing
        return pd.DataFrame(columns=["device_id", "user_id"])
    
def get_safety_graph_data() -> pd.DataFrame:
    """
    Load only the columns required for /safety_graph_trend
    instead of SELECT * which is very slow.
    """
    engine = get_engine()
    sql = text(f"""
        SELECT timestamp,
               acc_score,
               dec_score,
               cor_score,
               spd_score,
               phone_score,
               safe_score
        FROM {main_table}
        WHERE safe_score IS NOT NULL
    """)
    df = pd.read_sql(sql, con=engine)
    return normalize_timestamp(df)


def get_mileage_graph_data() -> pd.DataFrame:
    """
    Load only the columns required for /mileage_daily
    instead of SELECT * which is very slow.
    """
    engine = get_engine()
    sql = text(f"""
        SELECT timestamp,
               unique_id,
               trip_distance_used
        FROM newSampleTable
        WHERE trip_distance_used <= 500
    """)
    df = pd.read_sql(sql, con=engine)
    return normalize_timestamp(df)



def get_mileage_graph_data() -> pd.DataFrame:
    """
    Load only the columns required for /mileage_daily
    instead of SELECT * which is very slow.
    """
    engine = get_engine()
    sql = text(f"""
        SELECT timestamp,
               unique_id,
               trip_distance_used
        FROM newSampleTable
        WHERE trip_distance_used <= 500
    """)
    df = pd.read_sql(sql, con=engine)
    return normalize_timestamp(df)


def get_performance_data():
    """
    Load only the necessary columns for performance summary.
    """
    engine = get_engine()
    sql = text(f"""
        SELECT unique_id, device_id, timestamp,
               acc_score, dec_score, cor_score, spd_score, phone_score, safe_score
        FROM {main_table}
        WHERE safe_score IS NOT NULL
    """)
    df = pd.read_sql(sql, con=engine)
    return normalize_timestamp(df)

def get_users_with_summary() -> pd.DataFrame:
    """
    Returns users with trip_count, safety_score, and status.
    Joins trips (main_table) with users table.
    """
    engine = get_engine()
    sql = text(f"""
        SELECT u.id AS user_id,
               u.name AS name,
               COUNT(DISTINCT m.unique_id) AS trip_count,
               AVG(m.safe_score) AS safety_score,
               MAX(m.timestamp) AS timestamp
        FROM users u
        LEFT JOIN {main_table} m ON u.id = m.user_id AND m.safe_score IS NOT NULL
        GROUP BY u.id, u.name
    """)
    df = pd.read_sql(sql, con=engine)
    df = df.where(pd.notnull(df), None)
    # calculate status (1 = active if any trips, else 0)
    df["status"] = df["trip_count"].apply(lambda x: 1 if x > 0 else 0)

    # round safety_score safely
    df["safety_score"] = df["safety_score"].fillna(0).round(2)

    return df

def get_trips_with_users() -> pd.DataFrame:
    """
    Returns trips (distance < 1 km) joined with users table for names.
    """
    engine = get_engine()
    sql = text(f"""
                 SELECT m.unique_id,
                        MIN(m.timestamp) AS start_time,
                        MAX(m.timestamp) AS end_time,
                        MAX(m.trip_distance_used) AS trip_distance_used,
                        m.user_id,
                        u.name
                FROM {main_table} m
                LEFT JOIN users u ON u.id = m.user_id
                    AND m.trip_distance_used > 0.1
                GROUP BY m.unique_id, m.user_id, u.name


    """)
    df = pd.read_sql(sql, con=engine)
    print("Row count fetched:", len(df))  # Debug row count
    print(df.head(5))                     # Debug preview

    # Normalize timestamps
    df = normalize_timestamp(df)
    return df


