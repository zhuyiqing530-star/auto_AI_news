"use client";

import { useRouter } from "next/navigation";

type Props = {
  sources: Record<string, { label: string; icon: string; color: string }>;
  activeSource?: string;
  sourceStats: { source: string; _count: number }[];
};

export default function SourceFilter({ sources, activeSource, sourceStats }: Props) {
  const router = useRouter();
  const countMap = Object.fromEntries(sourceStats.map((s) => [s.source, s._count]));

  return (
    <div className="flex gap-2 flex-wrap">
      <FilterPill
        label="All"
        active={!activeSource}
        onClick={() => router.push("/dashboard")}
      />
      {Object.entries(sources).map(([key, src]) => (
        <FilterPill
          key={key}
          label={`${src.icon} ${src.label}`}
          count={countMap[key]}
          active={activeSource === key}
          onClick={() => router.push(`/dashboard?source=${key}`)}
        />
      ))}
    </div>
  );
}

function FilterPill({
  label, count, active, onClick,
}: {
  label: string; count?: number; active: boolean; onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="text-xs px-3 py-1.5 rounded-full border transition-colors"
      style={{
        background: active ? "var(--primary)" : "var(--muted)",
        borderColor: active ? "var(--primary)" : "var(--border)",
        color: active ? "var(--primary-foreground)" : "var(--muted-foreground)",
      }}
    >
      {label}{count !== undefined ? ` (${count})` : ""}
    </button>
  );
}
