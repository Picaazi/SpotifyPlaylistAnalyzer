SELECT count(DISTINCT(Tracks.isrc)) + count(*) - count(Tracks.isrc) AS [Total Tracks],
	sum(Tracks.explicit) AS [Explicit Tracks],
	sum(Tracks.track_duration_ms) * 1.66666667 / 100000 AS [Track Duration (min)],
	count(DISTINCT(Artists.artist_name) )AS [Total Artists],
	count(DISTINCT(Albums.album_name) ) AS [Total Albums]
FROM Tracks
JOIN TrackArtists
	ON TrackArtists.track_uri = Tracks.track_uri
JOIN Artists
	ON Artists.artist_uri = TrackArtists.artist_uri
JOIN Albums
	ON Tracks.album_uri = Albums.album_uri