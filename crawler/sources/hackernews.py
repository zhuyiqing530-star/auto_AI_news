import httpx
from datetime import datetime, timedelta
from .base import BaseSource, CrawledItem


class HackerNewsSource(BaseSource):
    API_URL = "https://hn.algolia.com/api/v1/search"

    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        items = []
        since_ts = int((datetime.utcnow() - timedelta(hours=since_hours)).timestamp())

        for keyword in keywords:
            try:
                resp = httpx.get(
                    self.API_URL,
                    params={
                        "query": keyword,
                        "tags": "story",
                        "numericFilters": f"created_at_i>{since_ts}",
                        "hitsPerPage": 20,
                    },
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()

                for hit in data.get("hits", []):
                    url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
                    matched = [k for k in keywords if k.lower() in (hit.get("title", "") + " " + (hit.get("story_text") or "")).lower()]

                    items.append(CrawledItem(
                        title=hit.get("title", ""),
                        url=url,
                        source="hackernews",
                        content_snippet=(hit.get("story_text") or "")[:500],
                        author=hit.get("author", ""),
                        published_at=datetime.utcfromtimestamp(hit.get("created_at_i", 0)),
                        engagement=hit.get("points", 0),
                        language="en",
                        keywords_matched=matched,
                    ))
            except Exception as e:
                print(f"[HN] Error fetching '{keyword}': {e}")

        # Deduplicate by URL
        seen = set()
        unique = []
        for item in items:
            if item.url not in seen:
                seen.add(item.url)
                unique.append(item)
        return unique
