"use client";

import * as React from "react";
import { Cpu, HardDrive, CheckCircle2, TrendingDown, Layers } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FlyweightMemoryAnalysis } from "@/types/streetlight";
import { useAppMode } from "@/components/mode-provider";

interface FlyweightSavingsCardProps {
  analysis: FlyweightMemoryAnalysis;
}

export function FlyweightSavingsCard({ analysis }: FlyweightSavingsCardProps) {
  const { isAcademic } = useAppMode();

  return (
    <Card className="border-emerald-200 dark:border-emerald-500/20 bg-gradient-to-br from-white via-emerald-50/30 to-emerald-100/30 dark:from-slate-900 dark:via-slate-900/90 dark:to-emerald-950/20 shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CardTitle className="text-sm md:text-base">
              {isAcademic ? "Flyweight Memory Optimization Analysis" : "Fleet Memory & Profile Optimization Analysis"}
            </CardTitle>
            <Badge variant="success" className="text-[10px]">
              {isAcademic ? "Flyweight Pattern" : "Resource Optimization"}
            </Badge>
          </div>
          <span className="text-xs text-emerald-600 dark:text-emerald-400 font-bold font-mono">
            -{analysis.savingsPercentage}% RAM Footprint
          </span>
        </div>
        <CardDescription>
          {isAcademic
            ? "Comparison between standard duplicated object instances vs. Flyweight shared intrinsic profiles"
            : "Comparison between un-optimized per-unit telemetry allocations vs. centralized shared hardware profiles"}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Memory Comparison Bar Visual */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Without Flyweight */}
          <div className="rounded-xl border border-rose-200 dark:border-rose-900/30 bg-rose-50/70 dark:bg-rose-950/10 p-3.5 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-rose-800 dark:text-rose-300">
                {isAcademic ? "Without Flyweight (Duplicated State)" : "Standard Per-Unit Allocation (Duplicated Payloads)"}
              </span>
              <span className="font-mono text-rose-600 dark:text-rose-400 font-bold">
                {(analysis.estimatedMemoryWithoutFlyweightKb / 1024).toFixed(1)} MB
              </span>
            </div>
            <div className="h-3 w-full bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-rose-500 rounded-full w-full" />
            </div>
            <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-snug">
              Every light duplicates optical curves, wattages, maintenance schedules, and warranty payloads
              (1,024 B/light × {analysis.totalLightCount.toLocaleString()} units).
            </p>
          </div>

          {/* With Flyweight */}
          <div className="rounded-xl border border-emerald-200 dark:border-emerald-900/30 bg-emerald-50/70 dark:bg-emerald-950/10 p-3.5 space-y-2">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-emerald-800 dark:text-emerald-300">
                {isAcademic ? "With Flyweight Pattern (Shared Profiles)" : "Centralized Profile Optimization (Shared Instances)"}
              </span>
              <span className="font-mono text-emerald-600 dark:text-emerald-400 font-bold">
                {(analysis.estimatedMemoryWithFlyweightKb / 1024).toFixed(1)} MB
              </span>
            </div>
            <div className="h-3 w-full bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-500 rounded-full"
                style={{ width: `${100 - analysis.savingsPercentage}%` }}
              />
            </div>
            <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-snug">
              Only {analysis.uniqueProfilesCount} shared hardware profiles allocated in memory pool.
              Saved ~{(analysis.memorySavedKb / 1024).toFixed(1)} MB RAM.
            </p>
          </div>
        </div>

        {/* Profile Breakdown Pills */}
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-950/50 p-3 shadow-xs">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 block pb-2">
            {isAcademic ? "Shared Intrinsic Profile Reference Distribution" : "Active Hardware Profile Distribution"}
          </span>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {analysis.profileUsageBreakdown.map((item) => (
              <div
                key={item.profileId}
                className="rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 p-2 text-xs"
              >
                <div className="flex items-center justify-between text-[11px]">
                  <span className="font-medium text-slate-700 dark:text-slate-300 truncate">{item.profileName}</span>
                </div>
                <div className="mt-1 flex items-baseline justify-between">
                  <span className="text-base font-bold text-slate-900 dark:text-white font-mono">
                    {item.assignedLightCount.toLocaleString()}
                  </span>
                  <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-semibold">
                    {((item.assignedLightCount / analysis.totalLightCount) * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
