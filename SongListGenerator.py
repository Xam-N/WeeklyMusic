import requests
import apiKeys
    
channelName = "theneedledrop"
videoName = "Weekly Track Roundup: "

apiKey = apiKeys.youtubeApiKey

def getChannelID(username): # gives the channel ID
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "id",
        "forUsername": username,
        "key": apiKey
    }
    
    response = requests.get(url,params = params)
    return response.json()
    
def searchForVideo(channelID,query):

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelID": channelID,
        "q": query,
        "order":"date", 
        "key":apiKey
    }
    response = requests.get(url,params=params)
    for vid in response.json()['items']:
        if 'youtube#video' in vid['id']['kind']:
            return vid["id"]["videoId"]
        else:
            print(vid['id']['kind'])
            print("Not a video")
    return "Error, no video found"

def getVideo(videoID):
    
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": videoID,
        "key":apiKey
    }
    response = requests.get(url, params=params)

    return response.json()["items"][0]["snippet"]["description"]

def SongList(): # returns this weeks best tracks
        
    videoInfo = getVideo(searchForVideo(getChannelID(channelName),videoName)) # gives the description of the latest needledrop weekly video
    #print(videoInfo)
    videoInfo = videoInfo.splitlines()

    songList = [] 
    song = False

    for video in videoInfo:
        #print(video)
        if "BEST TRACK" in video: # checks if in the best tracks section
            #print("Here")
            song = True
            continue
            
        if "meh" in video: # checks if in the meh section
            song = False
            break
        
        if "Worst Tracks" in video: # checks if in the bad section
            song = False
            break
        
        if "https:" in video:
            continue
        
        if song == True and video != "":
            songList.append(video)
    #print(songList)
    return songList