"use client";

import { useArticleStream } from "@/lib/use-article-stream";

export default function LiveBanner() {
  const { newArticles, connected } = useArticleStream();

  return (
    <div className="flex items-center gap-3 text-xs px-4 py-2 border-b"
      style={{ borderColor: "var(--border)", background: "var(--muted)" }}>
      <span className="flex items-center gap-1.5">
        <span className="w-2 h-2 rounded-full"
          style={{ background: connected ? "var(--success)" : "var(--destructive)" }} />
        {connected ? "Live" : "Offline"}
      </span>
      {newArticles.length > 0 && (
        <a href="/dashboard" className="text-blue-400 hover:underline">
          {newArticles.length} new article{newArticles.length > 1 ? "s" : ""}
        </a>
      )}
    </div>
  );
}
