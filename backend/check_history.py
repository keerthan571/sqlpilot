import sqlite3

conn = sqlite3.connect("sqlpilot_history.db")

tables = conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""").fetchall()

print("TABLES:", tables)

conn.close()