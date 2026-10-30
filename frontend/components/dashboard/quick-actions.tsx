"use client";

import * as React from "react";
import Link from "next/link";
import {
  Layers,
  Network,
  AlertTriangle,
  Lightbulb,
  FileCode2,
  CheckCircle2,
  ArrowRight,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

export function QuickActions() {
  const actions = [
    {
      title: "Data Streams",
      desc: "Configure dynamic decorator wrappers",
      pattern: "Decorator Pattern",
      href: "/data-streams",
      icon: Layers,
      color: "text-cyan-600 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-500/10 border-cyan-200 dark:border-cyan-500/20",
    },
    {
      title: "Zone Hierarchy",
      desc: "Dispatch uniform operations to composite nodes",
      pattern: "Composite Pattern",
      href: "/zones",
      icon: Network,
      color: "text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10 border-blue-200 dark:border-blue-500/20",
    },
    {
      title: "Complaint Escalation",
      desc: "Route tickets through Chain of Responsibility",
      pattern: "Chain of Resp.",
      href: "/complaints",
      icon: AlertTriangle,
      color: "text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-500/10 border-amber-200 dark:border-amber-500/20",
    },
    {
      title: "Smart Streetlights",
      desc: "Inspect shared intrinsic Flyweight profiles",
      pattern: "Flyweight Pattern",
      href: "/streetlights",
      icon: Lightbulb,
      color: "text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10 border-emerald-200 dark:border-emerald-500/20",
    },
    {
      title: "Policy DSL Interpreter",
      desc: "Parse & evaluate custom city expressions",
      pattern: "Interpreter Pattern",
      href: "/policies",
      icon: FileCode2,
      color: "text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-500/10 border-purple-200 dark:border-purple-500/20",
    },
    {
      title: "VIVA Test Center",
      desc: "Deterministic interactive 5-pattern test suite",
      pattern: "Academic Testing",
      href: "/test-center",
      icon: CheckCircle2,
      color: "text-emerald-600 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-500/10 border-emerald-200 dark:border-emerald-500/30",
    },
  ];

  return (
    <Card className="border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/70 shadow-sm">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm md:text-base">Quick Access &amp; Scenario Launchers</CardTitle>
        <CardDescription>
          Jump directly to pattern demonstration environments
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {actions.map((act) => {
            const Icon = act.icon;
            return (
              <Link
                key={act.href}
                href={act.href}
                className="group flex flex-col justify-between rounded-xl border border-slate-200 dark:border-slate-800/80 bg-slate-50/70 dark:bg-slate-950/50 p-3.5 hover:border-slate-300 dark:hover:border-slate-700 hover:bg-slate-100/80 dark:hover:bg-slate-900/80 transition-all shadow-xs"
              >
                <div className="flex items-start justify-between">
                  <div className={`rounded-lg border p-2 ${act.color}`}>
                    <Icon className="h-4 w-4" />
                  </div>
                  <span className="text-[10px] font-semibold text-slate-500 dark:text-slate-400 group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">
                    {act.pattern}
                  </span>
                </div>
                <div className="mt-3">
                  <h4 className="text-xs font-semibold text-slate-900 dark:text-white group-hover:text-cyan-700 dark:group-hover:text-cyan-300 transition-colors">
                    {act.title}
                  </h4>
                  <p className="mt-0.5 text-[11px] text-slate-500 dark:text-slate-400 leading-snug">{act.desc}</p>
                </div>
                <div className="mt-3 flex items-center gap-1 text-[11px] font-medium text-cyan-600 dark:text-cyan-400 opacity-90 group-hover:opacity-100">
                  <span>Open Scenario</span>
                  <ArrowRight className="h-3 w-3 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
