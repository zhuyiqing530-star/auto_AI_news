import httpx
from datetime import datetime, timedelta
from .base import BaseSource, CrawledItem


class RedditSource(BaseSource):
    """Reddit search via JSON API (no auth needed for basic search)"""
    SEARCH_URL = "https://www.reddit.com/search.json"
    SUBREDDITS = [
        "artificial", "MachineLearning", "LocalLLaMA",
        "ClaudeAI", "ChatGPT", "singularity",
    ]

    HEADERS = {"User-Agent": "ai-news-aggregator/1.0"}

    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        items = []
        cutoff = datetime.utcnow() - timedelta(hours=since_hours)

        for keyword in keywords[:8]:
            try:
                resp = httpx.get(self.SEARCH_URL, params={
                    "q": keyword,
                    "sort": "new",
                    "t": "week",
                    "limit": 15,
                }, headers=self.HEADERS, timeout=15)
                resp.raise_for_status()
                data = resp.json()

                for post in data.get("data", {}).get("children", []):
                    d = post["data"]
                    pub = datetime.utcfromtimestamp(d.get("created_utc", 0))
                    if pub < cutoff:
                        continue

                    title = d.get("title", "")
                    selftext = d.get("selftext", "")[:500]
                    text = (title + " " + selftext).lower()
                    matched = [k for k in keywords if k.lower() in text]

                    items.append(CrawledItem(
                        title=title,
                        url=f"https://reddit.com{d.get('permalink', '')}",
                        source="reddit",
                        content_snippet=selftext,
                        author=d.get("author", ""),
                        published_at=pub,
                        engagement=d.get("score", 0),
                        language="en",
                        keywords_matched=matched,
                    ))
                import time; time.sleep(2)
            except Exception as e:
                print(f"[Reddit] Error fetching '{keyword}': {e}")

        seen = set()
        return [i for i in items if i.url not in seen and not seen.add(i.url)]
