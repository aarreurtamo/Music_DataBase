SELECT
Song.name as 'All songs by selected artist'
from song
inner join artist on Artist.ArtistID = Song.FK_ArtistID
WHERE artist.ArtistID = 1;