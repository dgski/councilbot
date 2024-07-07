import uuid
from pydantic import BaseModel
from typing import List

class CitySummary(BaseModel):
    city_id: uuid.UUID
    city_name: str
    city_url: str

class MeetingSummary(BaseModel):
    meeting_id: uuid.UUID
    meeting_date: int
    meeting_keywords: List[str]

class MeetingSegment(BaseModel):
    start_time_seconds: int
    end_time_seconds: int
    text: str

class Meeting(BaseModel):
    meeting_id: uuid.UUID
    city_id: uuid.UUID
    meeting_date: int
    meeting_link: str
    meeting_keywords: List[str]
    meeting_segments: List[MeetingSegment]
    meeting_decisions: List[str]