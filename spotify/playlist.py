#Dependencies

from dateutil.parser import parse as parse_date
import pandas as pd
import spotipy
import spotipy.util as util
import time
import os
user_id = os.environ['USER_ID']
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
redirect_uri = os.environ['REDIRECT_URI']
playlist_id = os.environ['PLAYLIST_ID']
# TODO Need to add in Spotify Credentials
def spotipy_connect():
    token = util.prompt_for_user_token(user_id,
                                       'playlist-read-collaborative',
                                       client_id,
                                       client_secret,
                                       redirect_uri)
    return spotipy.Spotify(auth=token)
# Read Playlist to pull data from Spotify API
def get_playlist():
    sp = spotipy_connect()
    return sp.user_playlist(user_id, playlist_id)
def get_tracks(playlist):
    sp = spotipy_connect()
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
                               parse_date(track['track']['album']['release_date']) if track['track']['album'][
                                   'release_date'] else None,
                               parse_date(track['added_at']))
                              for track in playlist['tracks']['items']],
                             columns=['id', 'artist', 'name', 'artist_id', 'user_id', 'release_date', 'added_at'])
    user_song_ids = pd.DataFrame(tracks_df, columns=['id', 'user_id'])
    song_id_list = tracks_df["id"].tolist()
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
        track = [id, name, album, artist, release_date, length, popularity, danceability, acousticness,
                 energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
        return track
    # loop over track ids
    tracks = []
    for i in range(len(song_id_list)):
        time.sleep(.1)
        track = getTrackFeatures(song_id_list[i])
        tracks.append(track)
    # create dataset
    song_data = pd.DataFrame(tracks, columns=['id', 'name', 'album', 'artist', 'release_date', 'length', 'popularity',
                                              'danceability', 'acousticness', 'energy',
                                              'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo',
                                              'time_signature'])
    # Merge data
    final = pd.merge(song_data, user_song_ids, how='left', on='id')
    final = pd.DataFrame(final)
    tracks_list = []
    for index, row in final.iterrows():
        track = {
            'info': {
                'name': row['name'],
                'album': row['album'],
                'artist': row['artist'],
                'user_id': row['user_id'],
                'track_id': row['id']
            },
            'features': {
                'length': row['length'],
                'popularity': row['popularity'],
                'danceability': row['danceability'],
                'acousticness': row['acousticness'],
                'danceability': row['danceability'],
                'energy': row['energy'],
                'instrumentalness': row['instrumentalness'],
                'liveness': row['liveness'],
                'loudness': row['loudness'],
                'speechiness': row['speechiness'],
                'tempo': row['tempo'],
                'time_signature': row['time_signature'],
            }
        }
        tracks_list.append(track)
    return tracks_list

















