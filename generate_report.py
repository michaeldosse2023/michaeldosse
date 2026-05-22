import sqlite3

# Connect to the database
conn = sqlite3.connect('moodle_analytics.db')
cursor = conn.cursor()

# Ask the database to list all of its actual table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("\n🔍 --- ACTUAL TABLES FOUND IN DATABASE --- 🔍")
if not tables:
    print("The database is completely empty! We are likely looking at a blank auto-created file.")
else:
    for t in tables:
        print(f"-> {t[0]}")

conn.close()