import sqlite3
import pandas as pd
import logging

# Setup logging
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Connect to the SQLite database
conn = sqlite3.connect("/home/chirag/Downloads/raxel_traker_db_200325.db")
cursor = conn.cursor()

# Get all table names (optional, if you want to list them)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print("Tables:", tables)

# Read data from the SampleTable

for table in tables: 
    table_name = table
    print(f"******************Table**************: {table_name}")
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    # Log the dataframe
    # logger.info(df)

    # Write to CSV
    df.to_csv(f"{table_name}.csv", index=False)
    print(f"Data from {table_name} written to {table_name}.csv")



# Close connection
conn.close()
