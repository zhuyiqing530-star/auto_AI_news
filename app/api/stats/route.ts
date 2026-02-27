import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

export async function GET() {
  const since = new Date(Date.now() - 72 * 3600000);

  const [totalCount, sourceStats, recentLogs] = await Promise.all([
    prisma.article.count({ where: { publishedAt: { gte: since } } }),
    prisma.article.groupBy({
      by: ["source"],
      _count: true,
      where: { publishedAt: { gte: since } },
    }),
    prisma.crawlLog.findMany({
      orderBy: { startedAt: "desc" },
      take: 20,
    }),
  ]);

  return NextResponse.json({ totalCount, sourceStats, recentLogs });
}
