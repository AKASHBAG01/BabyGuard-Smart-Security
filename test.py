import argparse
import os
import pickle
import sys

import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
MODELS_DIR = "models"
CASCADE_PATH = os.path.join(MODELS_DIR, "haarcascade_frontalface_default.xml")
NAMES_PATH = os.path.join(MODELS_DIR, "names.pkl")
FACES_PATH = os.path.join(MODELS_DIR, "faces_data.pkl")

FACE_SIZE = (50, 50)
DEFAULT_THRESHOLD = 3500.0   # distance above which a face is "Unknown"
DEFAULT_K = 5
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5

KNOWN_COLOR = (255, 120, 0)   # BGR - blue-ish
UNKNOWN_COLOR = (0, 0, 255)   # BGR - red


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real-time face recognition.")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                         help="Max nearest-neighbour distance to accept a match")
    parser.add_argument("--k", type=int, default=DEFAULT_K,
                         help="Number of neighbours for KNN")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    return parser.parse_args()


def load_cascade(path: str) -> cv2.CascadeClassifier:
    if not os.path.isfile(path):
        sys.exit(f"[ERROR] Haar cascade not found at '{path}'.")
    cascade = cv2.CascadeClassifier(path)
    if cascade.empty():
        sys.exit(f"[ERROR] Failed to load cascade classifier from '{path}'.")
    return cascade


def load_dataset() -> tuple[np.ndarray, list]:
    if not os.path.isfile(NAMES_PATH) or not os.path.isfile(FACES_PATH):
        sys.exit(
            "[ERROR] No trained dataset found. Run add_faces.py first to "
            f"create '{NAMES_PATH}' and '{FACES_PATH}'."
        )

    with open(NAMES_PATH, 'rb') as f:
        labels = pickle.load(f)
    with open(FACES_PATH, 'rb') as f:
        faces = pickle.load(f)

    if len(labels) != faces.shape[0]:
        sys.exit(
            f"[ERROR] Mismatch between number of labels ({len(labels)}) and "
            f"number of face samples ({faces.shape[0]}). Dataset is corrupted."
        )

    return faces, labels


def open_camera(index: int) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        sys.exit(f"[ERROR] Could not open camera at index {index}.")
    return cap


def run_recognition(cap: cv2.VideoCapture, cascade: cv2.CascadeClassifier,
                     knn: KNeighborsClassifier, threshold: float) -> None:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to read frame from camera; stopping.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = cascade.detectMultiScale(
            gray, scaleFactor=SCALE_FACTOR, minNeighbors=MIN_NEIGHBORS
        )

        for (x, y, w, h) in face_rects:
            crop_img = frame[y:y + h, x:x + w]
            resized_img = cv2.resize(crop_img, FACE_SIZE).flatten().reshape(1, -1)

            distances, _ = knn.kneighbors(resized_img)
            distance = distances[0][0]

            if distance > threshold:
                name = "Unknown"
                box_color = UNKNOWN_COLOR
            else:
                name = str(knn.predict(resized_img)[0])
                box_color = KNOWN_COLOR

            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
            cv2.rectangle(frame, (x, y - 35), (x + w, y), box_color, -1)
            cv2.putText(
                frame, name, (x + 8, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
            )

        cv2.imshow("Face Recognition System (press 'q' to quit)", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break


def main() -> None:
    args = parse_args()

    cascade = load_cascade(CASCADE_PATH)
    faces, labels = load_dataset()

    n_neighbors = min(args.k, len(labels))  # avoid crash if dataset is tiny
    if n_neighbors < args.k:
        print(f"[WARN] Only {len(labels)} samples available; "
              f"reducing k from {args.k} to {n_neighbors}.")

    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(faces, labels)

    cap = open_camera(args.camera)
    try:
        run_recognition(cap, cascade, knn, args.threshold)
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()