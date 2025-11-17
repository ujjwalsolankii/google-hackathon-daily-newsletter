import feedparser

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en",
]

def fetch_top_items(max_items=5):
    items = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:max_items]:
            items.append({
                "title": entry.title,
                "summary": entry.summary if hasattr(entry, "summary") else "",
                "link": entry.link
            })
        if len(items) >= max_items:
            break
    return items[:max_items]
