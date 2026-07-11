import json
import os

from flask import jsonify

EVENT_FILE = "database/events.json"


def get_events():

    if not os.path.exists(EVENT_FILE):
        return jsonify({
            "events": []
        })

    try:
        with open(EVENT_FILE, "r") as file:
            events = json.load(file)

        return jsonify({
            "events": events
        })

    except Exception as e:

        return jsonify({
            "events": [],
            "error": str(e)
        })