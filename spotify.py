import requests
import os
import base64
import random
from urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request

load_dotenv(find_dotenv()) # This is to load your API keys from .env

token_url = "https://accounts.spotify.com/api/token" # url to get authorization and make a token for a session
genius_url = "https://api.genius.com/"
method = "POST"

# set the credentials from .env file
client_id = os.getenv('client_id_spotify')
client_secret = os.getenv('client_secret_spotify')
client_access_token = os.getenv('client_access_token') # <- for genius

# make an f string with the credentials, which will be encoded with base64 later
client_creds = f"{client_id}:{client_secret}"

# this encodes the creds into bytes and then one more time into base64 for it to be passed in header
client_creds_b64 = base64.b64encode(client_creds.encode())

token_data = {
    "grant_type": "client_credentials",
}
    
token_header = {
    "Authorization": f"Basic {client_creds_b64.decode()}" # client credentials utilized for authorization, creds are decoded to make it into a base64 encoded string not bytes 
}
    
response = requests.post(token_url, data=token_data, headers=token_header)
    
# handling the initial authentication requests
if response.status_code in range(200, 299): # to check if the response is valid or not
    response_data = response.json() # returns a map of different auth data
    access_token = response_data['access_token'] # grab the access_token
        
# this will get the song name, artists, images, url... using the tracks API
headers = {
    "Authorization" : f"Bearer {access_token}" # use the access token from above
}
    
# do genius authorization
headers_genius = {
    "Authorization" : f"Bearer {client_access_token}"
}

# introducing Flask framework to pass the data in list format 
app = Flask(__name__)

@app.route('/')
def home():
    # creating a home page where the user will be greated and be allowed to search any songs
    return render_template(
        "home.html"
    )
    
@app.route('/send', methods=['POST', 'GET'])  # <- to get user search input
def send():
    track=""
    if request.method == 'POST':
        track = request.form["search"]
    track = track.replace(" ", "%20")
    track_search_url = f"https://api.spotify.com/v1/search?q={track}&type=track%2Cartist&market=US"
    track_response = requests.get(track_search_url, headers=headers)
    track_data = track_response.json()
    
    # search version of the info for sportify api
    artist_s = track_data['tracks']['items'][0]['artists'][0]['name']
    song_s = track_data['tracks']['items'][0]['name']
    song_img_s = track_data['tracks']['items'][0]['album']['images'][1]['url']
    preview_url_s = track_data['tracks']['items'][0]['preview_url']
    
    # genius lyrics lookup
    genius_search_url = f"{genius_url}search?q={track}"
    genius_response = requests.get(genius_search_url, headers=headers_genius)
    lyrics_data = (genius_response.json())
    
    song_lyrics_s = lyrics_data['response']['hits'][0]['result']['url']
    artist_img_s = lyrics_data['response']['hits'][0]['result']['primary_artist']['image_url']
    
    return render_template(
        "home.html",
        artist = artist_s,
        song = song_s,
        song_img = song_img_s,
        preview_url = preview_url_s,
        song_lyrics=song_lyrics_s,
        artist_img=artist_img_s
    )
    
    
    
    
    
@app.route('/spotify')
def spotify():
    #print("HELLOO")
    # the artist's id
    artist_id = ['0Y5tJX1MQlPlqiwlOH1tJY', '3MZsBdqDrRTJihTHQrO6Dq', '4O15NlyKLIASxsJ0PrXPfz', '1anyVhU62p31KFi8MEzkbf', '7tYKF4w9nC0nq9CsPZTHyP', '2h93pZq0e7k5yf4dywlkpM','1Xyo4u8uXC1ZmMpatF05PJ','20wkVLutqVOYrc0kxFs7rA'] 
    # travis, joji, lil uzi, chance, sza, frank ocean, weekend, daniel
        
    artist_index = random.randint(0, len(artist_id)-1) # determines the artist from the list above
    track_index = random.randint(0, 9) # determines the track from the top-tracks(10 tracks)
    
    #print(artist_index)
    #print(track_index)
        
    endpoint = f"https://api.spotify.com/v1/artists/{artist_id[artist_index]}/top-tracks" # endpoint to use for artists' top-tracks api
    #print(endpoint)
    market = urlencode({"market": "US"})        
    lookup_url = f"{endpoint}?{market}"
    artist_response = requests.get(lookup_url, headers=headers) # make the request
    artist_data = (artist_response.json()) # append each artist's data into the list 
        
    #print(artist_data)
    # this sets the name of artist, artist's song, song cover, and song preview 
    artist = artist_data['tracks'][track_index]['artists'][0]['name']
    song = artist_data['tracks'][track_index]['name']
    song_img = artist_data['tracks'][track_index]['album']['images'][1]['url']
    preview_url = artist_data['tracks'][track_index]['preview_url']
        
    #print("artist: " + artist)
    #print("song: " + song)
    #print("song_img: " + song_img)
    #print("preview_url: " + str(preview_url))
    # to search genius lyrics of the songs
    song_genius_url = song.replace(" ", "%20") # <- replace the spaces for url use in genius api request
    genius_search = f"{genius_url}search?q={song_genius_url}"
    genius_response = requests.get(genius_search, headers=headers_genius)
    lyrics_data = (genius_response.json())
    #print(lyrics_data)
        
    # get the lyrics link of the song
    song_lyrics = lyrics_data['response']['hits'][0]['result']['url']
    artist_img = lyrics_data['response']['hits'][0]['result']['primary_artist']['image_url']
    
    return render_template(
        "index.html",
        artist = artist,
        song = song,
        song_img = song_img,
        preview_url = preview_url,
        song_lyrics=song_lyrics,
        artist_img=artist_img
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)