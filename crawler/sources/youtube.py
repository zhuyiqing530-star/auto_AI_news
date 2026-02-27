import httpx
from datetime import datetime, timedelta
from .base import BaseSource, CrawledItem


class YouTubeSource(BaseSource):
    """YouTube Data API v3 - requires YOUTUBE_API_KEY in .env"""
    API_URL = "https://www.googleapis.com/youtube/v3/search"

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        if not self.api_key:
            print("[YouTube] No API key configured, skipping")
            return []

        items = []
        since = (datetime.utcnow() - timedelta(hours=since_hours)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Batch keywords to save quota (100 units per search)
        batches = [keywords[i:i+3] for i in range(0, len(keywords), 3)]

        for batch in batches[:5]:  # max 5 searches per cycle
            query = " | ".join(batch)
            try:
                resp = httpx.get(self.API_URL, params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "order": "date",
                    "publishedAfter": since,
                    "maxResults": 15,
                    "key": self.api_key,
                }, timeout=15)
                resp.raise_for_status()
                data = resp.json()

                for item in data.get("items", []):
                    snippet = item["snippet"]
                    vid = item["id"]["videoId"]
                    title = snippet.get("title", "")
                    desc = snippet.get("description", "")
                    text = (title + " " + desc).lower()
                    matched = [k for k in keywords if k.lower() in text]

                    items.append(CrawledItem(
                        title=title,
                        url=f"https://youtube.com/watch?v={vid}",
                        source="youtube",
                        content_snippet=desc[:500],
                        author=snippet.get("channelTitle", ""),
                        published_at=datetime.fromisoformat(
                            snippet["publishedAt"].replace("Z", "+00:00")
                        ).replace(tzinfo=None),
                        language="en",
                        keywords_matched=matched,
                    ))
            except Exception as e:
                print(f"[YouTube] Error: {e}")

        seen = set()
        return [i for i in items if i.url not in seen and not seen.add(i.url)]
