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

  failedSongs = [] #List of songs I was unable to find on spotify
  for song in songList:
    print(f"Song Name: {song}")
    #print(SpotifyPlaylistGenerator.findSongID(song, accessToken).json())
    try:
      songID = SpotifyPlaylistGenerator.findSongID(song, accessToken).json()['tracks']['items'][0]['id']
    except:
      failedSongs.append(song)
      print("Failed to find song")
      
    #print(f"SongID: {songID}")
    SpotifyPlaylistGenerator.addSongToPlaylist(playlistID,songID,accessToken)


  print(f"Failed to add the following songs \n {failedSongs}")
  
  os._exit(0)
  
  

runner()