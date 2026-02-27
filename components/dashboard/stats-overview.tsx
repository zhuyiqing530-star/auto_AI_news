type Props = {
  totalCount: number;
  sourceStats: { source: string; _count: number }[];
};

export default function StatsOverview({ totalCount, sourceStats }: Props) {
  const activeSources = sourceStats.length;

  return (
    <div className="grid grid-cols-3 gap-4">
      <StatCard label="Articles (72h)" value={totalCount} />
      <StatCard label="Active Sources" value={activeSources} />
      <StatCard label="Sources Total" value={8} />
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg p-4 border"
      style={{ background: "var(--card)", borderColor: "var(--border)" }}>
      <p className="text-xs" style={{ color: "var(--muted-foreground)" }}>{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  );
}
