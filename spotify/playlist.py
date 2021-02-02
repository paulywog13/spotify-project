#Dependencies

from dateutil.parser import parse as parse_date
import pandas as pd
import spotipy as sp
import requests
from pprint import pprint
import time

#Read Playlist to pull data from Spotify API

playlist = sp.user_playlist(user_id, playlist_id)
tracks = playlist['tracks']['items']
next_uri = playlist['tracks']['next']
for _ in range(int(playlist['tracks']['total'] / playlist['tracks']['limit'])):
    response = sp._get(next_uri)
    tracks += response['items']
    next_uri = response['next']

tracks_df = pd.DataFrame([(track['track']['id'],
                           track['track']['artists'][0]['name'],
                           track['track']['name'],
                           track['added_by']['id'],
                           parse_date(track['track']['album']['release_date']) if track['track']['album']['release_date'] else None,
                           parse_date(track['added_at']))
                          for track in playlist['tracks']['items']],
                         columns=['id', 'artist', 'name', 'user_id', 'release_date', 'added_at'])


token = util.prompt_for_user_token(user_id,
                                   'playlist-read-collaborative',
                                   client_id,
                                   client_secret,
                                   redirect_uri)
sp = spotipy.Spotify(auth=token)

# Artist ID in Dataframe
artist_id = pd.DataFrame(artist_id['id'])
artist_id

# Pull User ID from Tracks
user_id = tracks_df['user_id'].unique()
user_id.tolist()

# Dataframe for Song ID and User ID

user_song_ids = pd.DataFrame(tracks_df, columns= ['id', 'user_id'])

#Send Song ID's to List

song_id_list = tracks_df["id"].tolist()

# Set Audio Features 
def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)
# features
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    track = [id, name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track

# For Loop track ids 
tracks = []
for i in range(len(song_id_list)):
  time.sleep(.1)
  track = getTrackFeatures(song_id_list[i])
  tracks.append(track)

# create song dataset
song_data = pd.DataFrame(tracks, columns = ['id','name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])

# Merge Datasets together

final = pd.merge(song_data, user_song_ids, how = 'left', on = 'id')
final =pd.DataFrame(final)

# Export to CSV

final.to_csv("user_song_info.csv", sep = ',')
