import mysql.connector

try:
    conn = mysql.connector.connect(
        host="192.168.10.41",       # Server IP (not localhost)
        user="fleet",
        password="fleetpass",
        database="accurate_tracking_db",
        port=3306
    )

    if conn.is_connected():
        print("✅ Connected to MySQL server")
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print(f"Current database: {db_name}")

        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tables in database:")
        for t in tables:
            print(f" - {t[0]}")

        cursor.close()
        conn.close()

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")