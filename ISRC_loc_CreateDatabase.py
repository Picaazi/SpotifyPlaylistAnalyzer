import sqlite3
import pandas as pd

# CSV file path
csv_file = 'ISRC_loc.csv'

# SQLite database path
db_file = 'ISRC_loc.db'

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Read CSV file into a pandas DataFrame, skipping the first two rows
df = pd.read_csv(csv_file, skiprows=2)

# Define the table schema
table_schema = '''
CREATE TABLE ISRCLocations (
    country_code TEXT PRIMARY KEY,
    location TEXT
);
'''

# Create the table
cursor.execute(table_schema)
conn.commit()

# Insert data into the table
for index, row in df.iterrows():
    country_code = row['First two Characters of ISRC Prefix']
    location = row['Location']
    print((country_code, location))
    cursor.execute("INSERT INTO ISRCLocations (country_code, location) VALUES (?, ?)", (country_code, location))

conn.commit()

# Close the connection
conn.close()

print(f'Data from {csv_file} (skipping 2 rows) successfully imported into {db_file}.')
