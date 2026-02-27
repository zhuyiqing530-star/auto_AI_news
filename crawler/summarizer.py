"""AI News Summarizer using DeepSeek API."""
import json
import sqlite3
import httpx
from datetime import datetime, timedelta
from config import DB_PATH, DEEPSEEK_API_KEY


DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

SYSTEM_PROMPT = """你是一位专业的 AI 行业分析师。请根据提供的新闻标题和摘要，生成一份简洁的 AI 圈动态总结报告。

要求：
1. **热点事件**：最近发生了哪些重要的 AI 相关事件（按重要性排序，最多5条）
2. **新项目/产品**：有哪些新的 AI 项目、工具或产品发布（最多5条）
3. **技术趋势**：当前 AI 圈的技术趋势和热门话题
4. **社区动态**：开发者社区在讨论什么

格式要求：
- 使用中文输出
- 每个部分用 markdown 标题分隔
- 每条内容简洁明了，1-2句话
- 如果有相关链接，附上原文URL"""


def get_recent_articles(hours: int = 72) -> list[dict]:
    """Fetch recent high-relevance articles from DB."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"

    rows = conn.execute(
        """SELECT title, url, source, contentSnippet, author,
                  publishedAt, engagementScore, relevanceScore, keywordsMatched
           FROM articles
           WHERE crawledAt > ?
           ORDER BY relevanceScore DESC, engagementScore DESC
           LIMIT 80""",
        (cutoff,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def build_prompt(articles: list[dict]) -> str:
    """Build the user prompt from articles."""
    lines = []
    for i, a in enumerate(articles, 1):
        snippet = (a.get("contentSnippet") or "")[:150]
        lines.append(
            f"{i}. [{a['source']}] {a['title']}\n"
            f"   URL: {a['url']}\n"
            f"   摘要: {snippet}\n"
            f"   关键词: {a.get('keywordsMatched', '[]')}"
        )
    return (
        f"以下是最近3天内爬取到的 {len(articles)} 条 AI 相关资讯：\n\n"
        + "\n\n".join(lines)
        + "\n\n请根据以上内容生成 AI 圈动态总结报告。"
    )


def summarize(hours: int = 72) -> dict:
    """Generate a summary of recent AI news using DeepSeek."""
    if not DEEPSEEK_API_KEY:
        return {"error": "DEEPSEEK_API_KEY not configured in .env"}

    articles = get_recent_articles(hours)
    if not articles:
        return {"error": "No articles found in the database"}

    user_prompt = build_prompt(articles)

    resp = httpx.post(
        DEEPSEEK_URL,
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
        },
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()

    content = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})

    return {
        "summary": content,
        "articleCount": len(articles),
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "tokensUsed": usage.get("total_tokens", 0),
    }


if __name__ == "__main__":
    import sys
    result = summarize()
    # Output JSON for API route to parse
    print(json.dumps(result, ensure_ascii=False))
