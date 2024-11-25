import SongListGenerator
import SpotifyPlaylistGenerator
import os
import datetime

def runner():
  
  songList = SongListGenerator.SongList()
  #print(songList)
  
  accessToken = SpotifyPlaylistGenerator.tokenGen()
  
  now = datetime.date.today()

  playlistName = now.strftime("%d - %m")
  
  playlistID = SpotifyPlaylistGenerator.createPlaylist(accessToken, playlistName)
  
  for song in songList:
    songID = SpotifyPlaylistGenerator.findSongID(song, accessToken).json()['tracks']['items'][0]['id']
    #print("Here")
    SpotifyPlaylistGenerator.addSongToPlaylist(playlistID,songID,accessToken)
  
  os._exit(0)
  

runner()