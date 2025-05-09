import sqlite3

# ✅ Define Database File Path
DB_FILE = r"Data/log_analytics.db"

# ✅ Create a Singleton Connection to SQLite
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
