from flask import Flask, request, render_template, json
from sassutils.wsgi import SassMiddleware
import pandas as pd

app = Flask(__name__)

app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/scss', 'static/css', '/static/css')
})


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/data")
def get_data():
    df = pd.csv('spotify.csv')
    df_json = df.to_json(orient="index")
    res =
    return 'this is where I give you the data'


if __name__ == "__main__":
    app.run(debug=True)
