from flask import Flask, request, render_template, json
from sassutils.wsgi import SassMiddleware
from flask_pymongo import PyMongo
import json
import pandas as pd

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["MONGO_URI"] = "mongodb://localhost:27017/spotify-db"
mongo = PyMongo(app)

app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/scss', 'static/css', '/static/css')
})


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/data")
def get_data():
    # run playlist.py (gets playlist from spotify API)
    # get the snapshot_id from the response
    # current_snapshot_id = mongo.db.playlist.find_one()
    # if (api_snapshot_id != current_snapshot_id):
        # run the code in audio-features.py
        # update tracks collection in mongo
        # run the code in user.py
        # update user in mongo
    tracks = mongo.db.tracks.find()
    return json.dumps(tracks)


if __name__ == "__main__":
    app.run(debug=True)
