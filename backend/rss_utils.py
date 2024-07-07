import feedparser
import time

# Get all URLs from a feed
def get_all_links(feed_url: str):
    feed = feedparser.parse(feed_url)
    return [{ 'link': entry.link, 'date': int(time.mktime(entry.published_parsed)) } for entry in feed.entries]