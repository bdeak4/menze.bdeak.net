from flask import Flask, render_template

import data

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.jinja", canteens=data.get_canteens())