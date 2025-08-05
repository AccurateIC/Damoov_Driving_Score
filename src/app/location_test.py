
"""import sqlite3
import pandas as pd
from geopy.geocoders import Nominatim

# === Step 1: Connect to your .db file ===
conn = sqlite3.connect("D:/Downloadss/New_db/Db.db")  # replace with your filename
cursor = conn.cursor()

# === Step 2: Load data from table ===
# Replace 'your_table_name' with the actual table name from your DB
df = pd.read_sql_query("SELECT * FROM SampleTable", conn)

# === Step 3: Prepare timestamp column ===
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # adjust unit if needed
df = df.sort_values(by='timestamp')

# === Step 4: Reverse Geocoding ===
geolocator = Nominatim(user_agent="trip-location-tester")

def reverse_geocode(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='en', timeout=10)
        return location.address if location else "Unknown location"
    except Exception as e:
        return f"Error: {e}"

# === Step 5: Test for one unique_id ===
test_unique_id = 1360458022  # replace or loop as needed
trip_data = df[df['unique_id'] == test_unique_id]

if trip_data.empty:
    print("Trip not found.")
else:
    start_row = trip_data.iloc[0]
    end_row = trip_data.iloc[-1]

    start_lat, start_lon = start_row['latitude'], start_row['longitude']
    end_lat, end_lon = end_row['latitude'], end_row['longitude']

    from_location = reverse_geocode(start_lat, start_lon)
    to_location = reverse_geocode(end_lat, end_lon)

    print(f"Unique ID: {test_unique_id}")
    print(f"From: ({start_lat}, {start_lon}) → {from_location}")
    print(f"To:   ({end_lat}, {end_lon}) → {to_location}")

# Optional: close connection
conn.close()
"""

import sqlite3
import pandas as pd
from geopy.geocoders import Nominatim

# === Step 1: Setup ===
test_unique_id = 309126682
conn = sqlite3.connect("D:/Downloadss/New_db/db.db")

# === Step 2: Query with JOIN ===
query = """
SELECT 
    s.UNIQUE_ID,
    s.device_id AS start_device,
    s.latitude AS start_latitude,
    s.longitude AS start_longitude,
    s.timeStart AS start_time,
    e.device_id AS end_device,
    e.latitude AS end_latitude,
    e.longitude AS end_longitude,
    e.timeStart AS end_time
FROM EventsStartPointTable s
LEFT JOIN EventsStopPointTable e
    ON s.UNIQUE_ID = e.UNIQUE_ID
WHERE s.UNIQUE_ID = ?
"""

df = pd.read_sql_query(query, conn, params=(test_unique_id,))
conn.close()

# === Step 3: Geocode if data exists ===
if df.empty:
    print("❌ Trip not found.")
else:
    row = df.iloc[0]
    geolocator = Nominatim(user_agent="trip-location-tester")

    def reverse_geocode(lat, lon):
        try:
            location = geolocator.reverse((lat, lon), language='en', timeout=10)
            return location.address if location else "Unknown location"
        except Exception as e:
            return f"Error: {e}"

    start_lat, start_lon = row['start_latitude'], row['start_longitude']
    end_lat, end_lon = row['end_latitude'], row['end_longitude']

    from_location = reverse_geocode(start_lat, start_lon)
    to_location = reverse_geocode(end_lat, end_lon)

    print(f"Unique ID: {test_unique_id}")
    print(f"From: ({start_lat}, {start_lon}) → {from_location}")
    print(f"To:   ({end_lat}, {end_lon}) → {to_location}")
