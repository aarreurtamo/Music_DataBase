PRAGMA foreign_keys = ON;


--Tables

CREATE TABLE User(
UserID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
Age INTEGER CHECK(Age >= 14),
Name VARCHAR(20) UNIQUE,
Followers INTEGER DEFAULT 0
);
CREATE TABLE Song(
SongID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name varchar(50) UNIQUE,
release_year INTEGER CHECK(release_year >= 1950 and release_year <= 2024),
FK_ArtistID INTEGER NOT NULL,
FOREIGN KEY (FK_ArtistID) REFERENCES Artist(ArtistID)
ON DELETE CASCADE
ON UPDATE CASCADE
);
CREATE TABLE Playlist(
PlaylistID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
Name VARCHAR(20),
Administrator INTEGER NOT NULL,
FOREIGN KEY (Administrator) REFERENCES User(UserID)
ON DELETE CASCADE
ON UPDATE CASCADE
);
CREATE TABLE Artist(
ArtistID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name varchar(50) UNIQUE,
First_Song_Released INTEGER CHECK(First_Song_Released >= 1950 and First_Song_Released <= 2024),
nationality varchar(20)
);
CREATE TABLE Listeners(
FK_SongID INTEGER NOT NULL,
FK_UserID INTEGER,
FOREIGN KEY (FK_SongID) REFERENCES Song(SongID)
ON DELETE CASCADE
ON UPDATE CASCADE,
FOREIGN KEY(FK_UserID) REFERENCES User(UserID)
ON DELETE SET NULL
ON UPDATE CASCADE
);
CREATE TABLE Add_songs(
FK_SongID INTEGER NOT NULL,
FK_PlaylistID INTEGER NOT NULL,
FOREIGN KEY (FK_SongID) REFERENCES Song(SongID)
ON DELETE CASCADE
ON UPDATE CASCADE,
FOREIGN KEY(FK_PlaylistID) REFERENCES Playlist(PlaylistID)
ON DELETE CASCADE
ON UPDATE CASCADE
);


--Views

CREATE VIEW Artist_information AS
SELECT Artist.name,Artist.First_Song_Released,Artist.nationality FROM Artist;

CREATE VIEW songs_by_artist AS SELECT
Song.name as 'All songs by selected artist'
from song
inner join artist on Artist.ArtistID = Song.FK_ArtistID
WHERE artist.ArtistID = 6;

CREATE VIEW all_playlists AS SELECT
Playlist.name as 'All Playlists by selected user'
from Playlist
inner join user on User.UserID = Playlist.Administrator
WHERE user.userID = 2;

CREATE VIEW songs_by_user AS SELECT Song.Name AS 'Name',
release_year AS 'Release Year',
artist.Name AS 'Artist Name'
FROM song
INNER JOIN artist ON Artist.ArtistID = Song.FK_ArtistID
WHERE song.songid IN
(SELECT FK_songID FROM listeners WHERE listeners.FK_Userid = 2);

CREATE VIEW artists_on_playlists AS SELECT
Playlist.Name as 'PlaylistName',
Song.Name as 'SongName',
Artist.Name as 'ArtistName'
FROM
Playlist
INNER JOIN
Add_songs on Playlist.PlaylistID = Add_songs.FK_PlaylistID
INNER JOIN
Song on Add_songs.FK_SongID = Song.SongID
INNER JOIN
Artist on Song.FK_ArtistID = Artist.ArtistID
Order by PlaylistID,ArtistID,SongID;

CREATE VIEW most_listened_songs AS
select x,song.name from (select FK_SongID,count(FK_UserID) as x from Listeners 
group by Listeners.FK_SongID)
inner join song on song.SongID = FK_SongID
order by x DESC;

-- Indexes

CREATE INDEX SongNameIndex ON Song(Name);
CREATE INDEX ArtistNameIndex ON Artist(Name);
CREATE INDEX UserNameIndex ON User(Name);
CREATE INDEX PlaylistNameIndex ON Playlist(Name);

