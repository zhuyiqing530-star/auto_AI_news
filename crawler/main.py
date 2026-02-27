"""AI News Aggregator - Crawler Entry Point"""
import sys
import os
import time
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.dirname(__file__))

from config import ALL_KEYWORDS, LOOKBACK_HOURS
from db import insert_article, insert_crawl_log
from config import YOUTUBE_API_KEY, GITHUB_TOKEN
from sources import (
    HackerNewsSource, RSSSource, YouTubeSource,
    BilibiliSource, GitHubSource, RedditSource,
    TwitterSource, ProductHuntSource,
)
from processors.scorer import compute_relevance
from processors.dedup import compute_content_hash
from notifiers.desktop import notify


def generate_id():
    import random, string
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=25))


def crawl_source(source_instance, source_name: str):
    """Run a single source crawl and save results."""
    log_id = generate_id()
    started = datetime.utcnow()
    print(f"[{source_name}] Starting crawl...")

    try:
        items = source_instance.fetch(ALL_KEYWORDS, LOOKBACK_HOURS)
        new_count = 0

        for item in items:
            score = compute_relevance(item)
            article = {
                "id": generate_id(),
                "title": item.title,
                "url": item.url,
                "source": item.source,
                "contentSnippet": item.content_snippet,
                "author": item.author,
                "publishedAt": item.published_at.isoformat(),
                "language": item.language,
                "engagementScore": item.engagement,
                "relevanceScore": score,
                "keywordsMatched": item.keywords_matched,
                "contentHash": compute_content_hash(item.title),
            }
            if insert_article(article):
                new_count += 1
                if score > 0.6:
                    notify(f"AI News: {source_name}", item.title[:150])

        elapsed = int((datetime.utcnow() - started).total_seconds() * 1000)
        print(f"[{source_name}] Done: {len(items)} found, {new_count} new ({elapsed}ms)")

        insert_crawl_log({
            "id": log_id,
            "source": source_name,
            "status": "success",
            "itemsFound": len(items),
            "itemsNew": new_count,
            "errorMsg": None,
            "startedAt": started.isoformat(),
            "completedAt": datetime.utcnow().isoformat(),
            "durationMs": elapsed,
        })
    except Exception as e:
        print(f"[{source_name}] Error: {e}")
        insert_crawl_log({
            "id": log_id,
            "source": source_name,
            "status": "error",
            "itemsFound": 0,
            "itemsNew": 0,
            "errorMsg": str(e),
            "startedAt": started.isoformat(),
            "completedAt": datetime.utcnow().isoformat(),
            "durationMs": int((datetime.utcnow() - started).total_seconds() * 1000),
        })


# All available sources
SOURCES = {
    "hackernews": HackerNewsSource(),
    "rss": RSSSource(),
    "youtube": YouTubeSource(YOUTUBE_API_KEY),
    "bilibili": BilibiliSource(),
    "github": GitHubSource(GITHUB_TOKEN),
    "reddit": RedditSource(),
    "twitter": TwitterSource(),
    "producthunt": ProductHuntSource(),
}


def run_once():
    """Run all sources once."""
    print(f"\n{'='*50}")
    print(f"Crawl started at {datetime.utcnow().isoformat()}")
    print(f"{'='*50}")
    for name, source in SOURCES.items():
        crawl_source(source, name)
    print(f"{'='*50}")
    print("Crawl complete.\n")


def run_scheduler():
    """Run on a schedule using APScheduler."""
    from apscheduler.schedulers.blocking import BlockingScheduler

    scheduler = BlockingScheduler()

    # High frequency (every 1h)
    scheduler.add_job(lambda: crawl_source(SOURCES["hackernews"], "hackernews"),
                      "interval", hours=1, id="hackernews")
    scheduler.add_job(lambda: crawl_source(SOURCES["rss"], "rss"),
                      "interval", hours=1, id="rss")

    # Medium frequency (every 2-4h)
    scheduler.add_job(lambda: crawl_source(SOURCES["reddit"], "reddit"),
                      "interval", hours=2, id="reddit")
    scheduler.add_job(lambda: crawl_source(SOURCES["youtube"], "youtube"),
                      "interval", hours=4, id="youtube")
    scheduler.add_job(lambda: crawl_source(SOURCES["bilibili"], "bilibili"),
                      "interval", hours=4, id="bilibili")
    scheduler.add_job(lambda: crawl_source(SOURCES["twitter"], "twitter"),
                      "interval", hours=4, id="twitter")

    # Low frequency (every 6h)
    scheduler.add_job(lambda: crawl_source(SOURCES["github"], "github"),
                      "interval", hours=6, id="github")
    scheduler.add_job(lambda: crawl_source(SOURCES["producthunt"], "producthunt"),
                      "interval", hours=6, id="producthunt")

    print("Scheduler started. Press Ctrl+C to stop.")
    run_once()
    scheduler.start()


if __name__ == "__main__":
    if "--once" in sys.argv:
        run_once()
    else:
        run_scheduler()
