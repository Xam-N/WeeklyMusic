import flask
import urllib.parse
import webbrowser
import threading
import requests
import base64
import datetime

app = flask.Flask(__name__)

authCode = None

callback_event = threading.Event()

clientID = '1e65a0ba27a9410f974dbcf7004c2fe0'
redirectURI = 'http://localhost:8888/callback'
clientSecret = "773e1b028ca4456385c8ea99c2270e3a"

def tokenGen():
  
  
  threading.Thread(target=lambda: app.run(port=8888)).start()

  webbrowser.open('http://localhost:8888/login')

  callback_event.wait()
  
  accessToken = getKey(authCode, redirectURI,clientID,clientSecret)['access_token']
  
  return accessToken

@app.route('/login')
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

@app.route('/callback')
def callback():
  global authCode
  code = flask.request.args.get('code')
  authCode = code
  callback_event.set()
  return code

def getKey(authCode,redirect_uri,clientID,clientSecret):
  url = "https://accounts.spotify.com/api/token"
  authString = clientID + ":" + clientSecret
  authString = base64.b64encode(authString.encode()).decode()
  data = {
    "code": authCode,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code"
  }
  headers = {
    "content-type" : "application/x-www-form-urlencoded",
    "Authorization" : "Basic " + authString
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
        #"description": "New playlist description",
        "public" : False
    }
    
    response = requests.post(url,headers = header, json=data)
    #print(response.json()['id'])
    return response.json()['id']

def findSongID(songToSearch, accessToken):
  year = datetime.date.today().strftime("%Y")
  url = "https://api.spotify.com/v1/search"
  params = {
    "q" : songToSearch + "year:" + year,
    "type" : "track",
    "limit":"1"
  }
  header = {
    "Authorization" : 'Bearer ' + accessToken
  }
  response = requests.get(url,params=params,headers=header)
  #print(response)
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