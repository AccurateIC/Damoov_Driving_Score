import mysql.connector

try:
    conn = mysql.connector.connect(
        host="192.168.10.41",
        user="fleet",
        password="fleetpass",
        database="accurate_tracking_db",
        port=3306
    )

    if conn.is_connected():
        print("✅ Connected to MySQL server")

        cursor = conn.cursor()

        # Step 1: Create new table with same structure as SampleTable
        cursor.execute("CREATE TABLE IF NOT EXISTS newSampleTable LIKE SampleTable;")

        # Step 2: Copy data from SampleTable into newSampleTable
        cursor.execute("INSERT INTO newSampleTable SELECT * FROM SampleTable;")

        conn.commit()  # Save changes
        print("🎉 Table 'newSampleTable' created and data copied from 'SampleTable'.")

        cursor.close()
        conn.close()

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
