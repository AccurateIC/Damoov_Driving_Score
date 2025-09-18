
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
    Returns users with trip_count, safety_score, and last trip timestamp.
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
        LEFT JOIN {main_table} m 
               ON u.id = m.user_id 
              AND m.safe_score IS NOT NULL
        GROUP BY u.id, u.name
    """)
    df = pd.read_sql(sql, con=engine)

    df = df.where(pd.notnull(df), None)
    df["status"] = df.apply(lambda row: 1 if row["trip_count"] and row["trip_count"] > 0 else 0, axis=1)
    df["safety_score"] = df["safety_score"].fillna(0).round(2)

    return df

#Trips Page table
def get_trips_with_users() -> pd.DataFrame:
    """
    Returns trips (distance > 0.1 km) joined with users table for names.
    Ensures correct start_time and end_time are picked from trip events.
    """
    engine = get_engine()
    sql = text(f"""
        WITH trip_bounds AS (
            SELECT
                m.unique_id,
                m.user_id,
                u.name,
                m.trip_distance_used,
                m.timestamp,
                ROW_NUMBER() OVER (PARTITION BY m.unique_id ORDER BY m.timestamp ASC)  AS rn_start,
                ROW_NUMBER() OVER (PARTITION BY m.unique_id ORDER BY m.timestamp DESC) AS rn_end
            FROM {main_table} m
            LEFT JOIN users u ON u.id = m.user_id
            WHERE m.trip_distance_used > 0.1
        )
        SELECT
            t.unique_id,
            MIN(CASE WHEN rn_start = 1 THEN t.timestamp END) AS start_time,
            MIN(CASE WHEN rn_end = 1 THEN t.timestamp END)   AS end_time,
            MAX(t.trip_distance_used) AS trip_distance_used,
            t.user_id,
            t.name
        FROM trip_bounds t
        GROUP BY t.unique_id, t.user_id, t.name;
    """)
    
    df = pd.read_sql(sql, con=engine)
    print("Row count fetched:", len(df))  # Debug row count
    print(df.head(5))                     # Debug preview

    # Normalize timestamps (convert Unix → human-readable)
    df = normalize_timestamp(df)
    return df

# User's Page trip section as per user id and filter
def fetch_all_trips(user_id: int, start=None, required_cols=None) -> pd.DataFrame:
    """
    Fetch trips dataframe with required columns from main table,
    but filter early in SQL for performance.
    """
    engine = get_engine()
    cols = ", ".join(required_cols) if required_cols else "*"

    query = f"SELECT {cols} FROM {main_table} WHERE user_id = :user_id"
    params = {"user_id": user_id}

    if start:
        query += " AND timestamp >= :start"
        params["start"] = start

    return pd.read_sql(text(query), con=engine, params=params)


# join with users table for name
def get_top_safe_drivers(limit: int = 3) -> pd.DataFrame:
    """
    Fetch top N safe drivers by average score per driver.
    """
    engine = get_engine()
    sql = text("""
        SELECT u.name,
               d.device_id,
               AVG(n.safe_score) AS avg_score,
               SUM(n.trip_distance_used) AS total_distance
        FROM newSampleTable n
        JOIN devices d ON n.device_id = d.device_id
        JOIN users u   ON d.user_id = u.id
        WHERE n.safe_score IS NOT NULL
          AND n.safe_score > 0
          AND n.trip_distance_used > 1
          AND n.trip_distance_used <= 500
        GROUP BY u.name, d.device_id
        ORDER BY avg_score DESC
        LIMIT :lim
    """)
    return pd.read_sql(sql, con=engine, params={"lim": limit})


def get_top_aggressive_drivers(limit: int = 3) -> pd.DataFrame:
    """
    Fetch top N aggressive drivers by average score per driver.
    """
    engine = get_engine()
    sql = text("""
        SELECT u.name,
               d.device_id,
               AVG(n.safe_score) AS avg_score,
               SUM(n.trip_distance_used) AS total_distance
        FROM newSampleTable n
        JOIN devices d ON n.device_id = d.device_id
        JOIN users u   ON d.user_id = u.id
        WHERE n.safe_score IS NOT NULL
          AND n.safe_score > 0
          AND n.trip_distance_used > 1
          AND n.trip_distance_used <= 500
        GROUP BY u.name, d.device_id
        ORDER BY avg_score ASC
        LIMIT :lim
    """)
    return pd.read_sql(sql, con=engine, params={"lim": limit})

def get_trip_level_data() -> pd.DataFrame:
    """
    Fetch trip-level data with filtering:
    - safe_score > 0
    - trip_distance_used between 1 and 500
    """
    engine = get_engine()
    sql = text("""
        SELECT 
            n.unique_id,
            d.device_id,
            u.name,
            n.safe_score,
            n.trip_distance_used
        FROM newSampleTable n
        JOIN devices d ON n.device_id = d.device_id
        JOIN users u   ON d.user_id = u.id
        WHERE n.safe_score IS NOT NULL
          AND n.safe_score > 0
          AND n.trip_distance_used > 1
          AND n.trip_distance_used <= 500
    """)
    df = pd.read_sql(sql, con=engine)
    return df

def get_badge_aggregates(user_id: int = None, filter_val: str = "last_1_month") -> tuple[dict, int, str]:
    """
    Returns aggregates (star_rating, speed score), trip count, and user name.
    """
    engine = get_engine()
    now = pd.Timestamp.now()
    start_date = get_time_range(filter_val, now)
    if not start_date:
        start_date = pd.Timestamp.min  # fallback

    sql = f"""
        SELECT
            u.name AS user_name,
            AVG(n.star_rating) AS avg_star,
            AVG(n.spd_score)   AS avg_speed,
            COUNT(DISTINCT n.unique_id) AS trips
        FROM newSampleTable n
        JOIN users u ON u.id = n.user_id
        WHERE n.timestamp >= :start_date
    """

    params = {"start_date": start_date.strftime("%Y-%m-%d")}

    if user_id:
        sql += " AND n.user_id = :user_id"
        params["user_id"] = user_id

    sql += " GROUP BY u.name"

    df = pd.read_sql(text(sql), con=engine, params=params)

    if df.empty:
        # return zeroed stats if user has no trips
        return {"star_rating": 0, "spd_score": 0.0}, 0, None

    row = df.iloc[0]
    agg = {
        "star_rating": row["avg_star"] or 0,
        "spd_score": row["avg_speed"] or 0.0
    }
    trips = int(row["trips"] or 0)
    user_name = row["user_name"]

    return agg, trips, user_name
