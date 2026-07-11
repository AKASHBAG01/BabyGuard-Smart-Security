from ultralytics import YOLO


class ObjectDetector:

    def __init__(self):

        self.model = YOLO("models/yolov8n.pt")

    def detect(self, frame):

        detections = []

        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=0.5,
            verbose=False
        )

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                class_id = int(box.cls[0])

                object_name = self.model.names[class_id]

                # Tracking ID
                if box.id is not None:
                    track_id = int(box.id[0])
                else:
                    track_id = -1

                detections.append({
                    "id": track_id,
                    "name": object_name,
                    "box": (x1, y1, x2, y2),
                    "confidence": confidence
                })

        return detections