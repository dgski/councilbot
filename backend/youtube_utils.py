import asyncio
from random import shuffle
import requests
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptAvailable, NoTranscriptFound, TranscriptsDisabled
from app_logger import logger

# Get a list of proxies that may be able to bypass YouTube's rate limiting
def get_list_of_proxies() -> list:
    url = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text'
    response = requests.get(url)
    return [url.strip() for url in response.text.split('\n') if url.startswith('http')]

# Get the raw transcript from a YouTube video
async def get_raw_transcript(video_url: str) -> str:
    video_id = video_url.split('=')[1]
    proxies = get_list_of_proxies()
    shuffle(proxies)
    for proxy in proxies:
        logger.info(f"Trying proxy {proxy}")
        try:
            
            transcript = await asyncio.wait_for(asyncio.to_thread(lambda: YouTubeTranscriptApi.get_transcript(
                video_id, proxies={"socks5": proxy})),
                timeout=5)
            return '\n'.join([str(line['start']) + 's : ' + line['text'] for line in transcript])
        except (NoTranscriptAvailable, NoTranscriptFound, TranscriptsDisabled) as e:
            logger.error(f"No transcript found: {e}")
            break
        except asyncio.TimeoutError:
            logger.error(f"Timeout error")
            await asyncio.sleep(1)
            continue
        except Exception as e:
            logger.error(f"General error: {e}")
            await asyncio.sleep(1)
            continue
    return ""