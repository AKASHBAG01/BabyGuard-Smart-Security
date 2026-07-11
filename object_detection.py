from ultralytics import YOLO
import cv2

# Load YOLO Model
model = YOLO("models/yolov8n.pt")

# Open Webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Run YOLO
    results = model(frame, conf=0.5)

    # Get Annotated Frame
    annotated_frame = results[0].plot()

    # Print Detected Objects
    for result in results:
        for box in result.boxes:

            cls = int(box.cls[0])
            confidence = float(box.conf[0])

            object_name = model.names[cls]

            print(f"{object_name} : {confidence:.2f}")

    # Count Objects
    total_objects = len(results[0].boxes)

    cv2.putText(
        annotated_frame,
        f"Objects : {total_objects}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.imshow("YOLO Object Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()