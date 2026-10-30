"use client";

import * as React from "react";
import {
  Network,
  Lightbulb,
  AlertTriangle,
  Layers,
  FileCode2,
  TrendingUp,
  ShieldCheck,
  Zap,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAppMode } from "@/components/mode-provider";

export function BentoKpi() {
  const { isAcademic } = useAppMode();

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Zones (Composite) */}
      <Card className="relative overflow-hidden border-blue-200 dark:border-blue-500/20 bg-gradient-to-br from-white via-blue-50/30 to-blue-100/40 dark:from-slate-900/90 dark:via-slate-900/60 dark:to-blue-950/30 hover:border-blue-400 dark:hover:border-blue-500/40 shadow-sm transition-all">
        <CardContent className="p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Managed Zones
            </span>
            <div className="rounded-xl bg-blue-100 dark:bg-blue-500/10 p-2 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-500/20">
              <Network className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">19</span>
            <span className="text-xs text-slate-500 dark:text-slate-400">
              {isAcademic ? "composite nodes" : "facilities active"}
            </span>
          </div>
          <div className="mt-3 flex items-center justify-between border-t border-slate-200 dark:border-slate-800/80 pt-2.5 text-[11px] text-slate-600 dark:text-slate-400">
            <span>3 Districts • 6 Streets • 10 Bldgs</span>
            <Badge variant="blue" className="text-[10px]">
              {isAcademic ? "Composite" : "Hierarchy"}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* 2. Streetlights (Flyweight) */}
      <Card className="relative overflow-hidden border-emerald-200 dark:border-emerald-500/20 bg-gradient-to-br from-white via-emerald-50/30 to-emerald-100/40 dark:from-slate-900/90 dark:via-slate-900/60 dark:to-emerald-950/30 hover:border-emerald-400 dark:hover:border-emerald-500/40 shadow-sm transition-all">
        <CardContent className="p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Smart Streetlights
            </span>
            <div className="rounded-xl bg-emerald-100 dark:bg-emerald-500/10 p-2 text-emerald-600 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-500/20">
              <Lightbulb className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">24,500</span>
            <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">88.8% RAM Saved</span>
          </div>
          <div className="mt-3 flex items-center justify-between border-t border-slate-200 dark:border-slate-800/80 pt-2.5 text-[11px] text-slate-600 dark:text-slate-400">
            <span>{isAcademic ? "4 Flyweight Profiles Shared" : "4 Shared LED Profiles"}</span>
            <Badge variant="success" className="text-[10px]">
              {isAcademic ? "Flyweight" : "Optimized"}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* 3. Complaints (Chain of Responsibility) */}
      <Card className="relative overflow-hidden border-amber-200 dark:border-amber-500/20 bg-gradient-to-br from-white via-amber-50/30 to-amber-100/40 dark:from-slate-900/90 dark:via-slate-900/60 dark:to-amber-950/30 hover:border-amber-400 dark:hover:border-amber-500/40 shadow-sm transition-all">
        <CardContent className="p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Active Complaints
            </span>
            <div className="rounded-xl bg-amber-100 dark:bg-amber-500/10 p-2 text-amber-600 dark:text-amber-400 border border-amber-200 dark:border-amber-500/20">
              <AlertTriangle className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">4</span>
            <span className="text-xs text-rose-600 dark:text-rose-400 font-medium">2 High/Critical</span>
          </div>
          <div className="mt-3 flex items-center justify-between border-t border-slate-200 dark:border-slate-800/80 pt-2.5 text-[11px] text-slate-600 dark:text-slate-400">
            <span>Local → Supervisor → Manager</span>
            <Badge variant="warning" className="text-[10px]">
              {isAcademic ? "Chain of Resp." : "Escalation Queue"}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* 4. Stream Decorators & Policy Interpreter */}
      <Card className="relative overflow-hidden border-cyan-200 dark:border-cyan-500/20 bg-gradient-to-br from-white via-cyan-50/30 to-cyan-100/40 dark:from-slate-900/90 dark:via-slate-900/60 dark:to-cyan-950/30 hover:border-cyan-400 dark:hover:border-cyan-500/40 shadow-sm transition-all">
        <CardContent className="p-5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Data Stream Events
            </span>
            <div className="rounded-xl bg-cyan-100 dark:bg-cyan-500/10 p-2 text-cyan-600 dark:text-cyan-400 border border-cyan-200 dark:border-cyan-500/20">
              <Layers className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">1.42M</span>
            <span className="text-xs text-cyan-600 dark:text-cyan-400 font-medium">3 Active Layers</span>
          </div>
          <div className="mt-3 flex items-center justify-between border-t border-slate-200 dark:border-slate-800/80 pt-2.5 text-[11px] text-slate-600 dark:text-slate-400">
            <span>Auth + Cipher + Comp</span>
            <Badge variant="info" className="text-[10px]">
              {isAcademic ? "Decorator" : "Secured"}
            </Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
