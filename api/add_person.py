import cv2
import numpy as np
import os

from flask import request, jsonify

from add_faces import save_dataset

CASCADE_PATH = "models/haarcascade_frontalface_default.xml"

cascade = cv2.CascadeClassifier(CASCADE_PATH)


def add_person():

    name = request.form.get("name")

    if not name:
        return jsonify({
            "success": False,
            "message": "Name missing"
        })

    images = request.files.getlist("images")

    if len(images) == 0:
        return jsonify({
            "success": False,
            "message": "No images uploaded"
        })

    faces = []

    for image_file in images:

        image_bytes = np.frombuffer(image_file.read(), np.uint8)

        frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detected = cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(detected) == 0:
            continue

        x, y, w, h = detected[0]

        face = frame[y:y+h, x:x+w]

        face = cv2.resize(face, (50, 50))

        faces.append(face)

    if len(faces) == 0:
        return jsonify({
            "success": False,
            "message": "No faces detected"
        })

    save_dataset(name, np.array(faces))

    return jsonify({
        "success": True,
        "person": name,
        "samples": len(faces)
    })