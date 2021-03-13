from flask import Flask, request, render_template, json
from sassutils.wsgi import SassMiddleware
from pymongo import MongoClient
import os
from bson.json_util import dumps
from spotify.playlist import get_playlist, get_tracks
from spotify.predict import get_track_genres

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
mdb_connect_string = os.environ['MONGODB_URI']

app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/scss', 'static/css', '/static/css')
})


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/data", methods=['GET'])
def get_data():
    try:
        connection = MongoClient(mdb_connect_string)
        db = connection.spotify
        mdb_playlist = db.playlists.find_one()
        sp_playlist = get_playlist()
        if mdb_playlist['snapshot_id'] != sp_playlist['snapshot_id']:
            db.playlists.update({}, sp_playlist, upsert=True)
            db.tracks.drop()
            db.tracks.insert_many(get_tracks(sp_playlist))
        tracks = dumps([track for track in db.tracks.find()])
        return tracks
    except:
        exit("Error: Unable to connect to the database")


@app.route("/recommend", methods=['GET'])
def get_recommendations():
    track_id = request.args['track_id']
    try:
        connection = MongoClient(mdb_connect_string)
        db = connection.spotify
        rec_tracks = dumps([track for track in db.recommended.find(
                { 'info.orig_track_id': { '$regex': '.*' + track_id[:-1] + '.*'} }
            )])
        if (len(rec_tracks) == 0):
            return dumps({'err': 'No tracks found'})
        else:
            return rec_tracks
    except:
        exit("Error: Unable to connect to the database")


@app.route("/genre-predict", methods=['GET'])
def get_genre_prediction():
    result = get_track_genres(request.args['q'])
    return dumps(result)


if __name__ == "__main__":
    app.run(debug=True)


dummy_tracks = [
    {
        'info': {
            'artist': 'Sammy Hagar',
            'name': "I can't drive 55",
            'id': "sligjsdo93u2849023"
        },

    }
]