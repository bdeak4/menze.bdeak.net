#!venv/bin/python

from bottle import route, run, template
import requests


@route("/")
def index():
    return template("index.html")


run(host="0.0.0.0", port=8080, server="waitress")
