import cv2
import time
from flask import Response
import modules.shared_frame as shared_frame


def generate_frames():

    while True:

        frame = shared_frame.latest_frame

        if frame is None:
            time.sleep(0.03)
            continue

        _, buffer = cv2.imencode(".jpg", frame)

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )


def video_feed():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )