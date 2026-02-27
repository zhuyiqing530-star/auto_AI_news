import { prisma } from "@/lib/prisma";
import { SOURCES } from "@/lib/constants";
import ArticleCard from "@/components/dashboard/article-card";
import StatsOverview from "@/components/dashboard/stats-overview";
import SourceFilter from "@/components/dashboard/source-filter";

export const dynamic = "force-dynamic";

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: Promise<{ source?: string }>;
}) {
  const params = await searchParams;
  const sourceFilter = params.source;

  const where = {
    ...(sourceFilter ? { source: sourceFilter } : {}),
    publishedAt: {
      gte: new Date(Date.now() - 72 * 60 * 60 * 1000),
    },
  };

  const [articles, totalCount, sourceStats] = await Promise.all([
    prisma.article.findMany({
      where,
      orderBy: { relevanceScore: "desc" },
      take: 50,
      include: { relatedProjects: true },
    }),
    prisma.article.count({ where }),
    prisma.article.groupBy({
      by: ["source"],
      _count: true,
      where: {
        publishedAt: { gte: new Date(Date.now() - 72 * 60 * 60 * 1000) },
      },
    }),
  ]);

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      <h2 className="text-xl font-semibold">Dashboard</h2>
      <StatsOverview totalCount={totalCount} sourceStats={sourceStats} />
      <SourceFilter
        sources={SOURCES}
        activeSource={sourceFilter}
        sourceStats={sourceStats}
      />
      <div className="space-y-3">
        {articles.length === 0 ? (
          <EmptyState />
        ) : (
          articles.map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))
        )}
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="text-center py-20" style={{ color: "var(--muted-foreground)" }}>
      <p className="text-lg">No articles yet</p>
      <p className="text-sm mt-2">Start the Python crawler to fetch data</p>
      <code className="text-xs mt-4 block opacity-60">
        cd crawler && python main.py --once
      </code>
    </div>
  );
}
