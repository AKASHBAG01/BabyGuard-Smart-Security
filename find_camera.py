import cv2

for i in range(10):
    print(f"Testing camera {i}...")

    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)

    if cap.isOpened():
        ret, frame = cap.read()

        if ret:
            print(f"✅ Camera found at index {i}")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow(f"Camera {i}", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()