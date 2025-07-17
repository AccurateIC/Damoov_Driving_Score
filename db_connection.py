
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

import mysql.connector
import pandas as pd

# Replace with your actual credentials
DB_CONFIG = {
    "username": "fleet",
    "password": "fleetpass",
    "host": "192.68.10.41",      # MySQL host
    "port": 5555,                # Your MySQL port
    "database": "tracking_db"
}

def load_table(table_name):
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['username'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port']
        )

        print(f"✅ Connected to DB: {DB_CONFIG['database']}")
        print(f"📥 Fetching table: {table_name} ...")

        query = f"SELECT * FROM {table_name} LIMIT 5"
        df = pd.read_sql(query, con=conn)

        print(f"✅ Retrieved {len(df)} rows from '{table_name}'\n")
        print(df)

        conn.close()
        return df

    except Exception as e:
        print(f"❌ Failed to load table '{table_name}': {e}")
        return pd.DataFrame()

# 🔍 Test with a known table
if __name__ == "__main__":
    load_table("SampleTable")
