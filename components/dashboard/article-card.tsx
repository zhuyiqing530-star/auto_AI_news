"use client";

import { SOURCES } from "@/lib/constants";
import type { SourceKey } from "@/lib/constants";

type Article = {
  id: string;
  title: string;
  url: string;
  source: string;
  contentSnippet: string;
  author: string | null;
  publishedAt: string | Date;
  relevanceScore: number;
  engagementScore: number;
  keywordsMatched: string;
  isRead: boolean;
  isBookmarked: boolean;
  relatedProjects: { id: string; name: string; url: string; platform: string; stars: number | null }[];
};

export default function ArticleCard({ article }: { article: Article }) {
  const source = SOURCES[article.source as SourceKey];
  const keywords: string[] = JSON.parse(article.keywordsMatched || "[]");
  const timeAgo = getTimeAgo(new Date(article.publishedAt));

  return (
    <div
      className="rounded-lg p-4 border transition-colors hover:border-blue-500/30"
      style={{
        background: "var(--card)",
        borderColor: article.isRead ? "var(--border)" : "var(--primary)",
        opacity: article.isRead ? 0.7 : 1,
      }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs">{source?.icon}</span>
            <span className="text-xs" style={{ color: source?.color }}>
              {source?.label}
            </span>
            <span className="text-xs" style={{ color: "var(--muted-foreground)" }}>
              {timeAgo}
            </span>
          </div>
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-sm hover:underline line-clamp-2"
          >
            {article.title}
          </a>
          {article.contentSnippet && (
            <p className="text-xs mt-1 line-clamp-2" style={{ color: "var(--muted-foreground)" }}>
              {article.contentSnippet}
            </p>
          )}
        </div>
        <RelevanceBadge score={article.relevanceScore} />
      </div>

      <div className="flex items-center gap-2 mt-2 flex-wrap">
        {[...new Set(keywords)].slice(0, 3).map((kw, i) => (
          <span key={i} className="text-xs px-2 py-0.5 rounded-full"
            style={{ background: "var(--muted)", color: "var(--muted-foreground)" }}>
            {kw}
          </span>
        ))}
        {article.author && (
          <span className="text-xs" style={{ color: "var(--muted-foreground)" }}>
            by {article.author}
          </span>
        )}
        {article.engagementScore > 0 && (
          <span className="text-xs" style={{ color: "var(--muted-foreground)" }}>
            {formatEngagement(article.engagementScore)}
          </span>
        )}
      </div>

      {article.relatedProjects.length > 0 && (
        <div className="mt-2 pt-2 border-t" style={{ borderColor: "var(--border)" }}>
          <span className="text-xs" style={{ color: "var(--muted-foreground)" }}>Related: </span>
          {article.relatedProjects.map((p) => (
            <a key={p.id} href={p.url} target="_blank" rel="noopener noreferrer"
              className="text-xs text-blue-400 hover:underline mr-2">
              {p.name}{p.stars ? ` (${p.stars})` : ""}
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

function RelevanceBadge({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  const color = pct >= 70 ? "var(--success)" : pct >= 40 ? "#eab308" : "var(--muted-foreground)";
  return (
    <span className="text-xs font-mono shrink-0" style={{ color }}>
      {pct}%
    </span>
  );
}

function getTimeAgo(date: Date): string {
  const diff = Date.now() - date.getTime();
  const hours = Math.floor(diff / 3600000);
  if (hours < 1) return "just now";
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

function formatEngagement(n: number): string {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
  return String(n);
}
