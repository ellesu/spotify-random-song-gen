import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred 
import random
import openpyxl
from openpyxl import Workbook
from datetime import datetime

# CHANGE SCOPE TO BE ALL SPOTIFY SONGS, THEN ADD THE DATE COMPONENT BACK IN

# Define the Spotify API credentials
client_id=cred.client_id
client_secret=cred.client_secret

# Authenticate with the Spotify API using the client credentials
# client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                                redirect_uri="https://google.com",
                                               scope=""))

# Input parameters
# date = input("Enter the release date (YYYY-MM-DD): ")
genre = input("Enter the genre: ")
num_songs = int(input("Enter the number of songs to fetch: "))

# release_date:{} , date
# Search for tracks based on release date and genre
# query = "genre:{} year:{} tag:new".format(genre, date.split('-')[0])
# results = sp.search(q=query, type='track', limit=50)

query = "genre:{}".format(genre)

# Search for tracks based on release date and genre
# query = "year:{} tag:new".format(date.split('-')[0])

results = sp.search(q='tag:new', type='track', market='US', limit=num_songs)

tracks = results['tracks']['items']

if num_songs > len(tracks):
    num_songs = len(tracks)
    print("Number of songs to fetch is greater than the number of tracks returned. Fetching {} songs instead.".format(num_songs))

# Select random tracks from the search results
random_tracks = random.sample(tracks, num_songs)
if results['tracks']['items'] == []:
    print("Error: No tracks found for the specified query.")
else:
    tracks = results['tracks']['items']

# Create Excel workbook and worksheet
wb = openpyxl.Workbook()
ws = wb.active

# Write header row
ws.append(['Track ID', 'Track Name', 'Artist', 'Followers', 'Streams', 'Release Date', 'Duration (ms)', 'Tempo','Album'])

# Iterate through the selected tracks and extract relevant information
for track in random_tracks:
    track_id = track['id']
    track_info = sp.track(track_id)
    song_name = track['name']
    artist_name = track['artists'][0]['name']
    artist_id = track['artists'][0]['id']
    followers = sp.artist(artist_id)['followers']['total']
    streams = sp.track(track_id)['id']
    print(streams)
    release_date = track['album']['release_date']
    if(track['album']['album_type']=="album"):
        album_type = 1
    else:
        album_type = 0
    duration_ms = track['duration_ms']
    tempo = sp.audio_features(track_id)[0]['tempo']
    
    # Write track information to worksheet
    ws.append([track_id, song_name, artist_name, followers, streams, release_date, duration_ms, tempo, album_type])

# Save workbook
wb.save('spotify_tracks.xlsx')