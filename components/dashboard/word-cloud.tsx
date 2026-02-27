"use client";

type Word = { text: string; value: number };

export default function WordCloud({ words }: { words: Word[] }) {
  if (words.length === 0) {
    return (
      <div className="text-center py-10" style={{ color: "var(--muted-foreground)" }}>
        No keyword data yet
      </div>
    );
  }

  const maxVal = Math.max(...words.map((w) => w.value));
  const minVal = Math.min(...words.map((w) => w.value));
  const range = maxVal - minVal || 1;

  const colors = ["#3b82f6", "#8b5cf6", "#22c55e", "#eab308", "#ef4444", "#f97316", "#06b6d4"];

  return (
    <div
      className="rounded-lg border p-6 flex flex-wrap gap-3 items-center justify-center min-h-[200px]"
      style={{ background: "var(--card)", borderColor: "var(--border)" }}
    >
      {words.map((word, i) => {
        const norm = (word.value - minVal) / range;
        const fontSize = 12 + norm * 28;
        const opacity = 0.5 + norm * 0.5;
        return (
          <span
            key={word.text}
            className="inline-block cursor-default transition-transform hover:scale-110"
            style={{
              fontSize: `${fontSize}px`,
              color: colors[i % colors.length],
              opacity,
              fontWeight: norm > 0.6 ? 700 : 400,
            }}
            title={`${word.text}: ${word.value}`}
          >
            {word.text}
          </span>
        );
      })}
    </div>
  );
}
