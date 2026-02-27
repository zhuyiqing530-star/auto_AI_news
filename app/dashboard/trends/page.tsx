import { prisma } from "@/lib/prisma";
import TrendChart from "@/components/dashboard/trend-chart";
import WordCloud from "@/components/dashboard/word-cloud";

export const dynamic = "force-dynamic";

export default async function TrendsPage() {
  const since = new Date(Date.now() - 72 * 3600000);

  const [articles, sourceStats] = await Promise.all([
    prisma.article.findMany({
      where: { publishedAt: { gte: since } },
      orderBy: { publishedAt: "asc" },
      select: {
        publishedAt: true,
        source: true,
        keywordsMatched: true,
        title: true,
      },
    }),
    prisma.article.groupBy({
      by: ["source"],
      _count: true,
      where: { publishedAt: { gte: since } },
    }),
  ]);

  // Build hourly trend data
  const hourlyMap = new Map<string, Record<string, number>>();
  for (const a of articles) {
    const hour = new Date(a.publishedAt).toISOString().slice(0, 13);
    if (!hourlyMap.has(hour)) hourlyMap.set(hour, {});
    const bucket = hourlyMap.get(hour)!;
    bucket[a.source] = (bucket[a.source] || 0) + 1;
  }

  const trendData = Array.from(hourlyMap.entries())
    .map(([hour, sources]) => ({ hour: hour + ":00Z", ...sources }))
    .sort((a, b) => a.hour.localeCompare(b.hour));

  // Build keyword frequency for word cloud
  const kwFreq: Record<string, number> = {};
  for (const a of articles) {
    const kws: string[] = JSON.parse(a.keywordsMatched || "[]");
    for (const kw of kws) {
      kwFreq[kw] = (kwFreq[kw] || 0) + 1;
    }
  }
  const wordData = Object.entries(kwFreq)
    .map(([text, value]) => ({ text, value }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 40);

  const pieData = sourceStats.map((s) => ({
    name: s.source,
    value: s._count,
  }));

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-8">
      <h2 className="text-xl font-semibold">Trends</h2>
      <section>
        <h3 className="text-sm mb-3" style={{ color: "var(--muted-foreground)" }}>
          Article Volume (72h)
        </h3>
        <TrendChart data={trendData} pieData={pieData} />
      </section>
      <section>
        <h3 className="text-sm mb-3" style={{ color: "var(--muted-foreground)" }}>
          Keyword Cloud
        </h3>
        <WordCloud words={wordData} />
      </section>
    </div>
  );
}
