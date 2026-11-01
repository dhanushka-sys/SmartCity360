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
import { Zap, AlertTriangle } from "lucide-react";
import { useTheme } from "@/components/theme-provider";
import { DashboardService, EnergyTrendPoint } from "@/lib/api/dashboard-service";

export function EnergyChart() {
  const [filter, setFilter] = React.useState<"24h" | "7d">("24h");
  const [data, setData] = React.useState<EnergyTrendPoint[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [mounted, setMounted] = React.useState(false);
  const { theme } = useTheme();

  React.useEffect(() => {
    setMounted(true);
    let isMounted = true;
    setLoading(true);
    DashboardService.getStats()
      .then((stats) => {
        if (isMounted) {
          if (stats.energyTrends && stats.energyTrends.length > 0) {
            setData(stats.energyTrends);
          } else {
            setData([]);
          }
          setError(null);
        }
      })
      .catch((err: unknown) => {
        if (isMounted) {
          setData([]);
          setError(err instanceof Error ? err.message : "Real MySQL backend offline");
        }
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
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
            Live database telemetry across Metropolis Neo-Prime
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
        <div className="h-[260px] w-full flex items-center justify-center">
          {loading ? (
            <div className="h-full w-full animate-pulse bg-slate-100 dark:bg-slate-800/40 rounded-xl flex items-center justify-center text-xs text-slate-400">
              Loading live energy telemetry from database...
            </div>
          ) : error || data.length === 0 ? (
            <div className="rounded-xl border border-rose-200 dark:border-rose-900/40 bg-rose-50/50 dark:bg-rose-950/20 p-6 text-center max-w-md w-full">
              <AlertTriangle className="h-6 w-6 text-rose-500 mx-auto mb-2" />
              <p className="text-xs font-semibold text-rose-800 dark:text-rose-200">
                Real Database Telemetry Required
              </p>
              <p className="mt-1 text-[11px] text-rose-600 dark:text-rose-400 leading-relaxed">
                {error || "No energy telemetry loaded. Ensure Tomcat 9 is running with correct MySQL credentials."}
              </p>
            </div>
          ) : mounted ? (
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={data}
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
                  tickFormatter={(val) => `${val >= 1000 ? `${(val / 1000).toFixed(1)}k` : val}`}
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
                                {payload[0]?.value} kW
                              </span>
                            </p>
                            <p className="text-blue-600 dark:text-blue-400 font-medium">
                              Projected:{" "}
                              <span className="font-semibold text-slate-900 dark:text-white">
                                {payload[1]?.value} kW
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
                  dataKey="actual"
                  stroke="#06b6d4"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#energyActual)"
                />
                <Area
                  type="monotone"
                  dataKey="projected"
                  stroke="#3b82f6"
                  strokeWidth={2}
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
      </CardContent>
    </Card>
  );
}
