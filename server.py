#!venv/bin/python

from bottle import route, run, template, static_file
import requests
import re


filter_out = [
    "juha",
    "salata",
    "kolač",
    "puding",
    "naranča",
    "banana",
    "jabuka",
    "jogurt",
    "munchmallow",
    "mlijeko",
]
regex = re.compile(".*" + ".*|.*".join(filter_out) + ".*", re.IGNORECASE)


@route("/")
def index():
    data = [(4, {}), (7, {}), (6, {}), (3, {})]
    canteens = requests.get("https://prod2.unispot.live/api/public/mess").json()
    for c in canteens:
        idx = next((i for i, d in enumerate(data) if d[0] == c["index"]), None)
        if idx == None:
            continue

        cur = data[idx][1]
        cur["name"] = c["name"].replace("_", "")

        try:
            camera_feed = requests.get(c["camUri"]).json()
            cur["camera_snapshot"] = camera_feed["imagePath"]
            cur["camera_timestamp"] = camera_feed["time"]
            cur["camera_active"] = camera_feed["active"]
        except:
            cur["camera_active"] = False

        cur["menu"] = []
        if "menu" in c:
            for meal in c["menu"]:
                menu = {}
                hr = {"lunch": "Ručak", "dinner": "Večera"}
                menu["name"] = hr[meal]
                menu["from"] = c["menu"][meal]["from"]
                menu["till"] = c["menu"][meal]["till"]

                dishes = []
                if "meals" in c["menu"][meal]:
                    for d in c["menu"][meal]["meals"]:
                        if not regex.match(d["dish"]):
                            dishes.append(d["dish"])

                if "menus" in c["menu"][meal]:
                    for m in c["menu"][meal]["menus"]:
                        for d in m["dishes"]:
                            if not regex.match(d):
                                dishes.append(d)

                menu["dishes"] = list(set(dishes))
                cur["menu"].append(menu)

    return template("index.html", canteens=data)


@route("/style.css")
def style():
    return static_file("style.css", root=".")


@route("/static.gif")
def tv_static():
    return static_file("static.gif", root=".")


run(host="0.0.0.0", port=8080, server="waitress")
