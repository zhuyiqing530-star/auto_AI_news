import httpx
from datetime import datetime, timedelta
from .base import BaseSource, CrawledItem


class BilibiliSource(BaseSource):
    """Bilibili public search API (no auth needed)"""
    SEARCH_URL = "https://api.bilibili.com/x/web-interface/search/type"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com",
    }

    def fetch(self, keywords: list[str], since_hours: int = 72) -> list[CrawledItem]:
        items = []
        zh_keywords = [k for k in keywords if any("\u4e00" <= c <= "\u9fff" for c in k)]
        if not zh_keywords:
            zh_keywords = ["AI", "智能体", "AI编程"]

        for keyword in zh_keywords[:5]:
            try:
                resp = httpx.get(self.SEARCH_URL, params={
                    "search_type": "video",
                    "keyword": keyword,
                    "order": "pubdate",
                    "page": 1,
                }, headers=self.HEADERS, timeout=15)
                resp.raise_for_status()
                data = resp.json()

                for v in data.get("data", {}).get("result", []) or []:
                    pub_ts = v.get("pubdate", 0)
                    pub_dt = datetime.utcfromtimestamp(pub_ts)
                    if pub_dt < datetime.utcnow() - timedelta(hours=since_hours):
                        continue

                    title = v.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", "")
                    text = (title + " " + v.get("description", "")).lower()
                    matched = [k for k in keywords if k.lower() in text]

                    items.append(CrawledItem(
                        title=title,
                        url=f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                        source="bilibili",
                        content_snippet=v.get("description", "")[:500],
                        author=v.get("author", ""),
                        published_at=pub_dt,
                        engagement=v.get("play", 0),
                        language="zh",
                        keywords_matched=matched,
                    ))
                import time; time.sleep(2)
            except Exception as e:
                print(f"[Bilibili] Error fetching '{keyword}': {e}")

        seen = set()
        return [i for i in items if i.url not in seen and not seen.add(i.url)]
