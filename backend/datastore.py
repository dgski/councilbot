import json
from typing import List, Set
import uuid
from models import CitySummary, MeetingSummary, Meeting

from databases import Database

# Helper that parses the JSON data from the database
def parse_data(s):
    return json.loads(s['data'])

# Datastore class that interacts with an SQL database
# Provides methods to save and retrieve data related to cities and meetings
class Datastore:
    def __init__(self, db_url: str):
        self.cities = []
        self.meetings = []
        self.database = Database(db_url)
        pass

    async def connect(self):
        await self.database.connect()

    async def create_table(self):
        await self.database.execute('CREATE TABLE IF NOT EXISTS entity (type TEXT, id TEXT, data JSON)')

    async def get_all_city_summaries(self) -> List[CitySummary]:
        results = await self.database.fetch_all("SELECT * FROM entity WHERE type = 'city'")
        return [CitySummary(**parse_data(city)) for city in results]

    async def get_all_meetings(self, city_id: uuid.UUID) -> List[MeetingSummary]:
        results = await self.database.fetch_all(
            "SELECT * FROM entity WHERE type = 'meeting' AND data->>'city_id' = :city_id",
            {'city_id': str(city_id)})
        return [MeetingSummary(**parse_data(meeting)) for meeting in results]

    async def get_meeting(self, meeting_id: uuid.UUID) -> Meeting:
        result = await self.database.fetch_one(
            "SELECT * FROM entity WHERE type = 'meeting' AND id = :meeting_id",
            {'meeting_id': str(meeting_id)})
        return Meeting(**parse_data(result))
    
    async def get_all_links(self) -> Set[str]:
        results = await self.database.fetch_all(
            "SELECT data->>'meeting_link' AS link FROM entity WHERE type = 'meeting'")
        return set(result['link'] for result in results)

    async def save_city(self, city: CitySummary):
        await self.database.execute(
            "INSERT INTO entity (type, id, data) VALUES (:type, :id, :data)",
            {'type': 'city', 'id': str(city.city_id), 'data': city.model_dump_json()})

    async def save_meeting(self, meeting: Meeting):
        await self.database.execute(
            "INSERT INTO entity (type, id, data) VALUES (:type, :id, :data)",
            {
                'type': 'meeting', 'id': str(meeting.meeting_id),
                'data': meeting.model_dump_json()
            })