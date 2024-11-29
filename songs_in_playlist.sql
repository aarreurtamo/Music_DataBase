SELECT Song.Name AS 'Name',
release_year AS 'Release Year',
artist.Name AS 'Artist Name'
FROM song
INNER JOIN artist ON Artist.ArtistID = Song.FK_ArtistID
WHERE song.songid IN
(SELECT FK_songID FROM Add_songs WHERE Add_songs.FK_PlaylistID = 1);