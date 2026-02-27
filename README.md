# AI News Aggregator

AI 资讯实时聚合仪表盘 — 自动爬取多平台 AI 相关内容，可视化展示趋势和热点。

## Features

- **多平台爬取**: Hacker News, RSS, YouTube, Bilibili, GitHub, Reddit, X/Twitter, Product Hunt
- **智能评分**: 关键词匹配 + 时效性 + 互动量 + 来源权重
- **实时推送**: SSE 实时更新，新文章自动推送到仪表盘
- **AI 总结**: 基于 DeepSeek API 自动生成 AI 圈动态报告
- **可视化**: 趋势图、词云、数据源分布饼图
- **桌面通知**: 高相关性文章自动弹窗提醒

## Tech Stack

- **Frontend**: Next.js 16 + Tailwind CSS v4 + Recharts
- **Crawler**: Python (httpx + feedparser + APScheduler)
- **Database**: SQLite (Prisma schema, Python writes)
- **Realtime**: Server-Sent Events (SSE)

## Quick Start

### 1. Install dependencies

```bash
npm install
pip install -r crawler/requirements.txt
```

### 2. Setup database

```bash
npx prisma migrate dev
```

### 3. Configure API keys

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 4. Run crawler

```bash
cd crawler
python main.py --once    # Single run
python main.py           # Continuous scheduling
```

### 5. Start dashboard

```bash
npm run dev
# Open http://localhost:3000
```

## API Keys

| Platform | Required | How to get |
|----------|----------|------------|
| YouTube | Optional | [Google Cloud Console](https://console.cloud.google.com/apis/credentials) |
| Reddit | Optional | [Reddit Apps](https://www.reddit.com/prefs/apps) |
| GitHub | Optional | [Personal Access Tokens](https://github.com/settings/tokens/new) |
| Product Hunt | Optional | [PH API Dashboard](https://www.producthunt.com/v2/oauth/applications) |
| DeepSeek | For AI Summary | [DeepSeek Platform](https://platform.deepseek.com/) |

## License

MIT
