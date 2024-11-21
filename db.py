# Initialises everything from the database

import mysql.connector
from config import Config

def get_db():
    try:
        print("Trying to connect to the database...")
        db = mysql.connector.connect(user="root", password="vikas*123", host="localhost", database="sports_tournament")
        print("Database connected successfully")
        return db
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise

def close_db(db):
    try:
        if db is not None:
            db.close()
            print("Database connection closed")
    except Exception as e:
        print(f"Error closing database: {e}")
