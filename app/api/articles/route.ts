import { NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const source = searchParams.get("source");
  const limit = parseInt(searchParams.get("limit") || "50");

  const articles = await prisma.article.findMany({
    where: {
      ...(source ? { source } : {}),
      publishedAt: { gte: new Date(Date.now() - 72 * 3600000) },
    },
    orderBy: { relevanceScore: "desc" },
    take: Math.min(limit, 100),
    include: { relatedProjects: true },
  });

  return NextResponse.json(articles);
}
