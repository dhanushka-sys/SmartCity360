"use client";

import * as React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Zap } from "lucide-react";
import { initialEnergyTrends } from "@/lib/mock-data/dashboard-data";
import { useTheme } from "@/components/theme-provider";

export function EnergyChart() {
  const [filter, setFilter] = React.useState<"24h" | "7d">("24h");
  const [mounted, setMounted] = React.useState(false);
  const { theme } = useTheme();

  React.useEffect(() => {
    setMounted(true);
  }, []);

  const isDark = theme === "dark";

  return (
    <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-4">
        <div>
          <CardTitle className="flex items-center gap-2 text-sm md:text-base">
            <Zap className="h-4 w-4 text-cyan-500 dark:text-cyan-400" />
            <span>Smart Grid Energy Consumption</span>
          </CardTitle>
          <CardDescription>
            Actual vs projected megawatt telemetry across Metropolis Neo-Prime
          </CardDescription>
        </div>
        <div className="flex items-center gap-1 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-950/60 p-1">
          <button
            onClick={() => setFilter("24h")}
            className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
              filter === "24h"
                ? "bg-white dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-semibold shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
            }`}
          >
            24 Hours
          </button>
          <button
            onClick={() => setFilter("7d")}
            className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
              filter === "7d"
                ? "bg-white dark:bg-slate-800 text-cyan-700 dark:text-cyan-300 font-semibold shadow-xs"
                : "text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200"
            }`}
          >
            7 Days
          </button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="h-[260px] w-full">
          {mounted ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={initialEnergyTrends}
                margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="energyActual" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="energyProjected" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={isDark ? "#1e293b" : "#e2e8f0"} vertical={false} />
                <XAxis
                  dataKey="time"
                  stroke="#64748b"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="#64748b"
                  fontSize={11}
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(val) => `${val / 1000}k`}
                />
                <Tooltip
                  content={({ active, payload, label }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900/95 p-3 shadow-xl backdrop-blur-md text-xs">
                          <p className="font-semibold text-slate-800 dark:text-slate-200">{label}</p>
                          <div className="mt-1 space-y-1">
                            <p className="text-cyan-600 dark:text-cyan-400 font-medium">
                              Actual:{" "}
                              <span className="font-semibold text-slate-900 dark:text-white">
                                {payload[0]?.value} kWh
                              </span>
                            </p>
                            <p className="text-blue-600 dark:text-blue-400 font-medium">
                              Projected:{" "}
                              <span className="font-semibold text-slate-900 dark:text-white">
                                {payload[1]?.value} kWh
                              </span>
                            </p>
                          </div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="actualKwh"
                  stroke="#0891b2"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#energyActual)"
                />
                <Area
                  type="monotone"
                  dataKey="projectedKwh"
                  stroke="#2563eb"
                  strokeWidth={1.5}
                  strokeDasharray="4 4"
                  fillOpacity={1}
                  fill="url(#energyProjected)"
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full w-full animate-pulse bg-slate-100 dark:bg-slate-800/30 rounded-xl" />
          )}
        </div>
        <div className="mt-3 flex items-center justify-between text-[11px] text-slate-500 dark:text-slate-400 border-t border-slate-200 dark:border-slate-800/80 pt-3">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-cyan-500" />
              <span>Real-time Composite Rollup</span>
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-blue-500" />
              <span>Predicted Baseline</span>
            </span>
          </div>
          <span className="text-slate-700 dark:text-slate-300 font-medium">Peak Capacity: 5,000 kW</span>
        </div>
      </CardContent>
    </Card>
  );
}
