import sqlite3
from datetime import datetime

DATABASE = "database.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kyc_records(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        verification_time TEXT,

        ocr_text TEXT,

        verification_status TEXT,

        face_distance REAL

    )
    """)

    conn.commit()
    conn.close()


def save_record(ocr_text, verified, distance):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO kyc_records(

        verification_time,

        ocr_text,

        verification_status,

        face_distance

    )

    VALUES (?, ?, ?, ?)

    """, (

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        ocr_text,

        "Verified" if verified else "Not Verified",

        distance

    ))

    conn.commit()

    conn.close()


if __name__ == "__main__":

    create_database()

    print("Database Created Successfully")