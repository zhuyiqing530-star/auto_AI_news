import httpx
import feedparser
from datetime import datetime, timedelta
from time import mktime
from urllib.parse import quote_plus
from .base import BaseSource, CrawledItem

# Nitter instances for RSS
NITTER_INSTANCES = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
]

# AI-focused accounts to monitor
AI_ACCOUNTS = [
    "AnthropicAI", "OpenAI", "GoogleDeepMind",
    "kaboroevich", "swaboroevich", "ylecun",
]


class TwitterSource(BaseSource):
    """Twitter/X via Nitter RSS bridges (free, no auth)"""

    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        items = []
        cutoff = datetime.utcnow() - timedelta(hours=since_hours)

        # Try each Nitter instance
        for instance in NITTER_INSTANCES:
            if items:
                break
            # Search RSS
            for keyword in keywords[:5]:
                try:
                    url = f"{instance}/search/rss?f=tweets&q={quote_plus(keyword)}"
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:10]:
                        pub = self._parse_date(entry)
                        if pub and pub < cutoff:
                            continue
                        title = entry.get("title", "")[:200]
                        text = title.lower()
                        matched = [k for k in keywords if k.lower() in text]
                        items.append(CrawledItem(
                            title=title,
                            url=entry.get("link", "").replace(instance, "https://x.com"),
                            source="twitter",
                            content_snippet=entry.get("summary", "")[:500],
                            author=entry.get("author", ""),
                            published_at=pub or datetime.utcnow(),
                            language="en",
                            keywords_matched=matched,
                        ))
                except Exception as e:
                    print(f"[Twitter] Nitter error ({instance}): {e}")

            # Account feeds
            for account in AI_ACCOUNTS[:3]:
                try:
                    url = f"{instance}/{account}/rss"
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:5]:
                        pub = self._parse_date(entry)
                        if pub and pub < cutoff:
                            continue
                        title = entry.get("title", "")[:200]
                        text = title.lower()
                        matched = [k for k in keywords if k.lower() in text]
                        if matched:
                            items.append(CrawledItem(
                                title=title,
                                url=entry.get("link", "").replace(instance, "https://x.com"),
                                source="twitter",
                                content_snippet="",
                                author=account,
                                published_at=pub or datetime.utcnow(),
                                language="en",
                                keywords_matched=matched,
                            ))
                except Exception:
                    pass

        seen = set()
        return [i for i in items if i.url not in seen and not seen.add(i.url)]

    @staticmethod
    def _parse_date(entry) -> datetime | None:
        for field in ("published_parsed", "updated_parsed"):
            parsed = entry.get(field)
            if parsed:
                return datetime.utcfromtimestamp(mktime(parsed))
        return None
