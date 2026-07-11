import cv2
import pickle
from sklearn.neighbors import KNeighborsClassifier


class FaceRecognizer:

    def __init__(self):

        # Load Haar Cascade
        self.face_detector = cv2.CascadeClassifier(
            "models/haarcascade_frontalface_default.xml"
        )

        # Load Face Data
        with open("models/names.pkl", "rb") as f:
            self.labels = pickle.load(f)

        with open("models/faces_data.pkl", "rb") as f:
            self.faces = pickle.load(f)

        # Train KNN
        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.knn.fit(self.faces, self.labels)

        self.threshold = 3500

    def recognize(self, frame):

        results = []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            face = frame[y:y+h, x:x+w]

            face = cv2.resize(face, (50, 50))

            face = face.flatten().reshape(1, -1)

            distances, _ = self.knn.kneighbors(face)

            distance = distances[0][0]

            if distance > self.threshold:
                name = "Unknown"
                color = (0, 0, 255)
            else:
                name = self.knn.predict(face)[0]
                color = (255, 120, 0)

            results.append({
                "name": name,
                "box": (x, y, w, h),
                "color": color,
                "distance": distance
            })

        return results