from dateutil.parser import parse as parse_date
import pandas as pd
import spotipy
import spotipy as sp
import spotipy.util as util
import requests
from pprint import pprint
import time

#TODO Need to add in Spotify Credentials


token = util.prompt_for_user_token(user_id,
                                   'playlist-read-collaborative',
                                   client_id,
                                   client_secret,
                                   redirect_uri)
sp = spotipy.Spotify(auth=token)

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
                           track['track']['artists'][0]['id'],
                           track['added_by']['id'],
                           parse_date(track['track']['album']['release_date']) if track['track']['album']['release_date'] else None,
                           parse_date(track['added_at']))
                          for track in playlist['tracks']['items']],
                         columns=['id', 'artist', 'name', 'artist_id','user_id', 'release_date', 'added_at'])


#Artist ID

artist_id = tracks_df['artist_id']
artist_id = artist_id.unique()

#User ID

user_id = tracks_df['user_id'].unique()
user_id.tolist()

#User Song ID

user_song_ids = pd.DataFrame(tracks_df, columns= ['id', 'user_id'])
user_song_ids

#User Artist ID

user_artist_id = pd.DataFrame(tracks_df, columns= ['artist_id', 'user_id'])
user_artist_id

#Put Track IDs into a list for Audio Features Loop

song_id_list = tracks_df["id"].tolist()
pprint(song_id_list)

# Get Track Features

def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

# meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

# features
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

# loop over track ids 
tracks = []
for i in range(len(song_id_list)):
    time.sleep(.1)
    track = getTrackFeatures(song_id_list[i])
    tracks.append(track)

pprint(tracks)

# create dataset
song_data = pd.DataFrame(tracks, columns = ['id','name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])

#Merge data

final = pd.merge(song_data, user_song_ids, how = 'left', on = 'id')
final =pd.DataFrame(final)

final = pd.merge(final, genre_df, how = 'left', left_on = 'artist', right_on = 'artist')

final.to_csv("user_song_info.csv", sep = ',')