
import sqlite3
import pandas as pd

# Step 1: Load CSV
csv_path = "D:/Downloadss/merged_output.csv"  # Already uploaded
df = pd.read_csv(csv_path)

# Step 2: Connect to your existing SQLite DB
db_path = "D:/Downloadss/raxel_traker_db_200325 (1).db"  # Make sure this path is correct
conn = sqlite3.connect(db_path)

# Step 3: Create or replace table
df.to_sql("merged_output", conn, if_exists="replace", index=False)

conn.close()
print("✅ 'merged_output' table created in data.sqlite successfully!")
