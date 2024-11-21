import mysql.connector

DATABASE_CONFIG = {
    'user': 'root',
    'password': 'Vishkrish3*',
    'host': 'localhost',
    'database': 'sports_tournament',
}

try:
    print("w")
    conn = mysql.connector.connect(**DATABASE_CONFIG)
    print("Database connected successfully")
    conn.close()
except mysql.connector.Error as err:
    print(f"Connection failed: {err}")
