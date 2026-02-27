import feedparser
from datetime import datetime, timedelta
from time import mktime
from .base import BaseSource, CrawledItem

# AI-related RSS feeds
FEEDS = [
    ("https://hnrss.org/newest?q=AI", "en"),
    ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "en"),
    ("https://feeds.arstechnica.com/arstechnica/technology-lab", "en"),
    ("https://blog.anthropic.com/rss.xml", "en"),
    ("https://openai.com/blog/rss.xml", "en"),
    ("https://rsshub.app/36kr/motif/ai", "zh"),
]


class RSSSource(BaseSource):
    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        items = []
        cutoff = datetime.utcnow() - timedelta(hours=since_hours)

        for feed_url, lang in FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:30]:
                    pub = self._parse_date(entry)
                    if pub and pub < cutoff:
                        continue

                    title = entry.get("title", "")
                    summary = entry.get("summary", "")[:500]
                    text = (title + " " + summary).lower()
                    matched = [k for k in keywords if k.lower() in text]

                    if not matched:
                        continue

                    items.append(CrawledItem(
                        title=title,
                        url=entry.get("link", ""),
                        source="rss",
                        content_snippet=summary,
                        author=entry.get("author", ""),
                        published_at=pub or datetime.utcnow(),
                        language=lang,
                        keywords_matched=matched,
                    ))
            except Exception as e:
                print(f"[RSS] Error parsing {feed_url}: {e}")

        seen = set()
        unique = []
        for item in items:
            if item.url not in seen:
                seen.add(item.url)
                unique.append(item)
        return unique

    @staticmethod
    def _parse_date(entry) -> datetime | None:
        for field in ("published_parsed", "updated_parsed"):
            parsed = entry.get(field)
            if parsed:
                return datetime.utcfromtimestamp(mktime(parsed))
        return None
