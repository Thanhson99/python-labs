import feedparser
import json
import os

SOURCE_FILE = "data/sources.json"

def load_sources():
    """Read source list from JSON file"""
    with open(SOURCE_FILE, "r") as f:
        data = json.load(f)
    return data["sources"]

def fetch_latest_news(coin_list):
    """Fetch news from configured sources"""
    sources = load_sources()
    all_news = []

    for source in sources:
        if not source["rss"]:
            continue  # Skip sources without RSS
        
        feed = feedparser.parse(source["rss"])
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            summary = entry.get("summary", "")

            # Check whether article contains target keywords
            if any(coin in title.upper() or coin in summary.upper() for coin in coin_list):
                all_news.append({"title": title, "link": link, "summary": summary})

    return all_news
