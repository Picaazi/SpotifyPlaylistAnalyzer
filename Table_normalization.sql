CREATE TABLE Tracks (
    track_uri TEXT PRIMARY KEY,
    track_name TEXT,
    album_uri TEXT,
    disc_number INTEGER,
    track_number INTEGER,
    track_duration_ms INTEGER,
    track_preview_url TEXT,
    explicit BOOLEAN,
    popularity INTEGER,
    isrc TEXT,
    FOREIGN KEY (album_uri) REFERENCES Albums(album_uri)
);

CREATE TABLE Artists (
    artist_uri TEXT PRIMARY KEY,
    artist_name TEXT
);

CREATE TABLE Albums (
    album_uri TEXT PRIMARY KEY,
    album_name TEXT,
    album_release_date DATE,
    album_image_url TEXT
);

CREATE TABLE AlbumArtists (
    album_uri TEXT,
    artist_uri TEXT,
    PRIMARY KEY (album_uri, artist_uri),
    FOREIGN KEY (album_uri) REFERENCES Albums(album_uri),
    FOREIGN KEY (artist_uri) REFERENCES Artists(artist_uri)
);

CREATE TABLE TrackArtists (
    track_uri TEXT,
    artist_uri TEXT,
    PRIMARY KEY (track_uri, artist_uri),
    FOREIGN KEY (track_uri) REFERENCES Tracks(track_uri),
    FOREIGN KEY (artist_uri) REFERENCES Artists(artist_uri)
);

CREATE TABLE Playlist (
    track_uri TEXT,
    added_at TIMESTAMP,
    PRIMARY KEY (track_uri, added_at),
    FOREIGN KEY (track_uri) REFERENCES Tracks(track_uri)
);