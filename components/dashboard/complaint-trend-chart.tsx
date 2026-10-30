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
import { AlertCircle } from "lucide-react";
import { initialComplaintTrends } from "@/lib/mock-data/dashboard-data";
import { useTheme } from "@/components/theme-provider";

export function ComplaintTrendChart() {
  const [mounted, setMounted] = React.useState(false);
  const { theme } = useTheme();

  React.useEffect(() => {
    setMounted(true);
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
          Intake vs resolution velocity across the Chain of Responsibility
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[260px] w-full">
          {mounted ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={initialComplaintTrends}
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
        <div className="mt-3 flex items-center justify-center gap-6 text-[11px] text-slate-500 dark:text-slate-400 border-t border-slate-200 dark:border-slate-800/80 pt-3">
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-sm bg-cyan-500" />
            <span>Submitted (Intake)</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-sm bg-emerald-500" />
            <span>Resolved</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-sm bg-rose-500" />
            <span>Escalated to Manager</span>
          </span>
        </div>
      </CardContent>
    </Card>
  );
}
