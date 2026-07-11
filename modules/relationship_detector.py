class RelationshipDetector:

    def __init__(self):
        pass

    def is_inside(self, person_box, object_box):

        px1, py1, px2, py2 = person_box
        ox1, oy1, ox2, oy2 = object_box

        object_center_x = (ox1 + ox2) // 2
        object_center_y = (oy1 + oy2) // 2

        return (
            px1 <= object_center_x <= px2 and
            py1 <= object_center_y <= py2
        )

    def detect(self, faces, objects):

        events = []

        # Find YOLO person
        persons = [obj for obj in objects if obj["name"] == "person"]

        for face in faces:

            fx, fy, fw, fh = face["box"]

            face_center_x = fx + fw // 2
            face_center_y = fy + fh // 2

            nearest_person = None
            min_distance = 999999

            # Match face to nearest person
            for person in persons:

                px1, py1, px2, py2 = person["box"]

                person_center_x = (px1 + px2) // 2
                person_center_y = (py1 + py2) // 2

                distance = ((face_center_x - person_center_x) ** 2 +
                            (face_center_y - person_center_y) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    nearest_person = person

            if nearest_person is None:
                continue

            person_box = nearest_person["box"]

            # Check every object
            for obj in objects:

                if obj["name"] == "person":
                    continue

                if self.is_inside(person_box, obj["box"]):

                    if obj["name"] == "cell phone":
                        events.append(f'{face["name"]} Holding Phone')

                    elif obj["name"] == "bottle":
                        events.append(f'{face["name"]} Holding Bottle')

                    elif obj["name"] == "laptop":
                        events.append(f'{face["name"]} Using Laptop')

        return events