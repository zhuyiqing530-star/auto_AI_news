import math
from datetime import datetime
from sources.base import CrawledItem

SOURCE_WEIGHTS = {
    "hackernews": 0.15,
    "github": 0.15,
    "reddit": 0.12,
    "youtube": 0.10,
    "rss": 0.10,
    "producthunt": 0.10,
    "bilibili": 0.08,
    "twitter": 0.08,
}


def compute_relevance(item: CrawledItem, keyword_weights: dict[str, float] | None = None) -> float:
    if keyword_weights is None:
        keyword_weights = {}

    score = 0.0

    # Keyword match (0-0.4)
    matched_weight = sum(keyword_weights.get(k, 1.0) for k in item.keywords_matched)
    score += min(0.4, matched_weight * 0.1)

    # Recency (0-0.2)
    hours_old = (datetime.utcnow() - item.published_at).total_seconds() / 3600
    score += 0.2 * math.exp(-hours_old / 24)

    # Engagement (0-0.25)
    if item.engagement > 0:
        score += 0.25 * min(1.0, math.log10(item.engagement + 1) / 5)

    # Source trust (0-0.15)
    score += SOURCE_WEIGHTS.get(item.source, 0.05)

    return round(min(1.0, score), 4)
