SELECT track_name AS [Track],
       Artists.artist_name AS [Artist],
       Albums.album_name AS [Album],
       round(track_duration_ms * 1.66666667 / 100000,2) AS [Track Duration (min)],
       isrc AS [ISRC],
       DATETIME(Playlist.added_at) AS [Added Time]
FROM Tracks
JOIN TrackArtists
	ON	 TrackArtists.track_uri = Tracks.track_uri
JOIN Artists
	ON Artists.artist_uri = TrackArtists.artist_uri
JOIN Albums
	ON Albums.album_uri = Tracks.album_uri
JOIN Playlist
	ON Playlist.track_uri = Tracks.track_uri
