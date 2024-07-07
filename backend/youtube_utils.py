import requests
from youtube_transcript_api import YouTubeTranscriptApi

def get_list_of_proxies() -> list:
    url = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&proxy_format=protocolipport&format=text'
    response = requests.get(url)
    return [url for url in response.text.split('\n') if url.startswith('http')]

# Get the raw transcript from a YouTube video
def get_raw_transcript(proxy_https: str, proxy_http: str, video_url: str) -> str:
    video_id = video_url.split('=')[1]
    for proxy in get_list_of_proxies():
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, proxies={"https": proxy, "http": proxy})
            return '\n'.join([str(line['start']) + 's : ' + line['text'] for line in transcript])
        except:
            continue