"use client";

import {
  AreaChart, Area, XAxis, YAxis, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from "recharts";
import { SOURCES } from "@/lib/constants";

const COLORS = ["#3b82f6", "#ef4444", "#22c55e", "#eab308", "#8b5cf6", "#f97316", "#06b6d4", "#ec4899"];

type Props = {
  data: Record<string, unknown>[];
  pieData: { name: string; value: number }[];
};

export default function TrendChart({ data, pieData }: Props) {
  const sourceKeys = Object.keys(SOURCES);

  return (
    <div className="space-y-6">
      <div className="rounded-lg border p-4" style={{ background: "var(--card)", borderColor: "var(--border)" }}>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={data}>
            <XAxis
              dataKey="hour"
              tick={{ fontSize: 10, fill: "var(--muted-foreground)" }}
              tickFormatter={(v: string) => v.slice(5, 13)}
            />
            <YAxis tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} />
            <Tooltip
              contentStyle={{ background: "#1a1a1a", border: "1px solid #333", borderRadius: 8, fontSize: 12 }}
            />
            {sourceKeys.map((key, i) => (
              <Area
                key={key}
                type="monotone"
                dataKey={key}
                stackId="1"
                stroke={COLORS[i % COLORS.length]}
                fill={COLORS[i % COLORS.length]}
                fillOpacity={0.3}
              />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="rounded-lg border p-4" style={{ background: "var(--card)", borderColor: "var(--border)" }}>
        <p className="text-sm mb-2" style={{ color: "var(--muted-foreground)" }}>Source Distribution</p>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%"
              outerRadius={80} label>
              {pieData.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Legend />
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
