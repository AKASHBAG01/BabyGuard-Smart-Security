from flask import Flask, jsonify
from api.camera import video_feed
from api.status import get_status
from api.events import get_events
from api.events import get_events
from api.unknown import get_unknown
from api.family import get_family
from api.add_person import add_person

app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({
        "project": "AI Baby Security System",
        "status": "running"
    })


@app.route("/live")
def live():

    return video_feed()


@app.route("/status")
def status():

    return jsonify(get_status())

@app.route("/events")
def events():
    return get_events()

@app.route("/unknown")
def unknown():

    return get_unknown()

@app.route("/family")
def family():

    return get_family()

@app.route("/add_person", methods=["POST"])
def add_new_person():
    return add_person()

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        threaded=True
    )