from typing import List
import uuid
from models import CitySummary, MeetingSummary, Meeting

class Datastore:
    def __init__(self, db_url: str):
        self.cities = []
        self.meetings = []
        pass

    def get_all_city_summaries(self) -> List[CitySummary]:
        return self.cities

    def get_all_meetings(self, city_id: uuid.UUID) -> List[MeetingSummary]:
        return [meeting for meeting in self.meetings if meeting.city_id == city_id]

    def get_meeting(self, meeting_id: uuid.UUID) -> Meeting:
        for meeting in self.meetings:
            if meeting.meeting_id == meeting_id:
                return meeting

    def save_city(self, city: CitySummary):
        self.cities.append(city)

    def save_meeting(self, meeting: Meeting):
        self.meetings.append(meeting)
