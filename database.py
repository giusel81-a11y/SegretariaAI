import sqlite3

conn = sqlite3.connect("data/database.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT,
created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
