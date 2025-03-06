import flask
import urllib.parse
import webbrowser
import threading
import requests
import base64
import datetime
from runner import website #imports flask application from main
from apiKeys import spotifyClientID, spotifyClientSecret

authCode = None
clientID = spotifyClientID
clientSecret = spotifyClientSecret
redirectURI = 'http://localhost:8888/callback'

@website.route('/login')
def login():
    scope = 'user-read-private playlist-modify-private'
    
    query_params = urllib.parse.urlencode({
        'response_type': 'code',
        'client_id': clientID,
        'scope': scope,
        'redirect_uri': redirectURI
    })
    auth_url = f'https://accounts.spotify.com/authorize?{query_params}'
    return flask.redirect(auth_url)

@website.route('/callback')
def callback():
    global authCode
    code = flask.request.args.get('code')
    authCode = code

    spotifyAccessToken = getKey(authCode, redirectURI, clientID, clientSecret)['access_token'] #gives access token, needed
    print(spotifyAccessToken)
    print("Doing stuff")
    flask.session['spotifyAccessToken'] = spotifyAccessToken
    return flask.redirect('/weeklyMusic')


def getKey(authCode, redirect_uri, clientID, clientSecret):
    url = "https://accounts.spotify.com/api/token"
    authString = clientID + ":" + clientSecret
    authString = base64.b64encode(authString.encode()).decode()
    data = {
        "code": authCode,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + authString
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()



def createPlaylist(accessToken,playlistName):
    url = "https://api.spotify.com/v1/users/slothsinblack/playlists"
    header = {
        "Authorization" : 'Bearer ' + accessToken,
        "Content-Type" : "application/json"
    }
    data = {
        "name" : playlistName,
        "public" : False
    }
    
    response = requests.post(url,headers = header, json=data)
    return response.json()['id']

def findSongID(songToSearch, accessToken):
  year = datetime.date.today().strftime("%Y")
  url = "https://api.spotify.com/v1/search"

  artistName, songTitle = songToSearch.split(" - ", 1) #ensures that only 1 split takes place
  if "ft." in songTitle:
    #print(f"Removing featured artists {songTitle}")
    songTitle = songTitle.split(" ft. ",1)[0]
    #print(f"Removed featured artists {songTitle}")
    
  params = {
    "q": f"track:{songTitle} artist:{artistName} year:{year}",
    "type" : "track",
    "limit":"1"
  }
  header = {
    "Authorization":f"Bearer {accessToken}"
  }
  response = requests.get(url,params=params,headers=header)
  
  return response

def addSongToPlaylist(playlistID, songID, accessToken):
    url = f"https://api.spotify.com/v1/playlists/{playlistID}/tracks"
    headers = {
        "Authorization": "Bearer " + accessToken,
        "Content-Type": "application/json"
    }
    data = {
        "uris": [f"spotify:track:{songID}"]
    }
    response = requests.post(url, headers=headers, json=data)
    return response

