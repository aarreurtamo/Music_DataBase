SELECT
Playlist.name as 'All Playlists by selected user'
from Playlist
inner join user on User.UserID = Playlist.Administrator
WHERE user.userID = 2;