SELECT track_name, location_code
FROM  Playlist
JOIN Tracks
	ON Tracks.track_uri = Playlist.track_uri