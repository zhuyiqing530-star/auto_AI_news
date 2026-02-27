export const SOURCES = {
  hackernews: { label: "Hacker News", icon: "🟠", color: "#ff6600" },
  rss: { label: "RSS Feeds", icon: "📡", color: "#f97316" },
  youtube: { label: "YouTube", icon: "🔴", color: "#ff0000" },
  reddit: { label: "Reddit", icon: "🟡", color: "#ff4500" },
  github: { label: "GitHub", icon: "⚫", color: "#333333" },
  bilibili: { label: "Bilibili", icon: "🔵", color: "#00a1d6" },
  producthunt: { label: "Product Hunt", icon: "🟤", color: "#da552f" },
  twitter: { label: "X/Twitter", icon: "✖", color: "#1da1f2" },
} as const;

export type SourceKey = keyof typeof SOURCES;

export const KEYWORDS_EN = [
  "AI", "agents", "Claude Code", "Codex", "OpenClaw",
  "vibe coding", "MCP", "cursor", "windsurf", "AI coding",
  "LLM", "GPT", "AI agent",
];

export const KEYWORDS_ZH = [
  "AI", "智能体", "AI编程", "大模型", "Claude",
  "人工智能", "AI工具",
];
