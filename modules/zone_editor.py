from matplotlib.pyplot import box

import cv2
import json
import os


class ZoneEditor:

    def __init__(self):

        self.start_point = None
        self.end_point = None

        self.drawing = False

        self.current_zone = "bed"

        self.zones = {
            "bed": None,
            "door": None,
            "play": None,
            "wardrobe": None
        }

        self.load()

    def mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            self.start_point = (x, y)
            self.drawing = True

        elif event == cv2.EVENT_MOUSEMOVE:

            if self.drawing:
                self.end_point = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:

            self.end_point = (x, y)
            self.drawing = False

            x1 = min(self.start_point[0], self.end_point[0])
            y1 = min(self.start_point[1], self.end_point[1])

            x2 = max(self.start_point[0], self.end_point[0])
            y2 = max(self.start_point[1], self.end_point[1])

            self.zones[self.current_zone] = [x1, y1, x2, y2]

    def draw(self, frame):

        colors = {
            "bed": (255,0,255),
            "door": (0,255,255),
            "play": (255,255,0),
            "wardrobe": (0,165,255)
        }

        for name, zone in self.zones.items():

            if zone is None:
                continue

            x1,y1,x2,y2 = zone

            cv2.rectangle(
                frame,
                (x1,y1),
                (x2,y2),
                colors[name],
                2
            )

            cv2.putText(
                frame,
                name.upper(),
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                colors[name],
                2
            )

        if self.drawing and self.start_point and self.end_point:

            cv2.rectangle(
                frame,
                self.start_point,
                self.end_point,
                (255,255,255),
                2
            )

        return frame

    def save(self):

        with open("zones.json","w") as f:
            json.dump(self.zones,f,indent=4)

        print("Zones Saved")

    def load(self):

        if os.path.exists("zones.json"):

            with open("zones.json","r") as f:

                self.zones=json.load(f)

    def is_inside(self, zone_name, box):

        if self.zones[zone_name] is None:
            return False

        zx1, zy1, zx2, zy2 = self.zones[zone_name]

        x1, y1, x2, y2 = box

        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        return (
            zx1 <= center_x <= zx2 and
            zy1 <= center_y <= zy2
        )   