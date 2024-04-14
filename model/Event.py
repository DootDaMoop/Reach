import datetime

class Event:
    def __init__(self, event_name: str, event_id: int, event_description: str, start_date: datetime, end_date: datetime, host_user_id: int):
        self.event_name = event_name
        self.event_id = event_id
        self.event_description = event_description
        self.start_date = start_date
        self.end_date = end_date
        self.group_ids = set()
        self.user_ids = set()