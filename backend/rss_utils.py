import feedparser
import time

# Get all items from a feed that are newer than a given date
def get_all_items_newer_than(feed_url: str, date: int):
    date = time.gmtime(date)
    feed = feedparser.parse(feed_url)
    return [entry for entry in feed.entries if entry.published_parsed > date]

# Get all URLs from a feed that are newer than a given date
def get_all_urls_newer_than_date(feed_url: str, date: int):
    entries = get_all_items_newer_than(feed_url, date)
    return [entry.link for entry in entries]