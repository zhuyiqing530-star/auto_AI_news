import os
from dotenv import load_dotenv

load_dotenv()

# Database path (shared with Next.js Prisma)
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "prisma", "dev.db")

# Crawl lookback window
LOOKBACK_HOURS = 72

# Keywords
KEYWORDS_EN = [
    "AI", "agents", "Claude Code", "Codex", "OpenClaw",
    "vibe coding", "MCP", "cursor", "windsurf", "AI coding",
    "LLM", "GPT", "AI agent",
]

KEYWORDS_ZH = [
    "AI", "智能体", "AI编程", "大模型", "Claude",
    "人工智能", "AI工具",
]

ALL_KEYWORDS = KEYWORDS_EN + KEYWORDS_ZH

# API Keys (from .env)
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
PRODUCTHUNT_TOKEN = os.getenv("PRODUCTHUNT_TOKEN", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
