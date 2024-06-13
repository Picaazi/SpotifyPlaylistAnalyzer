import pandas as pd
import sqlite3

# Load the CSV file
df = pd.read_csv('liked.csv')

# Connect to SQLite database
conn = sqlite3.connect('spotify_playlist.db')
cursor = conn.cursor()

# Create tables by executing the SQL script
with open('Table_normalization.sql', 'r') as sql_file:
    sql_script = sql_file.read()
cursor.executescript(sql_script)
conn.commit()

# Normalize and insert data
tracks = df[['Track URI', 'Track Name', 'Album URI', 'Disc Number', 'Track Number', 'Track Duration (ms)', 'Track Preview URL', 'Explicit', 'Popularity', 'ISRC']].drop_duplicates()
tracks.columns = ['track_uri', 'track_name', 'album_uri', 'disc_number', 'track_number', 'track_duration_ms', 'track_preview_url', 'explicit', 'popularity', 'isrc']
tracks.to_sql('Tracks', conn, if_exists='append', index=False)

albums = df[['Album URI', 'Album Name', 'Album Release Date', 'Album Image URL']].drop_duplicates()
albums.columns = ['album_uri', 'album_name', 'album_release_date', 'album_image_url']
albums.to_sql('Albums', conn, if_exists='append', index=False)

artists = pd.concat([
    df[['Artist URI(s)', 'Artist Name(s)']].rename(columns={'Artist URI(s)': 'artist_uri', 'Artist Name(s)': 'artist_name'}),
    df[['Album Artist URI(s)', 'Album Artist Name(s)']].rename(columns={'Album Artist URI(s)': 'artist_uri', 'Album Artist Name(s)': 'artist_name'})
]).drop_duplicates().explode(['artist_uri', 'artist_name'])
#artists['artist_uri'] = artists['artist_uri'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
#artists['artist_name'] = artists['artist_name'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
artists = artists.explode('artist_uri').explode('artist_name').drop_duplicates()
artists.to_sql('Artists', conn, if_exists='append', index=False)

album_artists = df[['Album URI', 'Album Artist URI(s)']].drop_duplicates()
album_artists.columns = ['album_uri', 'artist_uri']
#album_artists['artist_uri'] = album_artists['artist_uri'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
album_artists = album_artists.explode('artist_uri').drop_duplicates()
album_artists.to_sql('AlbumArtists', conn, if_exists='append', index=False)

track_artists = df[['Track URI', 'Artist URI(s)']].drop_duplicates()
track_artists.columns = ['track_uri', 'artist_uri']
#atrack_artists['artist_uri'] = track_artists['artist_uri'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
track_artists = track_artists.explode('artist_uri').drop_duplicates()
track_artists.to_sql('TrackArtists', conn, if_exists='append', index=False)

playlist = df[['Track URI', 'Added At']].drop_duplicates()
playlist.columns = ['track_uri', 'added_at']
playlist.to_sql('Playlist', conn, if_exists='append', index=False)

conn.commit()

conn.close()
