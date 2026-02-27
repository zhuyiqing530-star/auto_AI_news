import sqlite3
import json
import re
from datetime import datetime
from config import DB_PATH


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def _to_prisma_datetime(dt_str: str) -> str:
    """Convert a datetime string to Prisma-compatible ISO 8601 format.
    Prisma SQLite expects: 2026-02-26T17:00:00.000Z"""
    # Remove microseconds, ensure .000 milliseconds and Z suffix
    dt_str = dt_str.replace("+00:00", "").rstrip("Z")
    # Strip microseconds if present (anything after seconds)
    if "." in dt_str:
        base, frac = dt_str.split(".", 1)
        ms = frac[:3].ljust(3, "0")
        return f"{base}.{ms}Z"
    return f"{dt_str}.000Z"


def _sanitize(text: str | None) -> str | None:
    """Remove null bytes and other control characters that break Prisma."""
    if text is None:
        return None
    # Remove null bytes and other C0 control chars except \n \r \t
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)


def insert_article(article: dict) -> bool:
    """Insert an article, return True if new, False if duplicate."""
    conn = get_conn()
    try:
        now = _to_prisma_datetime(datetime.utcnow().isoformat())
        pub = _to_prisma_datetime(article["publishedAt"])

        conn.execute(
            """INSERT INTO articles
            (id, title, url, source, contentSnippet, author,
             publishedAt, crawledAt, language, engagementScore,
             relevanceScore, keywordsMatched, contentHash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                article["id"],
                _sanitize(article["title"]),
                article["url"],
                article["source"],
                _sanitize(article.get("contentSnippet", "")),
                _sanitize(article.get("author")),
                pub,
                now,
                article.get("language", "en"),
                article.get("engagementScore", 0),
                article.get("relevanceScore", 0),
                json.dumps(article.get("keywordsMatched", []), ensure_ascii=False),
                article.get("contentHash"),
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def insert_crawl_log(log: dict):
    conn = get_conn()
    conn.execute(
        """INSERT INTO crawl_logs
        (id, source, status, itemsFound, itemsNew,
         errorMsg, startedAt, completedAt, durationMs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            log["id"],
            log["source"],
            log["status"],
            log.get("itemsFound", 0),
            log.get("itemsNew", 0),
            _sanitize(log.get("errorMsg")),
            _to_prisma_datetime(log["startedAt"]),
            _to_prisma_datetime(log["completedAt"]) if log.get("completedAt") else None,
            log.get("durationMs"),
        ),
    )
    conn.commit()
    conn.close()
