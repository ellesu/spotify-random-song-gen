import pandas as pd
import spotipy
import cred
from spotipy.oauth2 import SpotifyClientCredentials

# set up Spotify API client
client_id = cred.client_id
client_secret = cred.client_secret
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



# read Excel file
df = pd.read_excel('pop.xlsx')

# loop through each track ID and search on Spotify API
for i, row in df.iterrows():
    track_id = row[2] # assumes track ID is in the third column
    track_info = sp.track(track_id)
    num_streams = track_info['popularity'] # number of streams is equivalent to popularity
    df.at[i, df.columns[-1] + '_streams'] = num_streams # appends number of streams onto the next open column
    if(track_info['album']['album_type']=="album"):
        album_type = 1
        
# write updated DataFrame to Excel file
df.to_excel('pop2.xlsx', index=False)