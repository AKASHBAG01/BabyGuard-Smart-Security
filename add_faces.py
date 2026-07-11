import argparse
import os
import pickle
import sys

import cv2
import numpy as np

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
MODELS_DIR = "models"
CASCADE_PATH = os.path.join(MODELS_DIR, "haarcascade_frontalface_default.xml")
NAMES_PATH = os.path.join(MODELS_DIR, "names.pkl")
FACES_PATH = os.path.join(MODELS_DIR, "faces_data.pkl")

FACE_SIZE = (50, 50)          # (width, height) each face is resized to
DEFAULT_SAMPLES = 100         # how many face crops to collect
DEFAULT_FRAME_SKIP = 10       # only keep every Nth detected face
SCALE_FACTOR = 1.3
MIN_NEIGHBORS = 5


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture face samples for training.")
    parser.add_argument("--name", type=str, default=None, help="Person's name")
    parser.add_argument("--samples", type=int, default=DEFAULT_SAMPLES,
                         help="Number of face samples to capture")
    parser.add_argument("--skip", type=int, default=DEFAULT_FRAME_SKIP,
                         help="Keep every Nth detected face frame")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    return parser.parse_args()


def load_cascade(path: str) -> cv2.CascadeClassifier:
    if not os.path.isfile(path):
        sys.exit(f"[ERROR] Haar cascade not found at '{path}'. "
                  f"Download it from OpenCV's repo and place it there.")
    cascade = cv2.CascadeClassifier(path)
    if cascade.empty():
        sys.exit(f"[ERROR] Failed to load cascade classifier from '{path}' "
                  f"(file exists but is invalid).")
    return cascade


def open_camera(index: int) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        sys.exit(f"[ERROR] Could not open camera at index {index}. "
                  f"Check that it's connected and not in use by another app.")
    return cap


def capture_faces(cap: cv2.VideoCapture, cascade: cv2.CascadeClassifier,
                   n_samples: int, frame_skip: int) -> np.ndarray:
    """Runs the capture loop and returns an (n_samples, H, W, 3) uint8 array."""
    faces_data: list[np.ndarray] = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to read frame from camera; stopping capture.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_rects = cascade.detectMultiScale(
            gray, scaleFactor=SCALE_FACTOR, minNeighbors=MIN_NEIGHBORS
        )

        for (x, y, w, h) in face_rects:
            crop_img = frame[y:y + h, x:x + w]
            resized_img = cv2.resize(crop_img, FACE_SIZE)

            if len(faces_data) < n_samples and frame_count % frame_skip == 0:
                faces_data.append(resized_img)

            frame_count += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame, f"Faces Captured: {len(faces_data)}/{n_samples}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
            )

        cv2.imshow("Face Capture (press 'q' to quit)", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or len(faces_data) >= n_samples:
            break

    return np.asarray(faces_data)


def save_dataset(name: str, faces_data: np.ndarray) -> None:
    os.makedirs(MODELS_DIR, exist_ok=True)

    if faces_data.size == 0:
        print("[WARN] No faces were captured; nothing saved.")
        return

    n_captured = faces_data.shape[0]
    flat_faces = faces_data.reshape(n_captured, -1)

    # ---- names.pkl ----
    if os.path.isfile(NAMES_PATH):
        with open(NAMES_PATH, 'rb') as f:
            names = pickle.load(f)
        names.extend([name] * n_captured)
    else:
        names = [name] * n_captured

    with open(NAMES_PATH, 'wb') as f:
        pickle.dump(names, f)

    # ---- faces_data.pkl ----
    if os.path.isfile(FACES_PATH):
        with open(FACES_PATH, 'rb') as f:
            existing_faces = pickle.load(f)
        # Guard against mismatched feature dimensions (e.g. FACE_SIZE changed).
        if existing_faces.shape[1] != flat_faces.shape[1]:
            sys.exit(
                "[ERROR] Existing faces_data.pkl has a different feature size "
                f"({existing_faces.shape[1]}) than the new samples "
                f"({flat_faces.shape[1]}). Delete the old .pkl files or keep "
                "FACE_SIZE consistent."
            )
        all_faces = np.append(existing_faces, flat_faces, axis=0)
    else:
        all_faces = flat_faces

    with open(FACES_PATH, 'wb') as f:
        pickle.dump(all_faces, f)

    print(f"[OK] Saved {n_captured} samples for '{name}'. "
          f"Dataset now has {all_faces.shape[0]} total samples.")


def main() -> None:
    args = parse_args()

    name = args.name or input("Enter your name: ").strip()
    if not name:
        sys.exit("[ERROR] Name cannot be empty.")

    cascade = load_cascade(CASCADE_PATH)
    cap = open_camera(0)

    try:
        faces_data = capture_faces(cap, cascade, args.samples, args.skip)
    finally:
        cap.release()
        cv2.destroyAllWindows()

    save_dataset(name, faces_data)


if __name__ == "__main__":
    main()