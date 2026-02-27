import type { Metadata } from "next";
import "./globals.css";
import LiveBanner from "@/components/dashboard/live-banner";

export const metadata: Metadata = {
  title: "AI News Aggregator",
  description: "AI 资讯实时聚合仪表盘",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh">
      <body className="antialiased">
        <div className="flex h-screen">
          <Sidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            <LiveBanner />
            <main className="flex-1 overflow-auto">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}

function Sidebar() {
  return (
    <aside className="w-56 border-r flex flex-col p-4 gap-1"
      style={{ borderColor: "var(--border)", background: "var(--card)" }}>
      <h1 className="text-lg font-bold mb-4 px-2">AI News</h1>
      <NavLink href="/dashboard" label="Dashboard" />
      <NavLink href="/dashboard/summary" label="AI 总结" />
      <NavLink href="/dashboard/trends" label="Trends" />
      <NavLink href="/dashboard/settings" label="Settings" />
    </aside>
  );
}

function NavLink({ href, label }: { href: string; label: string }) {
  return (
    <a href={href}
      className="block px-3 py-2 rounded-md text-sm hover:bg-white/5 transition-colors"
      style={{ color: "var(--muted-foreground)" }}>
      {label}
    </a>
  );
}
