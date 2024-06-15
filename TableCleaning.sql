ALTER TABLE Tracks
ADD COLUMN location_code TEXT;

ALTER TABLE Tracks
ADD COLUMN registrant_code TEXT;

ALTER TABLE Tracks
ADD COLUMN year_of_reference TEXT;

ALTER TABLE Tracks
ADD COLUMN designation_code TEXT;

UPDATE Tracks
SET
    location_code = SUBSTR(isrc, 1, 2),
    registrant_code = SUBSTR(isrc, 3, 3),
    year_of_reference = SUBSTR(isrc, 6, 2),
    designation_code = SUBSTR(isrc, 8);
