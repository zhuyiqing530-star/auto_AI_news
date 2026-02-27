import httpx
from datetime import datetime, timedelta
from .base import BaseSource, CrawledItem


class GitHubSource(BaseSource):
    """GitHub Search API + trending"""
    SEARCH_URL = "https://api.github.com/search/repositories"

    def __init__(self, token: str = ""):
        self.headers = {"Accept": "application/vnd.github+json"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        items = []
        since = (datetime.utcnow() - timedelta(hours=since_hours)).strftime("%Y-%m-%d")

        for keyword in keywords[:6]:
            try:
                resp = httpx.get(self.SEARCH_URL, params={
                    "q": f"{keyword} created:>{since}",
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 10,
                }, headers=self.headers, timeout=15)
                resp.raise_for_status()

                for repo in resp.json().get("items", []):
                    title = repo["full_name"]
                    desc = repo.get("description") or ""
                    text = (title + " " + desc).lower()
                    matched = [k for k in keywords if k.lower() in text]

                    items.append(CrawledItem(
                        title=f"{title} - {desc[:100]}",
                        url=repo["html_url"],
                        source="github",
                        content_snippet=desc[:500],
                        author=repo["owner"]["login"],
                        published_at=datetime.fromisoformat(
                            repo["created_at"].replace("Z", "+00:00")
                        ).replace(tzinfo=None),
                        engagement=repo.get("stargazers_count", 0),
                        language="en",
                        keywords_matched=matched,
                    ))
                import time; time.sleep(2)
            except Exception as e:
                print(f"[GitHub] Error fetching '{keyword}': {e}")

        seen = set()
        return [i for i in items if i.url not in seen and not seen.add(i.url)]
