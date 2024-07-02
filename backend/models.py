from pydantic import BaseModel
from typing import List

class CitySummary(BaseModel):
    city_id: int
    city_name: str
    city_url: str

class MeetingSummary(BaseModel):
    meeting_id: int
    meeting_date: int
    meeting_title: str
    meeting_keywords: List[str]

class Meeting(BaseModel):
    meeting_id: int
    meeting_date: int
    meeting_title: str
    meeting_keywords: List[str]
    meeting_segments: List[str]
    meeting_decisions: List[str]