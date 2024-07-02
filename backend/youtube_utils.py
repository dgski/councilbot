from youtube_transcript_api import YouTubeTranscriptApi

# Get the raw transcript from a YouTube video
def get_raw_transcript(video_url: str) -> str:
    video_id = video_url.split('=')[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return '\n'.join([str(line['start']) + 's : ' + line['text'] for line in transcript])
