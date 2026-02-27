import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

export async function GET() {
  let lastCheck = new Date();

  const stream = new ReadableStream({
    async start(controller) {
      const encoder = new TextEncoder();

      const interval = setInterval(async () => {
        try {
          const newArticles = await prisma.article.findMany({
            where: { crawledAt: { gt: lastCheck } },
            orderBy: { relevanceScore: "desc" },
            take: 20,
          });
          if (newArticles.length > 0) {
            const data = `data: ${JSON.stringify(newArticles)}\n\n`;
            controller.enqueue(encoder.encode(data));
            lastCheck = new Date();
          }
        } catch {
          // connection closed
        }
      }, 30000);

      // Send initial heartbeat
      controller.enqueue(encoder.encode("data: {\"type\":\"connected\"}\n\n"));

      // Cleanup
      const cleanup = () => clearInterval(interval);
      controller.enqueue(encoder.encode(""));
      (controller as unknown as { _cleanup: () => void })._cleanup = cleanup;
    },
    cancel() {
      // Stream closed by client
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  });
}
