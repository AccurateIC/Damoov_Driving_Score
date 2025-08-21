
import pandas as pd
import sqlite3
import os

# Define your file paths
db_path = "D:/Downloadss/raxel_traker_db_200325 (1).db"
csv_path = "D:/Downloadss/Cleaned_SampleTable.csv"
table_name = "Cleaned_SampleTable"  # Desired table name in SQLite DB

# Check if files exist
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database file not found: {db_path}")
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

# Read CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Connect to SQLite database and write to table
with sqlite3.connect(db_path) as conn:
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"✅ Table '{table_name}' added to database successfully!")
