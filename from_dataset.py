import pandas as pd
import random
import time
import cred
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime, timedelta

# Set up authentication for Spotify API
client_id = cred.client_id
client_secret = cred.client_secret
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the dataset
df = pd.read_csv('SpotifyFeatures.csv')

# User input
genre = input("Enter the genre: ")
market = input("Enter the market: ")
num_songs = int(input("Enter the number of songs to collect: "))

# Output dataframe
output = pd.DataFrame(columns=['Song Name', 'Artist Name', 'Number of Streams', 'Tempo', 'Duration (ms)', 'Number of Followers', 'Release Date', 'Days Since Release', 'Danceability'])

# Loop until enough songs are collected
while len(output) < num_songs:
    # Randomly select a track
    random_index = random.randint(0, len(df) - 1)
    track_uri = df['track_id'][random_index]
    
    # Get track information from Spotify API
    try:
        track_info = sp.track(track_uri)
        artist_info = sp.artist(track_info['artists'][0]['id'])
    except:
        time.sleep(2)
        continue
    
    # Check if it matches user input parameters
    if genre.lower() not in [g['name'].lower() for g in track_info['genre']]:
        continue
    if market.lower() not in track_info['available_markets']:
        continue
    
    # Collect information about the track
    song_name = track_info['name']
    artist_name = artist_info['name']
    num_streams = track_info['popularity']
    tempo = track_info['tempo']
    duration = track_info['duration_ms']
    followers = artist_info['followers']['total']
    release_date = track_info['album']['release_date']
    days_since_release = (pd.Timestamp.now() - pd.Timestamp(release_date)).days
    danceability = track_info['danceability']
    
    # Add the track to the output dataframe
    output = output.append({'Song Name': song_name, 'Artist Name': artist_name, 'Number of Streams': num_streams,
                            'Tempo': tempo, 'Duration (ms)': duration, 'Number of Followers': followers,
                            'Release Date': release_date, 'Days Since Release': days_since_release,
                            'Danceability': danceability}, ignore_index=True)

# Save output to a CSV file
output.to_csv('spotify_tracks2.csv', index=False)