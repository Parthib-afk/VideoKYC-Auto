import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kyc_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    id_number TEXT,
    verification_status TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")