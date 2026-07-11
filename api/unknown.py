import os
from flask import jsonify

UNKNOWN_FOLDER = "Unknown_Person"


def get_unknown():

    if not os.path.exists(UNKNOWN_FOLDER):
        return jsonify({"photos": []})

    photos = []

    for file in os.listdir(UNKNOWN_FOLDER):

        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            photos.append(file)

    photos.sort(reverse=True)

    return jsonify({
        "photos": photos
    })