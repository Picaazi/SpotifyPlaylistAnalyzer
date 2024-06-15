SELECT count(DISTINCT(Tracks.isrc)) + count(*) - count(Tracks.isrc) AS [Total Tracks],
	count(DISTINCT(Artists.artist_name) )AS [Total Artists],
	count(DISTINCT(Albums.album_name) ) AS [Total Albums],
	sum(Tracks.explicit) AS [Explicit Tracks],
	round(sum(Tracks.track_duration_ms) * 1.66666667 / 100000,2) AS [Track Duration (min)]
FROM Tracks
JOIN TrackArtists
	ON TrackArtists.track_uri = Tracks.track_uri
JOIN Artists
	ON Artists.artist_uri = TrackArtists.artist_uri
JOIN Albums
	ON Tracks.album_uri = Albums.album_uri