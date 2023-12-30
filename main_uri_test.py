import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openpyxl
from openpyxl import Workbook
import random
import cred
import datetime

# Set up Spotify API credentials
client_id = cred.client_id
client_secret = cred.client_secret
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set up Excel workbook
wb = Workbook()
ws = wb.active
ws.append(['Track URI', 'Song Title', 'Artist Name', 'Artist Followers', 'Global Streams', 'Tempo', 'Duration', 'Release Date', 'Single/Album'])

# User inputs
user_date = input('Enter a date in yyyy-mm-dd format: ')
user_market = input('Enter a Spotify market code (e.g. US, GB, FR): ')
user_num_songs = int(input('Enter the number of songs you want to generate: '))
user_genre = input('Enter a genre (optional): ')

# Convert user_date to a datetime object
user_date = datetime.datetime.strptime(user_date, '%Y-%m-%d').date()

# Track search function
def search_track():
    # Generate a random track URI
    rand_track_uri = 'spotify:track:' + ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(22))
    try:
        # Get track information from Spotify API
        track_info = sp.track(rand_track_uri)
        artist_info = sp.artist(track_info['artists'][0]['uri'])
        # Check if track meets user's criteria
        if track_info['album']['release_date'] < str(user_date):
            return False
        if user_genre and user_genre.lower() not in [g['name'].lower() for g in track_info['album']['genres']]:
            return False
        if user_market != track_info['album']['available_markets'] and user_market != 'global':
            return False
        # Return track information
        return [rand_track_uri, track_info['name'], artist_info['name'], artist_info['followers']['total'], track_info['popularity'], track_info['tempo'], track_info['duration_ms'], track_info['album']['release_date'], int(track_info['album']['album_type'] == 'single')]
    except Exception as e:
        print(f"Error fetching track {rand_track_uri}: {e}")
        return False
    
# Generate tracks and add to Excel sheet
count = 0
while count < user_num_songs:
    track_info = search_track()
    if track_info:
        ws.append(track_info)
        count += 1

# Save Excel workbook
wb.save('spotify_tracks.xlsx')
print(f'Successfully generated {user_num_songs} tracks and saved to spotify_tracks.xlsx')