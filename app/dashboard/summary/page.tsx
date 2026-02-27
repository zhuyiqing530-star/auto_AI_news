"use client";

import { useState } from "react";

type SummaryResult = {
  summary: string;
  articleCount: number;
  generatedAt: string;
  tokensUsed: number;
};

export default function SummaryPage() {
  const [result, setResult] = useState<SummaryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function generate() {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch("/api/summary", { method: "POST" });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "请求失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">AI 圈动态总结</h1>
        <button
          onClick={generate}
          disabled={loading}
          className="px-4 py-2 rounded-md text-sm font-medium transition-colors"
          style={{
            background: loading ? "var(--muted)" : "var(--primary)",
            color: loading ? "var(--muted-foreground)" : "var(--primary-foreground)",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "正在生成..." : "生成摘要"}
        </button>
      </div>

      <p className="text-sm mb-4" style={{ color: "var(--muted-foreground)" }}>
        基于 DeepSeek API 对最近 3 天爬取的所有文章进行智能总结，了解 AI 圈最新动态。
      </p>

      {error && (
        <div className="p-4 rounded-md mb-4"
          style={{ background: "var(--destructive)", color: "white" }}>
          {error}
        </div>
      )}

      {loading && (
        <div className="flex items-center gap-3 p-8 justify-center"
          style={{ color: "var(--muted-foreground)" }}>
          <span className="animate-spin text-lg">⟳</span>
          正在调用 DeepSeek 分析文章，请稍候...
        </div>
      )}

      {result && (
        <>
          <div className="flex gap-4 mb-4 text-xs"
            style={{ color: "var(--muted-foreground)" }}>
            <span>分析了 {result.articleCount} 篇文章</span>
            <span>Token 用量: {result.tokensUsed}</span>
            <span>生成于: {new Date(result.generatedAt).toLocaleString("zh-CN")}</span>
          </div>
          <article
            className="prose prose-invert max-w-none p-6 rounded-lg"
            style={{ background: "var(--card)", border: "1px solid var(--border)" }}
          >
            <SummaryContent text={result.summary} />
          </article>
        </>
      )}
    </div>
  );
}

function SummaryContent({ text }: { text: string }) {
  const lines = text.split("\n");
  return (
    <div className="space-y-2">
      {lines.map((line, i) => {
        if (line.startsWith("## ")) {
          return <h2 key={i} className="text-lg font-bold mt-6 mb-2"
            style={{ color: "var(--foreground)" }}>{line.slice(3)}</h2>;
        }
        if (line.startsWith("### ")) {
          return <h3 key={i} className="text-base font-semibold mt-4 mb-1"
            style={{ color: "var(--foreground)" }}>{line.slice(4)}</h3>;
        }
        if (line.startsWith("# ")) {
          return <h1 key={i} className="text-xl font-bold mt-6 mb-3"
            style={{ color: "var(--foreground)" }}>{line.slice(2)}</h1>;
        }
        if (line.startsWith("- ") || line.startsWith("* ")) {
          return <p key={i} className="pl-4 text-sm leading-relaxed"
            style={{ color: "var(--foreground)" }}>• {line.slice(2)}</p>;
        }
        if (line.match(/^\d+\.\s/)) {
          return <p key={i} className="pl-4 text-sm leading-relaxed"
            style={{ color: "var(--foreground)" }}>{line}</p>;
        }
        if (line.trim() === "") return <br key={i} />;
        return <p key={i} className="text-sm leading-relaxed"
          style={{ color: "var(--foreground)" }}>{line}</p>;
      })}
    </div>
  );
}
