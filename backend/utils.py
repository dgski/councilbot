import asyncio
from app_logger import logger
import uuid
from models import Meeting
import ai_utils

async def create_meeting(claude_key: str, meeting_id: uuid.UUID, city_id: uuid.UUID, meeting_date: str, meeting_link: str, meeting_transcript: str) -> Meeting:
    for model in (ai_utils.HAIKU, ai_utils.SONNET):
        try:
            logger.info(f'Trying model {model}')
            logger.info(f'Got meeting transcript length={len(meeting_transcript)}')
            meeting_info = await ai_utils.extract_meeting_info(claude_key, meeting_transcript, model)
            logger.info(f'Extracted meeting info')
            meeting = Meeting(
                meeting_id = meeting_id,
                city_id = city_id,
                meeting_date = meeting_date,
                meeting_link = meeting_link,
                meeting_keywords = meeting_info['keywords'],
                meeting_segments = meeting_info['segments'],
                meeting_decisions = meeting_info['decisions'])
            return meeting
        except Exception as e:
            logger.error(f'Error extracting meeting info: {e}')
            await asyncio.sleep(20)
