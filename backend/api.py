# External dependencies
import base64
import json
from os import environ
import time
import uuid
from fastapi import Request, Response
from fastapi import FastAPI, Depends
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import List

import uvicorn

# Internal dependencies
from app_logger import logger
import web_utils
import rss_utils
import youtube_utils
import ai_utils
from models import CitySummary, MeetingSummary, Meeting
from datastore import Datastore

# Get configuration from environment variable
CONFIG = environ.get('CONFIG')
decoded = str(base64.b64decode(bytes(CONFIG, 'utf-8')), 'utf-8')
config = json.loads(decoded)
HOST = config['host']
PORT = config['port']
CRONSERVICE_URL = config['cronservice_url']
CLAUDE_KEY = config['claude_key']
DATABASE_STR = config['db_url']

# Connect to the database
DB = Datastore(DATABASE_STR)
DB.save_city(CitySummary(city_id=uuid.uuid4(), city_name='Waterloo', city_url='https://www.youtube.com/feeds/videos.xml?channel_id=UCVP6QGtoGy5jmMkKhE3FRPA'))

# Set up the app and rate limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(debug=True)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware with dynamically calculated allowed origins
@app.middleware("http")
async def add_custom_cors_headers(request : Request, call_next):
    allowed_origins = web_utils.get_allowed_origins(request.headers.get("origin"))
    response = Response(content=None, status_code=204)  # No Content
    if request.method != "OPTIONS":
        response = await call_next(request)
    response.headers["access-control-allow-origin"] = ",".join(allowed_origins)
    response.headers["access-control-allow-credentials"] = "true"
    response.headers["access-control-allow-methods"] = "GET, POST, OPTIONS, PUT, DELETE"
    response.headers["access-control-allow-headers"]  = "*"
    return response

############################################
# Data endpoints
############################################

@app.get('/cities')
async def cities() -> List[CitySummary]:
    return DB.get_all_city_summaries()

@app.get('/meetings')
async def meetings(city_id: uuid.UUID) -> List[MeetingSummary]:
    return DB.get_all_meetings(city_id)

@app.get('/meeting/{meeting_id}')
async def meeting(meeting_id: uuid.UUID) -> Meeting:
    return DB.get_meeting(meeting_id)

############################################
# Job endpoints
############################################

@app.get('/jobs/download')
# async def download(valid_token = Depends(lambda x: web_utils.get_valid_token(CRONSERVICE_URL, x))):
async def download(valid_token: str):
    last_meeting_date = DB.get_last_meeting_date()
    all_cities = DB.get_all_city_summaries()
    logger.info(f'Last meeting date: {last_meeting_date} city_count: {len(all_cities)}')
    for city in all_cities:
        new_meetings = rss_utils.get_all_newer_than_date(city.city_url, last_meeting_date)
        logger.info(f'City {city.city_name} new_meetings: {len(new_meetings)}')
        for meeting in new_meetings:
            logger.info(f"Processing meeting {meeting['link']}")
            try:
                meeting_id = uuid.uuid4()
                meeting_transcript = youtube_utils.get_raw_transcript(meeting['link'])
                logger.info(f'Got meeting transcript length={len(meeting_transcript)}')
                meeting_info = ai_utils.extract_meeting_info(CLAUDE_KEY, meeting_transcript)
                logger.info(f'Extracted meeting info')
                meeting = Meeting(
                    meeting_id = meeting_id,
                    city_id = city.city_id,
                    meeting_date = meeting['date'],
                    meeting_keywords = meeting_info['keywords'],
                    meeting_segments = meeting_info['segments'],
                    meeting_decisions = meeting_info['decisions']
                )
                DB.save_meeting(meeting)
            except Exception as e:
                logger.error(f'Error processing meeting {meeting}: {e}')
    return {}

uvicorn.run(app, host=HOST, port=PORT)