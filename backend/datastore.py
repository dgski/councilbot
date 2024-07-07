import time
from typing import List, Set
import uuid
from models import CitySummary, MeetingSummary, Meeting

class Datastore:
    def __init__(self, db_url: str):
        self.cities = []
        self.meetings = []
        pass

    async def get_all_city_summaries(self) -> List[CitySummary]:
        return self.cities

    async def get_all_meetings(self, city_id: uuid.UUID) -> List[MeetingSummary]:
        return [meeting for meeting in self.meetings if meeting.city_id == city_id]

    async def get_meeting(self, meeting_id: uuid.UUID) -> Meeting:
        for meeting in self.meetings:
            if meeting.meeting_id == meeting_id:
                return meeting
    
    async def get_all_links(self) -> Set[str]:
        return {meeting.link for meeting in self.meetings}

    async def save_city(self, city: CitySummary):
        self.cities.append(city)

    async def save_meeting(self, meeting: Meeting):
        self.meetings.append(meeting)