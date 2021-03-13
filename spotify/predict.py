from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import itertools
import os

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def get_track_genres(q):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    track = sp.search(q=q, limit=1)['tracks']['items'][0]

    artists = sp.artists(artists=[artist['id'] for artist in track['artists']])
    genres = list(set(list(itertools.chain(*[artist['genres'] for artist in artists['artists']]))))
    words = list(set([word for word in ' '.join([genre.replace('-', ' ') for genre in genres]).split(' ') if word not in ['a', 'and']]))
    features = sp.audio_features(tracks=[track['id']])[0]

    model = load_model('spotify/track_model.h5')
    X_scaler = joblib.load('spotify/scaler.gz')
    label_encoder = joblib.load('spotify/label_encoder.gz')

    features_df = pd.DataFrame({k: [v] for k, v in features.items()})[['acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'speechiness', 'tempo', 'valence']]
    features_scaled = X_scaler.transform(features_df)
   
    encoded_prediction = model.predict_classes(features_scaled)
    prediction = label_encoder.inverse_transform(encoded_prediction)[0]
    
    features['artists'] = [artist['name'] for artist in track['artists']],
    features['words'] = words,
    features['prediction'] = prediction

    return features
