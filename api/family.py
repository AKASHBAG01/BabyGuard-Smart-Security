import json
import os
from flask import jsonify

DATABASE = "database/family.json"


def get_family():

    if not os.path.exists(DATABASE):

        return jsonify({
            "members": []
        })

    with open(DATABASE, "r") as file:

        data = json.load(file)

    return jsonify(data)