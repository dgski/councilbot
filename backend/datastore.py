from typing import List
from models import CitySummary, MeetingSummary, Meeting

class Datastore:
    def __init__(self, db_url: str):
        pass

    def get_all_city_summaries(self) -> List[CitySummary]:
        []

    def get_all_meetings(self, city_id: int) -> List[MeetingSummary]:
        []

    def get_meeting(self, meeting_id: int) -> Meeting:
        Meeting(meeting_id=1, meeting_date=1, meeting_title='title', meeting_keywords=['keyword'], meeting_segments=['segment'], meeting_decisions=['decision'])

    def save_meeting(self, meeting: Meeting):
        pass
