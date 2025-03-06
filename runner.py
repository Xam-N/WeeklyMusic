import SongListGenerator
import SpotifyPlaylistGenerator
import os
import datetime
from flask import Flask, session, redirect, render_template, stream_with_context, Response
import threading
import webbrowser 

website = Flask(__name__)

website.secret_key = 'supersecretkey'

threading.Thread(target=lambda: website.run(port=8888, use_reloader=False)).start()

webbrowser.open('http://localhost:8888/')

@website.route("/")
def home():
  return render_template("home.html")
  
@website.route("/spotifyLogin")
def loginRedirect():
    return redirect("/login")

@website.route("/action2")
def action2():
    return "Button 2 Clicked!"
  
@website.route('/set_token')
def set_token():
    session['spotifyAccessToken'] = "Hello?"
    return 'Token stored in session!'

@website.route('/getToken')
def get_token():
    token = session.get('spotifyAccessToken', 'No token found')
    return f'Stored token: {token}'
  
@website.route("/weeklyMusic")
def weeklyMusic():
  
  render_template("weeklyMusic.html")
  
  songList = SongListGenerator.SongList() # generates a song list from the youtube video
  
  accessToken = session.get('spotifyAccessToken')
  
  print(accessToken)
    
  now = datetime.date.today()

  playlistName = now.strftime("%d - %m")
  
  playlistID = SpotifyPlaylistGenerator.createPlaylist(accessToken, playlistName)
  
  def generate():
        """Streams updates to the client while looping"""
        yield render_template("weeklyMusic.html", message="Processing playlist...")

        for song in songList:
            songID = SpotifyPlaylistGenerator.findSongID(song, accessToken).json()['tracks']['items'][0]['id']
            SpotifyPlaylistGenerator.addSongToPlaylist(playlistID, songID, accessToken)

            # Send an update after processing each song
            yield f"<p>Added song: {song}</p>\n"

        yield f'<p>{playlistName} created successfully!</p>'
        yield '<a href="/" class="button">Go Home</a>'
  
  
  return Response(stream_with_context(generate()), content_type='text/html')
#runner()
  