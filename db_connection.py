
"""from sqlalchemy import create_engine
import pandas as pd

# Replace with actual credentials
DB_CONFIG = {
    "username": "fleet",
    "password": "fleetpass",
    "host": "http://192.68.10.41",          # e.g., "db.myserver.com" or "127.0.0.1"
    "port": 5555,                 # default PostgreSQL port
    "database": "tracking_db"
}

def get_engine():
    uri = f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(uri)

def load_table(table_name):
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    return df
"""

from sqlalchemy import create_engine
import pandas as pd

# Replace with your actual credentials
DB_CONFIG = {
    "username": "fleet",
    "password": "fleetpass",
    "host": "192.68.10.41",           # e.g., "db.example.com"
    "port": 5555,                  # PostgreSQL default port
    "database": "tracking_db"
}

port = int(DB_CONFIG['port'])
def get_engine():
    uri = f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{port}/{DB_CONFIG['database']}"
    return create_engine(uri)

def load_table(table_name):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            print(f"✅ Connected to DB: {DB_CONFIG['database']}")
            print(f"📥 Fetching table: {table_name} ...")
            df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 5", conn)  # just first 5 rows
            print(f"✅ Retrieved {len(df)} rows from '{table_name}'\n")
            print(df)
            return df
    except Exception as e:
        print(f"❌ Failed to load table '{table_name}': {e}")
        return pd.DataFrame()

# 🔍 Test with a known table
if __name__ == "__main__":
    load_table("SampleTable")  # change table name as needed
