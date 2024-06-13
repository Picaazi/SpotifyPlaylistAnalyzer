import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('spotify_playlist.db')
cursor = conn.cursor()

# Get a list of all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print all table names
print("Tables in the database:")
for table in tables:
    print(table[0])

# Print the first 10 rows of each table
for table in tables:
    print(f"\nContent of table {table[0]}:")
    cursor.execute(f"SELECT * FROM {table[0]} LIMIT 10;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Close the connection
conn.close()
