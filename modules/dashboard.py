import cv2
import datetime


class Dashboard:

    def __init__(self):
        self.title = "AI BABY SECURITY SYSTEM"

    def draw(self, frame, faces, objects, fps, events):

        h, w = frame.shape[:2]

        # ---------- Header ----------
        cv2.rectangle(frame, (0, 0), (w, 70), (35, 35, 35), -1)

        cv2.putText(
            frame,
            self.title,
            (20, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        # ---------- Live ----------
        cv2.circle(frame, (w - 200, 30), 8, (0, 0, 255), -1)

        cv2.putText(
            frame,
            "LIVE",
            (w - 180, 36),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # ---------- Information Panel ----------
        cv2.rectangle(frame, (0, 70), (260, h), (45, 45, 45), -1)

        cv2.putText(frame, "STATUS", (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.putText(frame, "SAFE", (30, 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.putText(frame, f"Faces : {faces}", (20, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(frame, f"Objects : {objects}", (20, 230),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(frame, f"FPS : {fps}", (20, 270),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        now = datetime.datetime.now()

        cv2.putText(frame,
                    now.strftime("%d-%m-%Y"),
                    (20, 320),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2)

        cv2.putText(frame,
                    now.strftime("%H:%M:%S"),
                    (20, 360),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2)

        # ---------- Events ----------
        cv2.putText(
            frame,
            "EVENTS",
            (20, 430),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        y = 470

        for event in events:

            text = f"{event['time']}  {event['message']}"

            cv2.putText(
                frame,
                text,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            y += 30

        return frame