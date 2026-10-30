"use client";

import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { initialActivityLogs } from "@/lib/mock-data/dashboard-data";
import { formatDate } from "@/lib/utils";

export function SystemActivityFeed() {
  return (
    <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm md:text-base">System Audit &amp; Pattern Activity</CardTitle>
        <CardDescription>
          Unified cross-module telemetry trace
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {initialActivityLogs.map((log) => (
            <div
              key={log.id}
              className="flex items-start gap-3 rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50/70 dark:bg-slate-950/40 p-3 hover:border-slate-300 dark:hover:border-slate-700/80 transition-colors"
            >
              <div className="mt-0.5">
                <span
                  className={`flex h-2 w-2 rounded-full ${
                    log.severity === "CRITICAL"
                      ? "bg-rose-500"
                      : log.severity === "WARNING"
                      ? "bg-amber-500"
                      : log.severity === "SUCCESS"
                      ? "bg-emerald-500"
                      : "bg-cyan-500"
                  }`}
                />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <p className="text-xs font-semibold text-slate-900 dark:text-white truncate">{log.title}</p>
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 shrink-0">
                    {formatDate(log.timestamp)}
                  </span>
                </div>
                <p className="mt-0.5 text-[11px] text-slate-600 dark:text-slate-400 leading-snug">{log.description}</p>
                <div className="mt-2 flex items-center gap-2">
                  <span className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">{log.module}</span>
                  <span className="text-slate-300 dark:text-slate-700">•</span>
                  <Badge variant="outline" className="text-[9px] py-0">
                    {log.patternRelated.replace(/_/g, " ")}
                  </Badge>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
