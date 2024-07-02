import anthropic
import instructor
from anthropic import Anthropic
from pydantic import BaseModel
from typing import List
from models import MeetingSegment
from app_logger import logger

class Meeting(BaseModel):
    segments: List[MeetingSegment]

HAIKU = "claude-3-haiku-20240307"
SONNET = "claude-3-5-sonnet-20240620"
OPUS = "claude-3-opus-20240620"

def claude_structured(key: str, system_prompt: str, user_prompt: str, model: str, response_model):
    client = instructor.from_anthropic(Anthropic(api_key=key))
    message = client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ],
        response_model=response_model
    )
    return message

def claude(key: str, system_prompt: str, user_prompt: str, model: str = HAIKU):
    client = anthropic.Anthropic(api_key=key)
    message = client.messages.create(
        model=model,
        max_tokens=4000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ]
    )
    return message.content[0].text

def summarize_meeting(key: str, transcript: str) -> str:
    return claude(
        key,
        "You are a council meeting summarizer. Always return a point form summary of the meeting with numeric details.",
        f"Can you summarize the following meeting? {transcript}")

def segment_meeting_timewise(key: str, transcript: str) -> str:
    return claude(
        key,
        "You are a council meeting segmenter. Always return a point form summary of the meeting with timing durations in seconds",
        f"Can you segment the following meeting? {transcript}",
        SONNET)

def segment_meeting_timewise_structured(key: str, transcript: str) -> Meeting:
    segments = segment_meeting_timewise(key, transcript)
    return claude_structured(
        key,
        "You are a council meeting segmenter. Always return a point form summary of the meeting with timing durations",
        f"Can you turn the following meeting into 'segments' with fields 'start_time', 'end_time', and 'text': {segments}",
        HAIKU,
        Meeting)

def keyword_extractor(key: str, transcript: str) -> str:
    return claude(
        key,
        "You are a council meeting keyword extractor. Always return a list of keywords from the meeting.",
        f"Can you extract keywords from the following meeting? {transcript}")

def keyword_extractor_structured(key: str, transcript: str) -> List[str]:
    return claude_structured(
        key,
        "You are a council meeting keyword extractor. Always return a list of keywords from the meeting.",
        f"Can you extract keywords from the following meeting? {transcript}",
        HAIKU,
        List[str])

def sentiment_analysis(key: str, transcript: str) -> str:
    return claude(
        key,
        "You are a council meeting sentiment analyzer. Always return the sentiment of the meeting.",
        f"Can you analyze the sentiment of the following meeting? {transcript}")

def decision_extractor(key:str, transcript: str) -> str:
    return claude(
        key,
        "You are a council meeting decision extractor. Always return a list of decisions made during the meeting.",
        f"Can you extract decisions from the following meeting? {transcript}")

def decision_extractor_structured(key: str, transcript: str) -> List[str]:
    return claude_structured(
        key,
        "You are a council meeting decision extractor. Just return a list of decisions made during the meeting.",
        f"Can you extract decisions from the following meeting, no preamble, no numbering? {transcript}",
        SONNET,
        List[str])

def cleaner_and_labeler(key: str, transcript: str) -> str:
    # Split transcript into chunks of 4000 characters
    chunks = [transcript[i:min(i + 4000, len(transcript))] for i in range(0, len(transcript), 4000)]
    cleaned_transcript = ""
    for chunk in chunks:
        cleaned_transcript += claude(
            key,
            "You are a council meeting cleaner and speaker labeler. Always return a cleaned version of the meeting transcript including speakers and times.",
            f"Can you clean and label the following meeting? {chunk}")
    return cleaned_transcript

def extract_meeting_info(key: str, transcript: str):
    segments = segment_meeting_timewise_structured(key, transcript)
    logger.info(f"Got segments")
    keywords = keyword_extractor_structured(key, transcript)
    logger.info(f"Got keywords")
    decisions = decision_extractor_structured(key, transcript)
    logger.info(f"Got decisions")
    summary = summarize_meeting(key, transcript)
    logger.info(f"Got summary")
    return {
        "segments": segments,
        "keywords": keywords,
        "decisions": decisions,
        "summary": summary
    }