import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "anpr_x.db"


def get_connection():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Vehicle table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT UNIQUE NOT NULL,
            manufacturer TEXT,
            model TEXT,
            vehicle_type TEXT,
            owner_name TEXT,
            registration_date TEXT,
            registration_status TEXT
        )
    """)

    # Challan table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS challans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT NOT NULL,
            violation_type TEXT,
            location TEXT,
            violation_date TEXT,
            amount REAL,
            payment_status TEXT
        )
    """)

    # Detection history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT,
            detection_time TEXT,
            detection_confidence REAL,
            ocr_confidence REAL
        )
    """)

    conn.commit()
    conn.close()

    print("ANPR-X DATABASE INITIALIZED SUCCESSFULLY!")


if __name__ == "__main__":
    initialize_database()

def save_detection(registration_number, detection_confidence, ocr_confidence):
    from datetime import datetime

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO detections (
            registration_number,
            detection_time,
            detection_confidence,
            ocr_confidence
        )
        VALUES (?, ?, ?, ?)
    """, (
        registration_number,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        detection_confidence,
        ocr_confidence
    ))

    conn.commit()
    conn.close()