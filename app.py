from flask import Flask, request, render_template, json
from sassutils.wsgi import SassMiddleware
from pymongo import MongoClient
from bson.json_util import dumps
from config import MONGODB_URI
from spotify.playlist import get_playlist, get_tracks

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
mdb_connect_string = MONGODB_URI

app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/scss', 'static/css', '/static/css')
})


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/data", methods=['GET'])
def get_data():
    try:
        # connection = MongoClient(mdb_connect_string)  # equal to > show dbs
        # db = connection.spotify
        # mdb_playlist = db.playlists.find_one()
        sp_playlist = get_playlist()
        # if mdb_playlist['snapshot_id'] != sp_playlist['snapshot_id']:
        #     db.tracks.update({}, sp_playlist, upsert=True)
        #     db.tracks.drop()
        #     db.createCollection('tracks')
        #     db.tracks.insert_many(get_tracks(sp_playlist))
        # return dumps([track for track in get_tracks(sp_playlist)])
        return {'msg': 'hello world'}
    except:
        return {'msg': 'hello world'}
    #     exit("Error: Unable to connect to the database")


if __name__ == "__main__":
    app.run(debug=True)
