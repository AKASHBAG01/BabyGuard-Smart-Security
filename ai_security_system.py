import cv2
import time
import os
import modules.shared_frame as shared_frame
from threading import Thread
from api.app import app

from modules.face_recognition import FaceRecognizer
from modules.object_detection import ObjectDetector
from modules.dashboard import Dashboard
from modules.event_logger import logger
from modules.relationship_detector import RelationshipDetector
from modules.zone_editor import ZoneEditor

# --------------------------------
# Configuration
# --------------------------------
UNKNOWN_PERSON_DIR = "Unknown_Person"
# how long a face must stay "Unknown" before we start photographing
UNKNOWN_CONFIRM_SECONDS = 3
PHOTO_DELAY = 10              # min seconds between saved photos of an unknown person
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

os.makedirs(UNKNOWN_PERSON_DIR, exist_ok=True)

# --------------------------------
# Initialize Modules
# --------------------------------
face_ai = FaceRecognizer()
object_ai = ObjectDetector()
dashboard = Dashboard()
relationship_ai = RelationshipDetector()
zone_editor = ZoneEditor()

# --------------------------------
# Open Webcam
# --------------------------------
cap = cv2.VideoCapture(0)
cv2.namedWindow("AI BABY SECURITY SYSTEM")
cv2.setMouseCallback(
    "AI BABY SECURITY SYSTEM",
    zone_editor.mouse_callback
)
if not cap.isOpened():
    raise RuntimeError(
        "Could not open webcam (index 0). Check that it's connected and not in use.")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

unknown_start_time = None
last_photo_time = 0.0
prev_time = time.time()

# --------------------------------
# Start Flask Server
# --------------------------------
flask_thread = Thread(
    target=lambda: app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    ),
    daemon=True
)

flask_thread.start()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to read frame from camera; stopping.")
            break

        current_time = time.time()

        # --------------------------------
        # Detection
        # --------------------------------
        faces = face_ai.recognize(frame)
        objects = object_ai.detect(frame)
        relationships = relationship_ai.detect(faces, objects)


        # --------------------------------
        # Bed Zone Detection
        # --------------------------------
        for obj in objects:

            if obj["name"] == "person":

                if zone_editor.is_inside("bed", obj["box"]):

                    logger.add_event("Person On Bed")

        # --------------------------------
        # Log Known-Face and Relationship Events
        # --------------------------------
        for face in faces:
            if face["name"] != "Unknown":
                logger.add_event(f"{face['name']} Detected")

        for event in relationships:
            logger.add_event(event)

        # --------------------------------
        # Draw Face Boxes + Unknown-Person Photo Capture
        # --------------------------------
        any_unknown = False

        for face in faces:
            x, y, w, h = face["box"]

            cv2.rectangle(frame, (x, y), (x + w, y + h), face["color"], 2)
            cv2.rectangle(frame, (x, y - 35), (x + w, y), face["color"], -1)
            cv2.putText(
                frame,
                face["name"],
                (x + 5, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            if face["name"] == "Unknown":
                any_unknown = True

                if unknown_start_time is None:
                    unknown_start_time = current_time

                confirmed = current_time - unknown_start_time >= UNKNOWN_CONFIRM_SECONDS
                cooldown_ok = current_time - last_photo_time >= PHOTO_DELAY

                if confirmed and cooldown_ok:
                    filename = "Unknown_" + \
                        time.strftime("%Y%m%d_%H%M%S") + ".jpg"

                    # Copy the frame so the live display isn't changed
                    saved_frame = frame.copy()

                    # Highlight the unknown person
                    cv2.rectangle(
                        saved_frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 0, 255),
                        3
                    )

                    cv2.putText(
                        saved_frame,
                        "UNKNOWN PERSON",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )

                    filepath = os.path.join(
                        UNKNOWN_PERSON_DIR,
                        filename
                    )

                    cv2.imwrite(filepath, saved_frame)

                    logger.add_event(f"Unknown Photo Saved : {filename}")

                    last_photo_time = current_time

        # Reset the "how long has someone been unknown" timer only once
        # nobody unknown is in frame at all.
        if not any_unknown:
            unknown_start_time = None

        # --------------------------------
        # Draw Object Boxes
        # --------------------------------
        for obj in objects:
            x1, y1, x2, y2 = obj["box"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                obj["name"],
                (x1, y1 - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # --------------------------------
        # FPS Calculation
        # --------------------------------
        elapsed = current_time - prev_time
        fps = int(1 / elapsed) if elapsed > 0 else 0
        prev_time = current_time

        # --------------------------------
        # Dashboard
        # --------------------------------
        frame = dashboard.draw(
            frame,
            len(faces),
            len(objects),
            fps,
            logger.get_events()
        )

        # --------------------------------
        # Show Window
        # --------------------------------
        frame = zone_editor.draw(frame)
        # Share latest AI frame with Flask
        shared_frame.latest_frame = frame.copy()
        cv2.imshow("AI BABY SECURITY SYSTEM", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("b"):
            zone_editor.current_zone = "bed"

        elif key == ord("d"):
            zone_editor.current_zone = "door"

        elif key == ord("p"):
            zone_editor.current_zone = "play"

        elif key == ord("w"):
            zone_editor.current_zone = "wardrobe"

        elif key == ord("s"):
            zone_editor.save()

        elif key == ord("c"):

            zone_editor.zones[zone_editor.current_zone] = None

            zone_editor.save()      # <-- Save immediately

            print(f"{zone_editor.current_zone.capitalize()} Zone Deleted") 

        elif key == ord("x"):

            zone_editor.zones = {
                "bed": None,
                "door": None,
                "play": None,
                "wardrobe": None
            }

            zone_editor.save()      # <-- Save immediately

            print("All Zones Deleted")
        elif key == ord("q"):
            break

finally:
    # --------------------------------
    # Cleanup (always runs, even on error)
    # --------------------------------
    cap.release()
    cv2.destroyAllWindows()
