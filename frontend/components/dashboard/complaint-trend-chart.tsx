"use client";

import * as React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { AlertCircle, AlertTriangle } from "lucide-react";
import { useTheme } from "@/components/theme-provider";
import { DashboardService, ComplaintTrendPoint } from "@/lib/api/dashboard-service";

export function ComplaintTrendChart() {
  const [data, setData] = React.useState<ComplaintTrendPoint[]>([]);
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
          if (stats.complaintTrends && stats.complaintTrends.length > 0) {
            setData(stats.complaintTrends);
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
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-sm md:text-base">
          <AlertCircle className="h-4 w-4 text-amber-500 dark:text-amber-400" />
          <span>7-Day Citizen Complaint Trends</span>
        </CardTitle>
        <CardDescription>
          Live intake vs resolution velocity from MySQL complaints registry
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[260px] w-full flex items-center justify-center">
          {loading ? (
            <div className="h-full w-full animate-pulse bg-slate-100 dark:bg-slate-800/40 rounded-xl flex items-center justify-center text-xs text-slate-400">
              Loading incident trends from database...
            </div>
          ) : error || data.length === 0 ? (
            <div className="rounded-xl border border-rose-200 dark:border-rose-900/40 bg-rose-50/50 dark:bg-rose-950/20 p-6 text-center max-w-md w-full">
              <AlertTriangle className="h-6 w-6 text-rose-500 mx-auto mb-2" />
              <p className="text-xs font-semibold text-rose-800 dark:text-rose-200">
                Real Incident Data Required
              </p>
              <p className="mt-1 text-[11px] text-rose-600 dark:text-rose-400 leading-relaxed">
                {error || "No complaint data loaded. Ensure Tomcat 9 is running with correct MySQL credentials."}
              </p>
            </div>
          ) : mounted ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data}
                margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke={isDark ? "#1e293b" : "#e2e8f0"} vertical={false} />
                <XAxis
                  dataKey="day"
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
                />
                <Tooltip
                  content={({ active, payload, label }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900/95 p-3 shadow-xl backdrop-blur-md text-xs">
                          <p className="font-semibold text-slate-800 dark:text-slate-200">{label}</p>
                          <div className="mt-1 space-y-1">
                            <p className="text-cyan-600 dark:text-cyan-400 font-medium">
                              Submitted:{" "}
                              <span className="font-semibold text-slate-900 dark:text-white">
                                {payload[0]?.value}
                              </span>
                            </p>
                            <p className="text-emerald-600 dark:text-emerald-400 font-medium">
                              Resolved:{" "}
                              <span className="font-semibold text-slate-900 dark:text-white">
                                {payload[1]?.value}
                              </span>
                            </p>
                            <p className="text-rose-600 dark:text-rose-400 font-medium">
                              Escalated:{" "}
                              <span className="font-semibold text-slate-900 dark:text-white">
                                {payload[2]?.value}
                              </span>
                            </p>
                          </div>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Bar dataKey="submitted" fill="#06b6d4" radius={[4, 4, 0, 0]} />
                <Bar dataKey="resolved" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="escalated" fill="#f43f5e" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full w-full animate-pulse bg-slate-100 dark:bg-slate-800/30 rounded-xl" />
          )}
        </div>
      </CardContent>
    </Card>
  );
}
