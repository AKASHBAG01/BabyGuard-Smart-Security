import datetime
import json
import os

EVENT_FILE = "database/events.json"


class EventLogger:

    def __init__(self):
        self.events = []

        os.makedirs("database", exist_ok=True)

        if os.path.exists(EVENT_FILE):
            try:
                with open(EVENT_FILE, "r") as f:
                    self.events = json.load(f)
            except Exception:
                self.events = []

    def add_event(self, message):

        now = datetime.datetime.now()

        # Remove events older than 15 minutes
        self.events = [
            event
            for event in self.events
            if (
                now - datetime.datetime.fromisoformat(event["datetime"])
            ).total_seconds() < 900
        ]

        # Ignore duplicate consecutive events
        if len(self.events) > 0:
            if self.events[-1]["message"] == message:
                return

        event = {
            "datetime": now.isoformat(),
            "time": now.strftime("%H:%M:%S"),
            "message": message
        }

        self.events.append(event)

        with open(EVENT_FILE, "w") as f:
            json.dump(self.events, f, indent=4)

    def get_events(self):
        return self.events


# Global logger object
logger = EventLogger()