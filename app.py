from flask import Flask, request, render_template, json
from sassutils.wsgi import SassMiddleware
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["MONGO_URI"] = "mongodb://localhost:27017/spotify_db"
mdb_connect_string = "mongodb://localhost:27017"

app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/scss', 'static/css', '/static/css')
})


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/data", methods=['GET'])
def get_data():
    connection = None
    try:
        connection = MongoClient(mdb_connect_string)  # equal to > show dbs
    except:
        exit("Error: Unable to connect to the database")
    db = connection.spotify
    # run playlist.py (gets playlist from spotify API)
    # get the snapshot_id from the response
    # current_snapshot_id = mongo.db.playlist.find_one()
    # if (api_snapshot_id != current_snapshot_id):
    # run the code in audio-features.py
    # update tracks collection in mongo
    # run the code in user.py
    # update user in mongo
    # output = []
    # for track in mongo.db.tracks.find():
    #     output.append({k: v for k, v in track.items() if k != '_id'})
    return dumps([track for track in db.tracks.find()])


if __name__ == "__main__":
    app.run(debug=True)
