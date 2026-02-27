import httpx
import os
from datetime import datetime, timedelta
from .base import BaseSource, CrawledItem


class ProductHuntSource(BaseSource):
    """Product Hunt via official API v2 (requires Developer Token)"""
    API_URL = "https://api.producthunt.com/v2/api/graphql"

    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        token = os.getenv("PRODUCTHUNT_TOKEN", "")
        if not token:
            print("[ProductHunt] No API token configured, skipping")
            return []

        items = []
        cutoff = datetime.utcnow() - timedelta(hours=since_hours)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        for keyword in keywords[:4]:
            try:
                resp = httpx.post(self.API_URL, json={
                    "query": """query($topic: String!) {
                        posts(topic: $topic, order: NEWEST, first: 10) {
                            edges { node {
                                id name tagline url
                                createdAt votesCount
                                makers { name }
                            }}
                        }
                    }""",
                    "variables": {"topic": keyword},
                }, headers=headers, timeout=15)
                resp.raise_for_status()
                data = resp.json()

                edges = (data.get("data", {})
                         .get("posts", {})
                         .get("edges", []))

                for edge in edges:
                    node = edge.get("node", {})
                    created = node.get("createdAt", "")
                    if created:
                        pub = datetime.fromisoformat(
                            created.replace("Z", "+00:00")
                        ).replace(tzinfo=None)
                        if pub < cutoff:
                            continue
                    else:
                        pub = datetime.utcnow()

                    name = node.get("name", "")
                    tagline = node.get("tagline", "")
                    text = (name + " " + tagline).lower()
                    matched = [k for k in keywords if k.lower() in text]

                    makers = [m["name"] for m in node.get("makers", [])[:2]]

                    items.append(CrawledItem(
                        title=f"{name} - {tagline}",
                        url=node.get("url", ""),
                        source="producthunt",
                        content_snippet=tagline,
                        author=", ".join(makers),
                        published_at=pub,
                        engagement=node.get("votesCount", 0),
                        language="en",
                        keywords_matched=matched,
                    ))
            except Exception as e:
                print(f"[ProductHunt] Error: {e}")

        seen = set()
        return [i for i in items if i.url not in seen and not seen.add(i.url)]
