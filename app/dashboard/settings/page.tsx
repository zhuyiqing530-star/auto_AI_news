import { prisma } from "@/lib/prisma";

export const dynamic = "force-dynamic";

export default async function SettingsPage() {
  const [keywords, sources, logs] = await Promise.all([
    prisma.keywordConfig.findMany({ orderBy: { keyword: "asc" } }),
    prisma.sourceConfig.findMany({ orderBy: { source: "asc" } }),
    prisma.crawlLog.findMany({ orderBy: { startedAt: "desc" }, take: 15 }),
  ]);

  return (
    <div className="p-6 max-w-3xl mx-auto space-y-8">
      <h2 className="text-xl font-semibold">Settings</h2>

      <section>
        <h3 className="text-sm font-medium mb-3" style={{ color: "var(--muted-foreground)" }}>
          Crawl History
        </h3>
        <div className="rounded-lg border overflow-hidden" style={{ borderColor: "var(--border)" }}>
          <table className="w-full text-xs">
            <thead>
              <tr style={{ background: "var(--muted)" }}>
                <th className="text-left p-2">Source</th>
                <th className="text-left p-2">Status</th>
                <th className="text-right p-2">Found</th>
                <th className="text-right p-2">New</th>
                <th className="text-right p-2">Time</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id} className="border-t" style={{ borderColor: "var(--border)" }}>
                  <td className="p-2">{log.source}</td>
                  <td className="p-2">
                    <span style={{
                      color: log.status === "success" ? "var(--success)" : "var(--destructive)"
                    }}>
                      {log.status}
                    </span>
                  </td>
                  <td className="p-2 text-right">{log.itemsFound}</td>
                  <td className="p-2 text-right">{log.itemsNew}</td>
                  <td className="p-2 text-right" style={{ color: "var(--muted-foreground)" }}>
                    {log.durationMs ? `${(log.durationMs / 1000).toFixed(1)}s` : "-"}
                  </td>
                </tr>
              ))}
              {logs.length === 0 && (
                <tr>
                  <td colSpan={5} className="p-4 text-center" style={{ color: "var(--muted-foreground)" }}>
                    No crawl history yet
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h3 className="text-sm font-medium mb-2" style={{ color: "var(--muted-foreground)" }}>
          Quick Start
        </h3>
        <div className="rounded-lg border p-4 text-xs space-y-2"
          style={{ background: "var(--card)", borderColor: "var(--border)", color: "var(--muted-foreground)" }}>
          <p>1. Run crawler once:</p>
          <code className="block bg-black/30 p-2 rounded">cd crawler && python main.py --once</code>
          <p>2. Run crawler with scheduler:</p>
          <code className="block bg-black/30 p-2 rounded">cd crawler && python main.py</code>
          <p>3. Configure API keys in <code>.env</code> file for YouTube, Reddit, GitHub</p>
        </div>
      </section>
    </div>
  );
}
