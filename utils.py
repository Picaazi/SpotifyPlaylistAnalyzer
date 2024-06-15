# utils.py

import pandas as pd
import sqlite3

def fetch_data_from_db(db_name, query):
    """Fetch data from the SQLite database."""
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def fetch_query_from_file(filename):
    """Fetch the SQL query from the file."""
    with open(filename, 'r') as file:
        query = file.read()
    return query

def fetch_data_from_playlist(query, type = 'file'):
    if type == 'file':
        query_input = fetch_query_from_file(query)
        return fetch_data_from_db('spotify_playlist.db', query_input)
    elif type == 'query':
        return fetch_data_from_db('spotify_playlist.db', query)
    else:
        print("Type is not available")
        return -1

def join_dataframes(df1, df2, join_key):
    """Join two dataframes on a specified key."""
    return pd.merge(df1, df2, on=join_key)

def fetch_isrc_data():
    location_code_data = fetch_data_from_db('ISRC_loc.db', "SELECT *  FROM ISRCLocations")

    location_code_playlist_data = fetch_data_from_playlist("country_code_playlist.sql", type='file')
    print(location_code_data)
    print(location_code_playlist_data)

    return join_dataframes(location_code_playlist_data, location_code_data, join_key = "location_code")
