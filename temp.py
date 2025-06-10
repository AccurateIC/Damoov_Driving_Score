import sqlite3

# Set your DB path here
db_path = 'csv/raxel_traker_db_200325 (1).db'  # ← Replace with your actual path

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fetch column info for 'SampleTable'
cursor.execute("PRAGMA table_info(SampleTable);")

columns = cursor.fetchall()

print("Columns in SampleTable:")
for col in columns:
    print(f"- {col[1]} ({col[2]})")

conn.close()
