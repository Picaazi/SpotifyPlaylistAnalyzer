import pandas as pd
import sqlite3


# Connect to SQLite database
conn = sqlite3.connect('spotify_playlist.db')
cursor = conn.cursor()

# Update database for isrc
with open('TableCleaning.sql', 'r') as sql_file:
    sql_script = sql_file.read()
cursor.executescript(sql_script)
conn.commit()
conn.close()